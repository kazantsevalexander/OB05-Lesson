import pygame
import random

# Инициализация Pygame
pygame.init()

# Определяем размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Класс для ракетки
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 30
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# Класс для мяча
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Отскок от стен
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

# Класс для блоков
class Block:
    def __init__(self, x, y):
        self.width = 75
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()

    # Создаем объекты игры
    paddle = Paddle()
    ball = Ball()

    # Создаем блоки
    blocks = []
    for i in range(6):
        for j in range(8):
            block = Block(j * 80 + 10, i * 30 + 10)
            blocks.append(block)

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Движение ракетки и мяча
        paddle.move()
        ball.move()

        # Отскок от ракетки
        if ball.rect.colliderect(paddle.rect):
            ball.dy = -ball.dy

        # Отскок от блоков
        for block in blocks[:]:
            if ball.rect.colliderect(block.rect):
                ball.dy = -ball.dy
                blocks.remove(block)

        # Проверка проигрыша
        if ball.rect.bottom >= SCREEN_HEIGHT:
            running = False

        # Отрисовка всех элементов
        paddle.draw(screen)
        ball.draw(screen)
        for block in blocks:
            block.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
