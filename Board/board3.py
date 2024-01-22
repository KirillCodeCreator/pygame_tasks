from random import randint

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Board:
    cells = list()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.init_cells()

    def init_cells(self):
        cell_rect = pygame.Surface((self.cell_size, self.cell_size))
        for y in range(self.height):
            for x in range(self.width):
                rect = cell_rect.get_rect(topleft=(x * self.cell_size + self.left, y * self.cell_size + self.top))
                cell_data = (rect, 0, (x, y))
                self.cells.append(cell_data)

    def render(self, screen):
        white_color = pygame.Color(WHITE)
        for cell_data in self.cells:
            if cell_data[1] == 1:
                pygame.draw.rect(screen, white_color, cell_data[0])
            else:
                pygame.draw.rect(screen, white_color, cell_data[0], 1)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        self.invert_cells_color(col, row)

    def get_click(self, mouse_pos):
        cell = (mouse_pos[0], mouse_pos[1])
        self.on_click(cell)

    def invert_cells_color(self, col, row):
        for idx, cell in enumerate(self.cells):
            if cell[2][0] == col or cell[2][1] == row:
                self.cells[idx] = (cell[0], self.invert_color(cell[1]), cell[2])

    def invert_color(self, color):
        if color == 0:
            return 1
        else:
            return 0


def main():
    pygame.init()
    width = 25 + 50 * 5 + 25
    heigth = 25 + 50 * 7 + 25
    size = width, heigth
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Чёрное в белое и наоборот')
    board = Board(5, 7)
    board.set_view(25, 25, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
