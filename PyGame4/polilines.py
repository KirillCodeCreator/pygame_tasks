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
        self.old = list()
        self.w = len(board[0])
        self.h = len(board)
        self.map = self.read_map(board)
        self.wayMap = [[0 for j in range(len(board[0]))] for i in range(len(board[0]))]
        self.clock = pygame.time.Clock()

    def read_map(self, board):
        map = [[0 for j in range(self.w)] for i in range(self.h)]
        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if board[row][col] != 1:
                    map[row][col] = 0
                else:
                    map[row][col] = 1
        return map

    def FindWave(self, x1, y1, x2, y2):
        add = True
        cMap = [[0 for j in range(self.w)] for i in range(self.h)]
        x = y = step = 0
        for y in range (self.h):
            for x in range (self.w):
                if self.map[y][x] == 1:
                    cMap[y][x] = -2; #индикатор стены
                else:
                    cMap[y][x] = -1; #индикатор еще не ступали сюда
        cMap[y2][x2] = 0 #Начинаем с финиша
        while add == True:
            add = False
            for y in range(self.h):
                for x in range(self.w):
                    if cMap[x][y] == step: #Ставим значение шага+1 в соседние ячейки (если они проходимы)
                        if y - 1 >= 0 and cMap[x - 1][y] != -2 and cMap[x - 1][y] == -1:
                            cMap[x - 1][y] = step + 1
                        if x - 1 >= 0 and cMap[x][y - 1] != -2 and cMap[x][y - 1] == -1:
                            cMap[x][y - 1] = step + 1
                        if y + 1 < self.w and cMap[x + 1][y] != -2 and cMap[x + 1][y] == -1:
                            cMap[x + 1][y] = step + 1
                        if x + 1 < self.h and cMap[x][y + 1] != -2 and cMap[x][y + 1] == -1:
                            cMap[x][y + 1] = step + 1
            step += 1
            add = True
            if cMap[y1][x1] != -1: #решение найдено
                add = False
            if step > self.w * self.h: #решение не найдено
                add = False

class PathAlgoritm:

    def __init__(self, board):
        self.old = list()
        self.board = board
        self.path = list()
        self.clock = pygame.time.Clock()
        self.step = 0
        self.max_step = len(board) * len(board[0])

    def get_path(self, start, to):
        self.step += 1
        if self.step > self.max_step:  # решение не найдено
            return False
        print(F'add to path {start}')
        self.path.append(start)
        self.old.append(start)
        neighbours = self.get_neighbours(start)
        if len(neighbours) == 0:
            print(F'clear path')
            return False
        if to in neighbours:
            self.path.append(to)
            print(F'get path')
            x, y = to
            return True
        else:
            for cell in neighbours:
                x, y = cell
                if self.board[y][x] == 0 and self.get_path(cell, to):
                    return True
        print(F'clear path')
        return False

    def get_neighbours(self, cell):
        x, y = cell
        possible_neighbours = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]
        real_neighbours = []
        for cell in possible_neighbours:
            if 0 <= cell[0] < len(self.board):
                if 0 <= cell[1] < len(self.board[0]):
                    if cell in self.old:
                        continue
                    real_neighbours.append(cell)
        return real_neighbours

class PathAlgoritm2:

    def __init__(self, board):
        self.old = list()
        self.w = len(board[0])
        self.h = len(board)
        self.map = self.read_map(board)
        self.path = list()
        self.clock = pygame.time.Clock()
        self.step = 0
        self.max_step = len(board) * len(board[0])
        print('========start===============')

    def read_map(self, board):
        map = [[0 for j in range(self.h)] for i in range(self.w)]
        for row in range(0, self.h):
            for col in range(0, self.w):
                if board[row][col] != 1:
                    map[row][col] = 0
                else:
                    map[row][col] = 1
        return map

    def get_path(self, start, to):
        if self.step == 0:
            print(f"from {start} to {to}")
        else:
            self.path.append(start)
            print(F'add to path {start}')
        if self.step > self.max_step:  # решение не найдено
            return False
        self.step += 1
        self.old.append(start)
        if start == to: #прибыли в точку назначения
            print('finish')
            return True
        x = y = -1
        if start[0] - to[0] == 0 and start[1] - to[1] > 0: # на одной оси x и вверх по y
            x, y = (start[0] , start[1] - 1)
        elif start[0] - to[0] == 0 and start[1] - to[1] < 0: # на одной оси x и вниз по y
            x, y = (start[0] , start[1] + 1)
        elif start[1] - to[1] == 0 and start[0] - to[0] > 0:
            x, y = (start[0] - 1, start[1])
        elif start[1] - to[1] == 0 and start[0] - to[0] < 0:
            x, y = (start[0] + 1, start[1])

        if x != -1 and y != -1 and self.map[y][x] == 0:
            if self.get_path((x, y), to):
                return True
        else:
            neighbours = self.get_neighbours(start)
            if len(neighbours) == 0:
                print('not found neighbours')
                return False
            print(F'found neighbours {neighbours}')
            for cell in neighbours:
                x, y = cell
                if self.map[y][x] == 0 and self.get_path(cell, to):
                    return True
                    print(F'found next path point {cell}')
            return False

    def get_neighbours(self, cell):
        x, y = cell
        possible_neighbours = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]
        if possible_neighbours in self.old:
            for i in possible_neighbours:
                self.old.remove(i)
        real_neighbours = []
        for cell in possible_neighbours:
            if 0 <= cell[0] < self.w:
                if 0 <= cell[1] < self.h:
                    if cell in self.old or self.map[cell[1]][cell[0]] == 1:
                        continue
                    real_neighbours.append(cell)
        return real_neighbours

class Lines(Board):
    red_circle_col = -1
    red_circle_row = -1

    def __init__(self, width, height):
        super().__init__(width, height)
        self.active_cells = [[0 for j in range(width)] for i in range(height)]
        self.points = list()
        self.prev_point = None
        self.clock = pygame.time.Clock()
        self.fps = 2

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
        alg.FindWave(x1, y1, x2, y2)
        #alg = PathAlgoritm2(self.active_cells)
        #if alg.get_path((x1, y1), (x2, y2)):
            #return alg.path
        #else:
            #return None

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
            elif self.active_cells[row][col] == 8:
                pygame.draw.circle(screen, white_color, cell_data[0].center, 16)
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
