import requests


def get_geocode_result(geocode_data, **params):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode_data,
        "format": "json",
        **params
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    return json_response


def get_toponym(geocode_result):
    try:
        toponym = geocode_result["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
    except (KeyError, IndexError):
        raise ValueError
    return toponym


def get_ll_from_geocode_response(toponym):
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coodrinates.split(" ")
    return toponym_longitude, toponym_latitude


def main():
    print(f"Пример адреса Ленинградский просп., 36")
    user_data = input('Введите адрес: ')
    try:
        point = get_ll_from_geocode_response(get_toponym(get_geocode_result(user_data)))
        nearest_metro = get_toponym(get_geocode_result(','.join(point), kind='metro'))
        print("Ближайщее метро:", nearest_metro['name'], " Координаты:", nearest_metro['Point']['pos'])
    except (ValueError):
        print("Не удалось найти ближайшую станцию метро")


if __name__ == '__main__':
    main()
