import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Zoom')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')
    black = pygame.Color('black')

    coordinates = []
    text = open('points.txt', encoding='utf8')

    b, c = 0, 0
    lines = text.readlines()
    for _ in lines:
        items = _.split(", ")
        for i, item in enumerate(items):
            points = item[1: -1].split(';')
            if len(points) < 2:
                continue
            if ',' in points[0]:
                points[0] = points[0].replace(',', '.')
            if ',' in points[1]:
                points[1] = points[1].replace(',', '.')
            coordinates.append([(float(points[0])), (float(points[1]) * -1)])
    k = 1
    coordinates1 = []
    running = True
    while running:
        screen.fill(black)
        coordinates1.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
                k *= 1.5
            if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                k /= 1.5
        for i in coordinates:
            x, y = i[0], i[1]
            coordinates1.append([float(x * k + width / 2), float(y * k + height / 2)])
        pygame.draw.polygon(screen, white, coordinates1, 1)
        pygame.display.update()
