import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def render(screen, w, hue):
    color1 = pygame.Color(255, 255, 255)
    hsv = color1.hsva
    color2 = pygame.Color(255, 255, 255)
    hsv2 = color2.hsva
    color3 = pygame.Color(255, 255, 255)
    hsv3 = color3.hsva
    wx = 130 - (w / 2)
    wy = 180 - (w / 2)
    ww = w / 2
    color1.hsva = (hue, hsv[1] + 100, hsv[2] - 25, hsv[3])
    color2.hsva = (hue, hsv2[1] + 100, hsv2[2], hsv[3])
    color3.hsva = (hue, hsv3[1] + 100, hsv3[2] - 50, hsv[3])
    pygame.draw.polygon(screen, color1, ((wx, wy), (wx + w, wy), (wx + w, wy + w), (wx, wy + w)))
    pygame.draw.polygon(screen, color2, ((wx + ww, wy - ww), (wx + ww + w, wy - ww), (wx + w, wy), (wx, wy)))
    pygame.draw.polygon(screen, color3, ((wx + w, wy), (wx + ww + w, wy - ww), (wx + ww + w, wy + ww),
                                         (wx + w, wy + w)))


def main():
    try:
        w, h = map(int, input("Введите W - размер стороны куба и Hue - оттенок (W и Hue):  ").split())
        if w <= 0 or w % 4 != 0 or w > 100 or h < 0 or h > 360:
            raise ValueError
    except Exception:
        print("Неправильный формат ввода")
        return

    pygame.init()
    s = 300
    size = s, s
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Куб')

    screen.fill(BLACK)
    render(screen, w, h)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
