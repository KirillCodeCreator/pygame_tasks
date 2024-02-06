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


class Life(Board):
    current_state = 0

    def __init__(self, width, height):
        super().__init__(width, height)
        self.active_cells = [[0 for x in range(width)] for y in range(height)]

    def render(self, screen):
        super().render(screen)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        if self.active_cells[row][col] == 1:
            self.active_cells[row][col] = 0
        else:
            self.active_cells[row][col] = 1

    # Функция определения кол-ва соседей с учетом поверхности Тора
    def near(self, cell, system=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]):
        y, x = cell
        count = 0
        for i in system:
            if self.active_cells[(y + i[0]) % len(self.active_cells)][(x + i[1]) % len(self.active_cells[0])]:
                count += 1
        return count

    def next_move(self):
        restart = 0
        cells2 = [[0 for x in range(len(self.active_cells[0]))] for y in range(len(self.active_cells))]
        for y in range(len(cells2)):
            for x in range(len(cells2[0])):
                neighbours_count = self.near([y, x])
                if self.active_cells[y][x]:
                    if neighbours_count not in (2, 3):
                        cells2[y][x] = 0
                        restart = 1
                        continue
                    cells2[y][x] = 1
                    continue
                if neighbours_count == 3:
                    cells2[y][x] = 1
                    restart = 1
                    continue
                cells2[y][x] = 0
        self.active_cells = cells2
        self.current_state = restart

    def render(self, screen):
        if self.current_state == 1:
            self.next_move()
        black_color = pygame.Color(BLACK)
        white_color = pygame.Color(WHITE)
        green_color = pygame.Color(GREEN)
        screen.fill(black_color)
        for cell_data in self.cells:
            pygame.draw.rect(screen, white_color, cell_data[0], 1)
            fill_rect = pygame.Rect(
                (cell_data[0].left + 2, cell_data[0].top + 2, self.cell_size - 2, self.cell_size - 2))
            col = cell_data[2][0]
            row = cell_data[2][1]
            if self.active_cells[row][col] == 1:
                screen.fill(rect=fill_rect, color=green_color)
        pygame.display.update()

    def run_or_stop(self):
        if self.current_state == 0:
            self.current_state = 1
        else:
            self.current_state = 0

    def get_status(self):
        return self.current_state


def main():
    cell_size = 22
    cols = 18
    rows = 18
    padding = 25
    pygame.init()
    clock = pygame.time.Clock()
    fps = 5
    width = padding + cell_size * cols + padding
    heigth = padding + cell_size * rows + padding
    size = width, heigth
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Жизнь на Торе')
    life = Life(cols, rows)
    life.set_view(padding, padding, cell_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and life.get_status() == 0:
                    life.get_click(event.pos)
                elif event.button == 3:
                    life.run_or_stop()
                elif event.button == 4 and life.get_status() == 1:
                    if fps <= 9:
                        fps += 1
                elif event.button == 5 and life.get_status() == 1:
                    if fps >= 2:
                        fps -= 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                life.run_or_stop()
        life.render(screen)
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
