import pygame

from Board.board5 import Board

WHITE = (255, 255, 255)
BLUE = (0, 0, 255, 0)
GREEN = (0, 255, 0, 0)
BLACK = (0, 0, 0)


class Life(Board):
    current_state = 0

    def __init__(self, width, height):
        super().__init__(width, height)
        self.active_cells = [[0 for j in range(width)] for i in range(height)]

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

    # Функция определения кол-ва соседей
    def near(self, system):
        count = 0
        for idx in system:
            if self.active_cells[idx[0]][idx[1]]:
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

    def next_move(self):
        restart = 0
        cells2 = [[0 for j in range(len(self.active_cells[0]))] for i in range(len(self.active_cells))]
        for i in range(len(cells2)):
            for j in range(len(cells2)):
                neighbours = self.get_neighbours((i, j))
                count = self.near(neighbours)
                if self.active_cells[i][j]:
                    if count not in (2, 3):
                        cells2[i][j] = 0
                        restart = 1
                        continue
                    cells2[i][j] = 1
                    continue
                if count == 3:
                    cells2[i][j] = 1
                    restart = 1
                    continue
                cells2[i][j] = 0
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
    cell_size = 15
    cols = 30
    rows = 30
    padding = 25
    pygame.init()
    clock = pygame.time.Clock()
    fps = 5
    width = padding + cell_size * cols + padding
    heigth = padding + cell_size * rows + padding
    size = width, heigth
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра «Жизнь»')
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
