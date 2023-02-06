import sys
import requests
from io import BytesIO
from PIL import Image
from params import get_scale_params, lonlat_distance


# python main.py Москва, ул. Ак. Королева, 12
toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('ERROR')
    pass

# Преобразуем ответ в json-объект
json_my_address_response = response.json()
my_addres_long, my_addres_lat = get_scale_params(json_my_address_response)['longitude'], get_scale_params(json_my_address_response)['latitude']




search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = ','.join([my_addres_long, my_addres_lat])
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
json_pharmacy_response = response.json()

# Получаем первую найденную организацию.
organization = json_pharmacy_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
pharmacy_point = organization["geometry"]["coordinates"]

pharmacy_long, pharmacy_lat = pharmacy_point[0], pharmacy_point[1]


# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "l": "map",
    "pt": f"{pharmacy_long},{pharmacy_lat},pm2gnm1~{my_addres_long},{my_addres_lat},pm2rdm1"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

dist = lonlat_distance((float(my_addres_long), float(my_addres_lat)), (pharmacy_long, pharmacy_lat))
print('Aптека:', org_name)
print('Адрес:', org_address)
print('Время работы:', org_time)
print('Расстояние до аптеки:', dist)

Image.open(BytesIO(
    response.content)).show()

