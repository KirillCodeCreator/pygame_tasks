from random import randint

import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Board:
    cells = list()
    cells_colors = list()
    colors = list()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.colors.append(pygame.Color(RED))
        self.colors.append(pygame.Color(BLUE))

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
        self.board[row][col] = (self.board[row][col] + 1) % 3

    def get_click(self, mouse_pos):
        cell = (mouse_pos[0], mouse_pos[1])
        self.on_click(cell)


def main():
    n = int(input("Введите размер доски: "))
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Недореверси')
    board = Board(n, n)
    board.set_view(50, 50, 55)
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
