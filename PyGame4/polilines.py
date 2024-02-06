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

class WaveAlgoritm:
    def __init__(self, board):
        self.w = len(board[0])
        self.h = len(board)
        self.px = [0] * self.w * self.h
        self.py = [0] * self.h * self.w
        self.wall = -1
        self.blank = -2
        self.len = 0
        self.grid = self.create_map(board)
        self.clock = pygame.time.Clock()

    def create_map(self, board):
        map = [[0 for j in range(self.w)] for i in range(self.h)]
        for y in range(0, self.h):
            for x in range(0, self.w):
                if board[y][x] != 1:
                    map[y][x] = self.blank
                else:
                    map[y][x] = self.wall
        return map

    def get_neighbours(self, y, x, value):
        possible_neighbours = [
            (y, x - 1),
            (y, x + 1),
            (y - 1, x),
            (y + 1, x)
        ]
        real_neighbours = []
        for cell in possible_neighbours:
            iy, ix = cell
            if 0 <= iy < self.h and 0 <= ix < self.w and self.grid[iy][ix] == value:
                    real_neighbours.append(cell)
        return real_neighbours

    def find_wave(self, ax, ay, bx, by):
        dx = [1, 0, -1, 0]   #смещения, соответствующие соседям ячейки
        dy = [0, 1, 0, -1];   #справа, снизу, слева и сверху
        stop = False

        if self.grid[ay][ax] == self.wall or self.grid[by][bx] == self.wall: #ячейка (ax, ay) или (bx, by) - стена
            return False
        step = 0
        self.grid[ay][ax] = step #стартовая ячейка помечена 0
        while stop == False and self.grid[by][bx] == self.blank:
            stop = True #предполагаем, что все свободные клетки уже помечены
            for y in range(0, self.h):
                for x in range(0, self.w):
                    if self.grid[y][x] == step:    #ячейка (x, y) помечена числом d
                        neighbours = self.get_neighbours(y, x, self.blank)
                        for cell in neighbours:  # проходим по всем непомеченным соседям
                            iy, ix = cell
                            stop = False #найдены непомеченные клетки
                            self.grid[iy][ix] = step + 1 #распространяем волну
            step += 1
        if self.grid[by][bx] == self.blank:
            return False #путь не найден
        self.len = self.grid[by][bx] #длина кратчайшего пути из(ax, ay) в (bx, by)
        x = bx
        y = by
        d = self.len
        while d > 0:
            self.px[d] = x
            self.py[d] = y
            d -= 1
            neighbours = self.get_neighbours(y, x, d)
            for cell in neighbours:  # проходим по всем непомеченным соседям
                iy, ix = cell
                if self.grid[iy][ix] == d:
                    x = ix
                    y = iy #переходим в ячейку, которая на 1 ближе к старту
                    break
        self.px[0] = ax
        self.py[0] = ay #теперь px[0..len] и py[0..len] - координаты ячеек пути
        return True

class Lines(Board):
    red_circle_col = -1
    red_circle_row = -1

    def __init__(self, width, height):
        super().__init__(width, height)
        self.active_cells = [[0 for j in range(width)] for i in range(height)]
        self.points = list()
        self.prev_point = None
        self.clock = pygame.time.Clock()
        self.fps = 4

    def is_red_circle(self, row, col):
        return self.active_cells[row][col] == 2

    def is_blue_circle(self, row, col):
        return self.active_cells[row][col] == 1

    def is_empty_cell(self, row, col):
        return self.active_cells[row][col] == 0

    def exists_red_circle(self):
        return self.red_circle_col > -1 and self.red_circle_row > -1

    def create_red_circle(self, row, col):
        self.active_cells[row][col] = 2
        self.red_circle_col = col
        self.red_circle_row = row

    def create_blue_circle(self, row, col):
        self.active_cells[row][col] = 1

    def create_white_circle(self, row, col):
        self.active_cells[row][col] = 8

    def delete_circle(self, row, col):
        if self.is_red_circle(row, col):
            self.red_circle_col = -1
            self.red_circle_row = -1
        self.active_cells[row][col] = 0

    def create_circle(self, row, col):
        if self.is_empty_cell(row, col):
            if self.exists_red_circle():
                path = self.has_path(self.red_circle_col, self.red_circle_row, col, row)
                if path is not None:
                    self.delete_circle(self.red_circle_row, self.red_circle_col)
                    self.points.clear()
                    for i in path:
                        self.points.append(i)
            else:
                self.points.clear()
                self.create_blue_circle(row, col)
        elif self.is_blue_circle(row, col):
            self.create_red_circle(row, col)
        elif self.is_red_circle(row, col):
            self.delete_circle(row, col)
            self.create_blue_circle(row, col)

    def show_next_path_point(self):
        if self.prev_point is not None:
            c, r = self.prev_point
            self.delete_circle(r, c)
        self.prev_point = self.points[0]
        col, row = self.points[0]
        self.points.remove(self.prev_point)
        self.create_blue_circle(row, col)
        self.clock.tick(self.fps)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return
        self.create_circle(row, col)

    def has_path(self, x1, y1, x2, y2):
        alg = WaveAlgoritm(self.active_cells)
        if alg.find_wave(x1, y1, x2, y2):
            points = list()
            for i in range(1, alg.len):
                points.append((alg.px[i], alg.py[i]))
            points.append((x2, y2))
            return points
        else:
            return None

    def render(self, screen):
        black_color = pygame.Color(BLACK)
        white_color = pygame.Color(WHITE)
        blue_color = pygame.Color(BLUE)
        red_color = pygame.Color(RED)
        screen.fill(black_color)
        if len(self.points) > 0:
            self.show_next_path_point()
        for cell_data in self.cells:
            col = cell_data[2][0]
            row = cell_data[2][1]
            if self.active_cells[row][col] == 1:
                pygame.draw.circle(screen, blue_color, cell_data[0].center, 16)
            elif self.active_cells[row][col] == 2:
                pygame.draw.circle(screen, red_color, cell_data[0].center, 16)
            pygame.draw.rect(screen, white_color, cell_data[0], 1)
        pygame.display.update()


def main():
    cell_size = 35
    cols = 10
    rows = 10
    padding = 25
    pygame.init()
    width = padding + cell_size * cols + padding
    heigth = padding + cell_size * rows + padding
    size = width, heigth
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Полилинии')
    lines = Lines(cols, rows)
    lines.set_view(padding, padding, cell_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                lines.get_click(event.pos)
        lines.render(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
