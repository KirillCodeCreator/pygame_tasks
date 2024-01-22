from random import randint

import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


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
                r = randint(0, 1)
                rect = cell_rect.get_rect(topleft=(x * self.cell_size + self.left, y * self.cell_size + self.top))
                cell_data = (rect, r, (x, y))
                self.cells.append(cell_data)

    def render(self, screen):
        border_color = pygame.Color(WHITE)
        red_color = pygame.Color(RED)
        blue_color = pygame.Color(BLUE)
        for cell_data in self.cells:
            pygame.draw.rect(screen, border_color, cell_data[0], 1)
            if cell_data[1] == 1:
                pygame.draw.circle(screen, red_color, cell_data[0].center, self.cell_size / 2 - 3)
            else:
                pygame.draw.circle(screen, blue_color, cell_data[0].center, self.cell_size / 2 - 3)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        color = self.get_cell_color(col, row)
        self.set_cells_color(col, row, color)

    def get_click(self, mouse_pos):
        cell = (mouse_pos[0], mouse_pos[1])
        self.on_click(cell)

    def set_cells_color(self, col, row, color):
        for idx, cell in enumerate(self.cells):
            if cell[2][0] == col or cell[2][1] == row:
                self.cells[idx] = (cell[0], color, cell[2])

    def get_cell_color(self, col, row):
        for cell in self.cells:
            if cell[2][0] == col and cell[2][1] == row:
                return cell[1]


def main():
    n = int(input("Введите размер доски: "))
    pygame.init()
    width = 25 + 50 * n + 25
    size = width, width
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Недореверси')
    board = Board(n, n)
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
