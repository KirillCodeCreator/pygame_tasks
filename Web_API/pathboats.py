import os
import sys

import pygame
import requests


def get_request_result(data):
    geocoder_request = f"https://geocode-maps.yandex.ru/" \
                       f"1.x/" \
                       f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={data}&format=json"
    resp = requests.get(geocoder_request)

    if resp.ok:
        json_resp = resp.json()
        try:
            toponym = json_resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        except (KeyError, IndexError):
            raise ValueError("Ничего не найдено")
        else:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coordinates = toponym['Point']['pos']
            return toponym_address, toponym_coordinates
    else:
        raise ValueError(f"Произошла ошибка\n"
                         f"{geocoder_request}\n"
                         f"Http status {resp.status_code}\n"
                         f"{resp.reason}")


_, back_map_coord = get_request_result('Невская губа')
boat_path = [
    "29.914783,59.891574",
    "30.105881,59.944074",
    "30.237944,59.916487",
    "30.266268,59.919073",
    "30.275489,59.930952",
    "30.310165,59.941203"
]
line_type = 'pm2' + 'org' + 'l'
route_coordinates_map = ','.join(boat_path)
map_request = f"http://static-maps.yandex.ru/1.x/" \
              f"?ll={','.join(back_map_coord.split())}&z=9&l=map&pl={route_coordinates_map}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
pygame.display.set_caption("Маршрут судна")
screen = pygame.display.set_mode((600, 450))
back_map = pygame.image.load(map_file)
screen.blit(back_map, (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)
