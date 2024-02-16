import os
import sys

import pygame

pygame.init()
FPS = 50
tile_width = tile_height = 50
size = width, height = 650, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Перемещение героя. Новый уровень')
clock = pygame.time.Clock()
player = None
player_start_x = player_start_y = 0
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('ошибка загрузки изображений:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя. Новый уровень", '',
                  "Карта «зациклено»",
                  "Герой двигается как будто по тору",
                  "Движение стрелками на клавиатуре",
                  "Для начала игры нажмите любую клавишу"]
    background = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, True, 'black')
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)
        text_coord += intro_rect.height + 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    with open(filename, 'r') as fd:
        level_map = [line.strip() for line in fd]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')


class Tile(pygame.sprite.Sprite):
    step = 50

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + self.step, tile_height * pos_y + self.step)

    def update(self, *args, **kwargs) -> None:
        pass


class Player(pygame.sprite.Sprite):
    step = 50

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15 + self.step, tile_height * pos_y + 5 + self.step)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx
                self.rect.y -= dy
                return


def generate_level(level):
    global player_start_x, player_start_y
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('wall', x, y)
            if level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_start_x = new_player.rect.x
                player_start_y = new_player.rect.y
                level[y][x] = '.'
    return new_player, x, y


def select_map_level():
    intro_text = ["Выберите уровень", '',
                  "В консоли введите имя файла с расширением",
                  "'level1.txt' или 'level2.txt' или 'level3.txt' или 'level4.txt'"]
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
        filename = os.path.join('data', filename)
        try:
            return generate_level(load_level(filename))
        except (FileNotFoundError, IOError):
            print(f"Произошла ошибка при загрузке файла '{filename}'. Программа будет закрыта")
            terminate()


player, level_x, level_y = select_map_level()

start_screen()


class Camera:

    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, sprite: pygame.sprite.Sprite):
        sprite.rect.x += self.dx
        sprite.rect.y += self.dy

    def update(self, target: pygame.sprite.Sprite):
        self.dx = -(target.rect.x + target.rect.w // 2 - player_start_x)
        self.dy = -(target.rect.y + target.rect.h // 2 - player_start_y)


def flip_tiles(dx, dy):
    if abs(dx) != tile_width and abs(dy) != tile_height:
        return
    top_right_rect = max((i for i in tiles_group if isinstance(i, Tile)),
                         key=lambda t: (t.rect.x, -t.rect.y)).rect.copy()
    bottom_left_rect = min((i for i in tiles_group if isinstance(i, Tile)),
                           key=lambda t: (t.rect.x, -t.rect.y)).rect.copy()
    for tile in tiles_group:
        if dx > 0:
            if tile.rect.right != top_right_rect.right:
                continue
            tile.rect.x = bottom_left_rect.x - top_right_rect.width
        elif dx < 0:
            if tile.rect.left != bottom_left_rect.left:
                continue
            tile.rect.x = top_right_rect.x + bottom_left_rect.width
    for tile in tiles_group:
        if dy > 0:
            if tile.rect.bottom != bottom_left_rect.bottom:
                continue
            tile.rect.y = top_right_rect.y - tile.rect.w
        elif dy < 0:
            if tile.rect.top != top_right_rect.top:
                continue
            tile.rect.y = bottom_left_rect.y + tile.rect.width


camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-tile_width, 0)
            if event.key == pygame.K_RIGHT:
                player.move(tile_width, 0)
            if event.key == pygame.K_UP:
                player.move(0, -tile_height)
            if event.key == pygame.K_DOWN:
                player.move(0, tile_height)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    flip_tiles(camera.dx, camera.dy)
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
