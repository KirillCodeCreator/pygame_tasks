import pygame

WHITE = (255, 255, 255)


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
                cell_data = (rect, (x, y))
                self.cells.append(cell_data)

    def render(self, screen):
        border_color = pygame.Color(WHITE)
        for cell_data in self.cells:
            pygame.draw.rect(screen, border_color, cell_data[0], 1)

    def on_click(self, cell):
        x, y = cell[0] - self.left, cell[1] - self.top
        row, col = y // self.cell_size, x // self.cell_size
        if col >= 0 and col < self.width and row >= 0 and row < self.height:
            print(f"({col}, {row})")
        else:
            print("None")

    def get_click(self, mouse_pos):
        cell = (mouse_pos[0], mouse_pos[1])
        self.on_click(cell)


def start():
    length = 375
    width = 450
    pygame.init()
    size = length + 25, width + 25
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Координаты клетки")
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


if __name__ == "__main__":
    start()
