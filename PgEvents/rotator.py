import math

import pygame


def main():
    pygame.init()
    fps = 70
    transform_angle = 0
    center_radius = 10.0
    a = b = 70
    angle = 0.5235987755982988  # 30 градусов в радианах
    osnovanie = math.sqrt((a ** 2 + b ** 2) - (2 * a * b * math.cos(angle)))
    coords = [[(101, 101), (101 + osnovanie / 2, 101 - a), (101 - osnovanie / 2, 101 - a)],
              [(101, 101), (171, 121), ((101 + osnovanie / 2) + 35, 150)],
              [(101, 101), (101 - 70, 121), ((101 - osnovanie / 2) - 35, 150)]]

    pygame.display.set_caption('Вентилятор')
    screen = pygame.display.set_mode([201, 201])
    screen.fill(pygame.Color('black'))
    clock = pygame.time.Clock()
    color = pygame.Color('white')
    screen2 = pygame.Surface((201, 201), pygame.SRCALPHA)
    pygame.draw.circle(screen2, color, (101, 101), center_radius)
    pygame.draw.polygon(screen2, color, coords[0])
    pygame.draw.polygon(screen2, color, coords[1])
    pygame.draw.polygon(screen2, color, coords[2])
    rotation = 0
    screen.blit(screen2, (0, 0))
    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    transform_angle -= 10
                elif event.button == 3:
                    transform_angle += 10
        rotation += transform_angle
        screen3 = pygame.transform.rotate(screen2, rotation)
        rect = screen3.get_rect()
        rect.center = (101, 101)
        screen.blit(screen3, rect)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
