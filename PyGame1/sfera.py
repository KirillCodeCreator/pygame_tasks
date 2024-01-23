import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw(screen, n, w):
    s = w // n
    pygame.draw.ellipse(screen, WHITE, (0, 0, w, w), 1)
    pygame.draw.ellipse(screen, WHITE, (0, w // 2 - s // 2, w, s), 1)
    pygame.draw.ellipse(screen, WHITE, (w // 2 - s // 2, 0, s, w), 1)

    for i in range(n - 1):
        pygame.draw.ellipse(screen, WHITE, (0, w // 2 - s // 2 * (i + 1), w, s * (i + 1)), 1)
        pygame.draw.ellipse(screen, WHITE, (w // 2 - s // 2 * (i + 1), 0, s * (i + 1), w), 1)


def main():
    try:
        n = int(input("Введите целое число эллипсов: "))
    except Exception:
        print("Неправильный формат ввода")
        return

    pygame.init()
    size = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Сфера')

    screen.fill(BLACK)
    draw(screen, n, 300)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
