import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = list()
colors.append(RED)
colors.append(GREEN)
colors.append(BLUE)


def render(screen, w, n):
    a = (n - 1) * w
    clrs = list()
    for i in range(n - 1):
        color = i % 3
        clrs.append((colors[color], i))

    for idx, t in enumerate(list(reversed(clrs))):
        pygame.draw.circle(screen, t[0], (a, a), radius=t[1] * w + w)


def main():
    try:
        w, n = map(int, input("Введите w - толщину кольца в пикселях и n - количество колец (w и n):  ").split())
    except Exception:
        print("Неправильный формат ввода")
        return

    pygame.init()
    s = (n * w) * 2
    size = s, s
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Мишень')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        render(screen, w, n)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
