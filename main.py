import sys
import requests
from io import BytesIO
from PIL import Image
from params import get_scale_params


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
json_response = response.json()

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ','.join([get_scale_params(json_response)['longitude'], get_scale_params(json_response)['latitude']]),
    "spn": get_scale_params(json_response)["spn"],
    "l": "map",
    "pt": f"{','.join([get_scale_params(json_response)['longitude'], get_scale_params(json_response)['latitude']])},pm2rdm1"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
