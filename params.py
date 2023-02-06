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
