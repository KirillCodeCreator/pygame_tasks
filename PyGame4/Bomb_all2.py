import os
import random

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
width, height = 500, 500
image_size = 75, 75
size = width, height
screen = pygame.display.set_mode(size)
coords = pygame.sprite.Group()


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image = pygame.transform.scale(image, image_size)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - image_size[0])
        self.rect.y = random.randrange(height - image_size[0])
        while pygame.sprite.spritecollideany(self, coords):
            self.rect.x = random.randrange(width - image_size[0])
            self.rect.y = random.randrange(height - image_size[0])
        self.add(coords)

    def get_event(self):
        if self.rect.collidepoint(event.pos):
            return True
        return False


class Boom(Bomb):
    image_boom = load_image("boom.png", -1)
    image_boom = pygame.transform.scale(image_boom, image_size)

    def __init__(self, bomb, group):
        super().__init__(group)
        self.image = self.image_boom
        self.rect = self.image_boom.get_rect()
        self.rect = bomb.rect

    def get_event(self):
        return False


all_sprites = pygame.sprite.Group()
for _ in range(20):
    Bomb(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bombs = []
            for bomb in all_sprites:
                if bomb.get_event() == True:
                    bombs.append(bomb)
            if len(bombs) > 0:
                for bomb in bombs:
                    all_sprites.add(Boom(bomb, all_sprites))
                    all_sprites.remove(bomb)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
