import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# プレイヤー画像読み込み（仮）
player_img = pygame.image.load("player1.png")

x = 100
y = 400
vy = 0
gravity = 1
jump_power = -15
on_ground = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
            vy = jump_power
            on_ground = False

    vy += gravity
    y += vy
    if y >= 400:
        y = 400
        vy = 0
        on_ground = True

    screen.fill((135, 206, 235))
    screen.blit(player_img, (x, y))
    pygame.display.flip()
    clock.tick(60)
