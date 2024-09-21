import pygame
import time

pygame.init()


window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Тестовый проект")

image1 = pygame.image.load("pic_python.png")
image_rect1 = image1.get_rect()

image2 = pygame.image.load("arrow.png")
image_rect2 = image2.get_rect()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if event.type ==pygame.MOUSEMOTION:
        mouseX, mouseY = pygame.mouse.get_pos()
        image_rect1.x = mouseX - 50
        image_rect1.y = mouseY - 50

    if image_rect1.colliderect(image_rect2):
        print("Произошло столкновение")
        time.sleep(1)

    screen.fill((100, 50, 50))
    screen.blit(image1, image_rect1)
    screen.blit(image2, image_rect2)
    pygame.display.flip()

pygame.QUIT