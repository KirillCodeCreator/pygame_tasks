import requests


def get_town_coords(town):
    geocoder_request = f"https://geocode-maps.yandex.ru/" \
                       f"1.x/" \
                       f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={town}" \
                       f"&results=1" \
                       f"&kind=locality&format=json"
    resp = requests.get(geocoder_request)

    if resp.ok:
        json_resp = resp.json()
        try:
            toponym = json_resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        except (KeyError, IndexError):
            raise ValueError("Ничего не найдено")
        else:
            toponym_coordinates = toponym['Point']['pos']
            coords = toponym_coordinates.split(' ')
            return (float(coords[0]), float(coords[1]))
    else:
        raise ValueError(f"Произошла ошибка\n"
                         f"{geocoder_request}\n"
                         f"Http status {resp.status_code}\n"
                         f"{resp.reason}")


def main():
    towns_data = input('Введите города через запятую: ')
    towns = towns_data.split(',')
    data = {}
    for t in towns:
        try:
            coords = get_town_coords(t)
            data[t] = coords[1] # читаем широту
        except (ValueError):
            pass
    if len(data) > 0:
        result = dict(sorted(data.items(), key=lambda item: item[1]))
        first_value = next(iter(result.keys()))
        print(first_value)


if __name__ == '__main__':
    main()
