import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_image = {'wall': load_image('box.png'),
              'empty': load_image('grass.png')}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def update(self, *args):
        x, y = args[0]
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y)
        self.pos = (x, y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя. Камера", '',
                  "Карта двигается",
                  "Герой на месте",
                  "Движение стрелками на клавиатуре",
                  "Для начала игры нажмите любую клавишу"]
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def select_map_level():
    intro_text = ["Выберите уровень", '',
                  "В консоли введите имя файла с расширением",
                  "'level1.txt' или 'level2.txt' или 'level3.txt'"]
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        filename = input('Введите название файла: ')
        try:
            return load_level(filename)
        except (FileNotFoundError, IOError):
            print(f"Произошла ошибка при загрузке файла '{filename}'. Программа будет закрыта")
            terminate()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)


def move_map(origin, movement):
    x, y = origin.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            origin.pos = (x, y - 1)
            for tile in sprite_group:
                px, py = tile.pos
                tile.pos = (px, py + 1)
                tile.update(tile.pos)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            origin.pos = (x, y + 1)
            for tile in sprite_group:
                px, py = tile.pos
                tile.pos = (px, py - 1)
                tile.update(tile.pos)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            origin.pos = (x - 1, y)
            for tile in sprite_group:
                px, py = tile.pos
                tile.pos = (px + 1, py)
                tile.update(tile.pos)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            origin.pos = (x + 1, y)
            for sprite in sprite_group:
                px, py = sprite.pos
                sprite.pos = (px - 1, py)
                sprite.update(sprite.pos)


if __name__ == '__main__':
    pygame.display.set_caption('Перемещение героя. Камера')
    player = None
    running = True
    level_map = select_map_level()
    start_screen()
    hero, max_x, max_y = generate_level(level_map)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_map(hero, 'up')
                if event.key == pygame.K_DOWN:
                    move_map(hero, 'down')
                if event.key == pygame.K_RIGHT:
                    move_map(hero, 'right')
                if event.key == pygame.K_LEFT:
                    move_map(hero, 'left')
        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
