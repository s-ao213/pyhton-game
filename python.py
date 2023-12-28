import pygame
pygame.init()

# ゲーム画面の大きさ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# pygameの初期化
pygame.init()

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面を白で塗りつぶす
    screen.fill((255, 255, 255))

    # 画面を更新
    pygame.display.flip()

pygame.quit()

# テトリミノの形状を定義
tetrominoes = [
    [(1, 1, 1, 1)],
    [(1, 1), (1, 1)],
    [(1, 1, 0), (0, 1, 1)],
    [(0, 1, 1), (1, 1)],
    [(1, 1, 1), (0, 1, 0)],
    [(1, 1, 1), (1)],
    [(1, 1, 1, 1), (0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0)]
]

# テトリミノの初期位置
x, y = 0, 0

# ゲームループ
while running:

    # キーボードの入力を検出
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_RIGHT]:
        x += 1

    # 時間経過でテトリミノを下に移動
    y += 1

    # ブロックの配置を記録する配列
board = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]

# 衝突判定
def check_collision(x, y, tetromino):
    for dx, row in enumerate(tetromino):
        for dy, cell in enumerate(row):
            if cell != 0 and (x + dx < 0 or x + dx >= SCREEN_WIDTH or y + dy < 0 or y + dy >= SCREEN_HEIGHT or board[y+dy][x+dx] != 0):
                return True
    return False

# ゲームループ
while running:

# 衝突判定
    if check_collision(x, y, tetrominoes[0]):
        x, y = 0, 0  # テトリミノの位置をリセット

# ゲームオーバー判定
if any(cell != 0 for cell in board[0]):
    running = False

# ゲームの進行速度
speed = 0.5
clock = pygame.time.Clock()

# ゲームループ
while running:
    # 時間経過でテトリミノを下に移動
    if pygame.time.get_ticks() / 1000 > speed:
        y += 1
        pygame.time.set_ticks(0)
    
    clock.tick(60)

# スコア
score = 0
pygame.init()
font = pygame.font.Font(None, 36)


# 行が全部埋まったら消す
for y, row in enumerate(board):
    if all(cell != 0 for cell in row):
        del board[y]
        board.insert(0, [0] * SCREEN_WIDTH)
        score += 100

# スコア表示

score_text = font.render(f"Score: {score}", True, (0, 0, 0))
screen.blit(score_text, (10, 10))

pygame.quit()
# プレビューテトリミノ
preview_tetromino = random.choice(tetrominoes)

# プレビュー表示
for dx, row in enumerate(preview_tetromino):
    for dy, cell in enumerate(row):
        if cell != 0:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH + dx * 30, 100 + dy * 30, 30, 30))

# ゲームオーバー

判定
if any(cell != 0 for cell in board[0]):
    running = False

# ゲームオーバー画面
while not running:
    screen.fill((255, 255, 255))
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            board = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]  # ボードをリセット
            running = True  # ゲームを
