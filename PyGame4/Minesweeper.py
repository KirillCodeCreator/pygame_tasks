import random

import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255, 0)
RED = (255, 0, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Board:
    cells = list()
    krest = 1
    zero = 2
    last_action = 2

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
        red_color = pygame.Color(RED)
        blue_color = pygame.Color(BLUE)
        for cell_data in self.cells:
            pygame.draw.rect(screen, white_color, cell_data[0], 1)

        for cell_data in self.cells:
            if cell_data[1] == 2:
                pygame.draw.circle(screen, red_color, cell_data[0].center, 22, 2)
            elif cell_data[1] == 1:
                rect = pygame.Rect((cell_data[0].left + 2, cell_data[0].top + 2, 44, 44))
                pygame.draw.line(screen, blue_color, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, blue_color, rect.topright, rect.bottomleft, 2)
        pygame.display.update()

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        action = self.get_cell_action(col, row)
        if action != 0:
            return
        self.last_action = self.invert_last_action(self.last_action)
        self.set_cells_action(col, row, self.last_action)

    def get_click(self, mouse_pos):
        cell = (mouse_pos[0], mouse_pos[1])
        self.on_click(cell)

    def invert_last_action(self, action):
        if action == self.krest:
            return self.zero
        else:
            return self.krest

    def set_cells_action(self, col, row, action):
        for idx, cell in enumerate(self.cells):
            if cell[2][0] == col and cell[2][1] == row:
                self.cells[idx] = (cell[0], action, cell[2])
                return

    def get_cell_action(self, col, row):
        for cell in self.cells:
            if cell[2][0] == col and cell[2][1] == row:
                return cell[1]


class Minesweeper(Board):
    current_state = 0

    def __init__(self, width, height, mines):
        super().__init__(width, height)
        self.active_cells = [[-1 for j in range(width)] for i in range(height)]
        while mines > 0:
            col = random.randint(0, width - 1)
            row = random.randint(0, height - 1)
            if self.active_cells[row][col] != 10:
                self.active_cells[row][col] = 10
                mines -= 1

    def render(self, screen):
        super().render(screen)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        if self.active_cells[row][col] == -1:
            self.open_cell(row, col)

    def mines_near_count(self, system):
        count = 0
        for idx in system:
            if self.active_cells[idx[0]][idx[1]] == 10:
                count += 1
        return count

    def get_neighbours(self, cell):
        x, y = cell
        possible_neighbours = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y)
        ]
        real_neighbours = []
        for n in possible_neighbours:
            if n[0] >= 0 and n[0] < self.height:
                if n[1] >= 0 and n[1] < self.width:
                    real_neighbours.append(n)
        return real_neighbours

    def open_cell(self, row, col):
        neighbours = self.get_neighbours((row, col))
        count = self.mines_near_count(neighbours)
        self.active_cells[row][col] = count

    def render(self, screen):
        black_color = pygame.Color(BLACK)
        white_color = pygame.Color(WHITE)
        green_color = pygame.Color(GREEN)
        red_color = pygame.Color(RED)
        screen.fill(black_color)
        for cell_data in self.cells:
            fill_rect = pygame.Rect(
                (cell_data[0].left + 2, cell_data[0].top + 2, self.cell_size - 2, self.cell_size - 2))
            col = cell_data[2][0]
            row = cell_data[2][1]
            if self.active_cells[row][col] == 10:
                screen.fill(rect=fill_rect, color=red_color)
            elif self.active_cells[row][col] > -1:
                count = self.active_cells[row][col]
                font = pygame.font.Font(None, 20)
                text = font.render(str(count), True, green_color)
                screen.blit(text, (cell_data[0].left + 4, cell_data[0].top + 2))
            pygame.draw.rect(screen, white_color, cell_data[0], 1)

        pygame.display.update()


def main():
    cell_size = 25
    cols = 10
    rows = 15
    padding = 25
    mines = 25
    pygame.init()
    width = padding + cell_size * cols + padding
    heigth = padding + cell_size * rows + padding
    size = width, heigth
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Дедушка сапёра')
    minesweeper = Minesweeper(cols, rows, mines)
    minesweeper.set_view(padding, padding, cell_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                minesweeper.get_click(event.pos)
        minesweeper.render(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
