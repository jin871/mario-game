


import qrcode

# ここに公開予定のURLを入力（仮の例）
url = "https://jin.github.io/mario-game"

# QRコード生成
qr = qrcode.make(url)

# 保存（ファイル名は自由に）
qr.save("mario_game_qr.png")

# 画像を表示（オプション）
qr.show()

import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("マリオ風ゲーム（画像不要版）")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 色
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)

# サウンド（なければコメントアウトしてOK）
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
    coin_sound = pygame.mixer.Sound("coin.wav")
    gameover_sound = pygame.mixer.Sound("gameover.wav")
except:
    jump_sound = coin_sound = gameover_sound = None

# マップ定義（C = コイン, E = 敵）
level_map = [
    "                                                                                          ",
    "                                                                                          ",
    "              C       C       C              C       C       C              C       C     ",
    "         B           C     B     C     B          B     C     B     C     B          C    ",
    "        B     C          B    C      B     C     B    C     B    C      B      C     B     ",
    "   B        B     B      BB   E    B       B     E      BB    B     B      B    E         ",
    "=========================================================================================="
]


player = pygame.Rect(100, 300, 40, 50)
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = False
camera_x = 0

world = []
enemies = []
coins = []
score = 0

# ワールド生成
def generate_world():
    for row_idx, row in enumerate(level_map):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile in ('=', 'B'):
                world.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 'E':
                enemies.append([pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 2])
            elif tile == 'C':
                coins.append(pygame.Rect(x, y, TILE_SIZE // 2, TILE_SIZE // 2))

generate_world()

# メインループ
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power
        if jump_sound:
            jump_sound.play()
        on_ground = False

    velocity_y += gravity
    player.y += velocity_y

    on_ground = False
    for block in world:
        if player.colliderect(block):
            if velocity_y > 0:
                player.bottom = block.top
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0:
                player.top = block.bottom
                velocity_y = 0

    # 敵の移動と衝突処理
    for enemy in enemies:
        enemy_rect, speed = enemy
        enemy_rect.x += speed
        for block in world:
            if enemy_rect.colliderect(block):
                enemy[1] *= -1
                enemy_rect.x += enemy[1] * 2
        if player.colliderect(enemy_rect):
            if gameover_sound:
                gameover_sound.play()
            print("ゲームオーバー！")
            pygame.quit()
            sys.exit()

    # コイン回収処理
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10
            if coin_sound:
                coin_sound.play()

    camera_x = player.x - WIDTH // 2

    # 描画
    for block in world:
        pygame.draw.rect(screen, BROWN, pygame.Rect(block.x - camera_x, block.y, TILE_SIZE, TILE_SIZE))

    for enemy in enemies:
        pygame.draw.rect(screen, RED, pygame.Rect(enemy[0].x - camera_x, enemy[0].y, TILE_SIZE, TILE_SIZE))

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin.x - camera_x + 10, coin.y + 10), 10)

    # プレイヤー描画（四角形）
    pygame.draw.rect(screen, BLUE, pygame.Rect(player.x - camera_x, player.y, player.width, player.height))

    # スコア表示
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)