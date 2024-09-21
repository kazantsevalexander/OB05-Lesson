import pygame
import random

# Инициализация Pygame
pygame.init()

# Определяем размеры окна
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Определение размеров блоков
BLOCK_SIZE = 30
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Фигуры Тетриса
TETROMINO_SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

TETROMINO_COLORS = [CYAN, PURPLE, YELLOW, RED, GREEN, ORANGE, BLUE]
DROP_SOUND = pygame.mixer.Sound("drop.mp3")
CLEAR_LINE_SOUND = pygame.mixer.Sound("line.mp3")

# Принцип Single Responsibility - класс отвечает только за движение тетромино
class TetrominoMovement:
    def __init__(self, tetromino, grid):
        self.tetromino = tetromino
        self.grid = grid

    def move(self, dx, dy):
        if self._can_move(dx, dy):
            self.tetromino.x += dx
            self.tetromino.y += dy
        else:
            return False
        return True

    def rotate(self):
        old_shape = self.tetromino.shape
        self.tetromino.rotate()
        if not self._can_move(0, 0):
            self.tetromino.shape = old_shape  # Возврат к старой форме, если вращение невозможно

    def _can_move(self, dx, dy):
        for row in range(len(self.tetromino.shape)):
            for col in range(len(self.tetromino.shape[row])):
                if self.tetromino.shape[row][col]:
                    new_x = self.tetromino.x + col + dx
                    new_y = self.tetromino.y + row + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return False
                    if self.grid.grid[new_y][new_x]:
                        return False
        return True

# Принцип Single Responsibility - класс отвечает только за управление сеткой
class Grid:
    def __init__(self):
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]

    def add_tetromino(self, tetromino):
        for row in range(len(tetromino.shape)):
            for col in range(len(tetromino.shape[row])):
                if tetromino.shape[row][col]:
                    self.grid[tetromino.y + row][tetromino.x + col] = tetromino.color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = ROWS - len(new_grid)
        new_grid = [[0] * COLUMNS for _ in range(cleared_lines)] + new_grid
        self.grid = new_grid
        return cleared_lines

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.grid[row][col]:
                    pygame.draw.rect(screen, self.grid[row][col],
                                     pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Принцип Single Responsibility - класс отвечает только за работу с фигурой
class Tetromino:
    def __init__(self):
        self.shape = random.choice(TETROMINO_SHAPES)
        self.color = random.choice(TETROMINO_COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(screen, self.color,
                                     pygame.Rect((self.x + col) * BLOCK_SIZE, (self.y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Принцип Open/Closed - класс легко расширяется без модификации
class Game:
    def __init__(self):
        self.grid = Grid()
        self.tetromino = Tetromino()
        self.movement = TetrominoMovement(self.tetromino, self.grid)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.is_running = True
        self.fall_speed = 0.1
        self.fall_counter = 0

    def run(self):
        while self.is_running:
            self._handle_events()
            self._update_game()
            self._draw_game()
            pygame.display.flip()
            self.clock.tick(60)

    def _update_game(self):
        self.fall_counter += self.fall_speed
        if self.fall_counter >= 1:
            if not self.movement.move(0, 1):
                DROP_SOUND.play()  # Воспроизведение звука падения
                self.grid.add_tetromino(self.tetromino)
                self.score += self.grid.clear_lines()
                self.tetromino = Tetromino()
                self.movement = TetrominoMovement(self.tetromino, self.grid)
            self.fall_counter = 0

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.movement.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.movement.move(0, 1)  # Ускорение падения фигуры при нажатии клавиши вниз
                elif event.key == pygame.K_UP:
                    self.movement.rotate()


    def _draw_game(self):
        screen.fill(BLACK)
        self.grid.draw(screen)
        self.tetromino.draw(screen)

if __name__ == "__main__":
    Game().run()
    pygame.quit()