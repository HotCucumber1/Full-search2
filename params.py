import math


def get_scale_params(response):
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Получаем spn
    toponym_delta = toponym["boundedBy"]["Envelope"]
    delta1 = float(toponym_delta["upperCorner"].split()[0]) - float(toponym_delta["lowerCorner"].split()[0])
    delta2 = float(toponym_delta["upperCorner"].split()[1]) - float(toponym_delta["lowerCorner"].split()[1])

    # Собираем параметры для запроса к StaticMapsAPI:
    scale_params = {
        "longitude": toponym_longitude,
        "latitude": toponym_lattitude,
        "spn": ",".join([str(delta1), str(delta2)]),
    }
    return scale_params


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    return distance
