import pygame
import random
import sys

# Pygameの初期化
pygame.init()

# 画面の大きさ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("テトリス")

# 日本語フォントのパス
font_path = "C:/Windows/Fonts/meiryo.ttc"  # Windowsの例

# 日本語対応のフォントをロード
japanese_font = pygame.font.Font(font_path, 36)

#ゲーム画面の大きさ
GAME_WIDTH = 10
GAME_HEIGHT = 20


# ブロックのサイズ
BLOCK_SIZE = 30

# ゲーム画面のオフセット
GAME_OFFSET_X = (SCREEN_WIDTH - GAME_WIDTH * BLOCK_SIZE) // 2
GAME_OFFSET_Y = (SCREEN_HEIGHT - GAME_HEIGHT * BLOCK_SIZE) // 2


# ブロックが落下する間隔（秒）
fall_time = 0.0# 2秒ごとにブロックを落下させる
last_fall_time = pygame.time.get_ticks()  # 最後にブロックが落下した時刻

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# フォントの初期化
font = pygame.font.Font(None, 36)

# テトリミノの形状を定義
tetrominoes = [
    [(1, 1, 1, 1)],
    [(1, 1), (1, 1)],
    [(1, 1, 0), (0, 1, 1)],
    [(0, 1, 1), (1, 1, 0)],
    [(1, 1, 1), (0, 1, 0)],
    [(1, 1, 1), (0, 0, 1)],
    [(0, 1, 0), (1, 1, 1)]
]

# テトリミノの色
tetromino_colors = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (255, 165, 0),  # Orange for S
    (0, 0, 255),    # Blue for Z
    (0, 255, 0),    # Green for T
    (255, 0, 0),    # Red for J
    (128, 0, 128)   # Purple for L
]

# 初期位置
x, y = 3, 5

# 現在のテトリミノ
current_tetromino = random.choice(tetrominoes)
current_color = random.choice(tetromino_colors)

# 次のテトリミノ
next_tetromino = random.choice(tetrominoes)
next_color = random.choice(tetromino_colors)

# ブロックの配置を記録する配列
board = [[0] * GAME_WIDTH for _ in range(GAME_HEIGHT)]

# 前回のスコアを保持する変数
last_score = 0

# ゲーム開始時刻
start_time = pygame.time.get_ticks()

# 衝突判定
def check_collision(x, y, tetromino):
    for dx, row in enumerate(tetromino):
        for dy, cell in enumerate(row):
            if cell != 0:
                if (x + dy >= GAME_WIDTH or
                        y + dx >= GAME_HEIGHT or
                        x + dy < 0 or
                        board[y + dx][x + dy] != 0):
                    return True
    return False

# テトリミノをボードに固定
def place_tetromino(x, y, tetromino, color):
    for dx, row in enumerate(tetromino):
        for dy, cell in enumerate(row):
            if cell != 0:
                board[y + dx][x + dy] = color

# ゲームオーバー判定
def check_game_over():
    return any(cell != 0 for cell in board[0])

# ゲームループ
running = True
clock = pygame.time.Clock()
speed = 0.5
score = 0

# ブロックが回転する間隔（秒）
change_time = 3.0
last_change_time = pygame.time.get_ticks()  # 最後にブロックが回転した時刻

# 新しい変数を追加
drop = False
rotate = True

# ゲーム開始時のタイマー設定（2分間）
GAME_DURATION = 120000  # 2分間をミリ秒単位で設定
game_start_time = pygame.time.get_ticks()  # ゲーム開始時刻を取得

# ブロックの回転
def rotate_tetromino(tetromino):
    return [list(x)[::-1] for x in zip(*tetromino)]

def rotate_tetromino_left(tetromino):
    # テトリミノを転置（行と列を入れ替える）
    transposed = [list(x) for x in zip(*tetromino)]
    # 各行を逆順にして左回転させる
    return [row[::-1] for row in transposed]

def rotate_tetromino_right(tetromino):
    # テトリミノを転置（行と列を入れ替える）
    transposed = [list(x) for x in zip(*tetromino)]
    # 各列を逆順にして右回転させる
    return transposed[::-1]

# ゲームをリセットする関数
def reset_game():
    global board, current_tetromino, current_color, next_tetromino, next_color, x, y, score, last_fall_time, game_over, running,  last_score
    last_score = score  # 現在のスコアを last_score に保存
    board = [[0] * GAME_WIDTH for _ in range(GAME_HEIGHT)]
    current_tetromino = random.choice(tetrominoes)
    current_color = random.choice(tetromino_colors)
    next_tetromino = random.choice(tetrominoes)
    next_color = random.choice(tetromino_colors)
    x, y = 3, 0
    score = 0
    last_fall_time = pygame.time.get_ticks()
    game_over = False
    running = True  # グローバル変数の running を True に設定

# ゲームループ
while running:
    screen.fill((255, 255, 255))  # 画面を白で塗りつぶす
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            if event.key == pygame.K_RETURN:  # Enterキーが押されたとき
                last_fall_time = current_time  # 最後にブロックが落下した時刻を更新
                drop = True
                rotate = False
            else:
                if rotate:
                    if event.key == pygame.K_UP:
                        current_tetromino = rotate_tetromino_left(current_tetromino)
                    elif event.key == pygame.K_DOWN:
                        current_tetromino = rotate_tetromino_right(current_tetromino)
                if event.key == pygame.K_RIGHT:  # 右矢印キーが押されたとき
                    if not check_collision(x + 1, y, current_tetromino):  # 壁や他のブロックとの衝突を確認
                        x += 1
                elif event.key == pygame.K_LEFT:  # 左矢印キーが押されたとき
                    if not check_collision(x - 1, y, current_tetromino):  # 壁や他のブロックとの衝突を確認
                        x -= 1

    # 残り時間の計算
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - game_start_time  # 経過時間を計算
    remaining_time = max(GAME_DURATION - elapsed_time, 0)  # 残り時間を計算（0未満にならないようにする）


    current_time = pygame.time.get_ticks()  # 現在の時刻を取得
    if drop and current_time - last_fall_time > fall_time * 1000:  # 一定時間が経過したかをチェック
        if not check_collision(x, y + 1, current_tetromino):
            y += 1
        else:
            place_tetromino(x, y, current_tetromino, current_color)
            x, y = 3, 0
            current_tetromino = next_tetromino
            current_color = next_color
            next_tetromino = random.choice(tetrominoes)
            next_color = random.choice(tetromino_colors)
            last_fall_time = current_time  # 最後にブロックが落下した時刻を更新
            drop = False
            rotate = True
            if check_game_over():
                game_over = True

            # 行が全部埋まったら消す
            for i, row in enumerate(board):
                if all(cell != 0 for cell in row):
                    del board[i]
                    board.insert(0, [0] * GAME_WIDTH)
                    score += 100
                
    # ブロックの枠線の色と幅を定義
    BLOCK_BORDER_COLOR = (0, 0, 0)  # Black
    BLOCK_BORDER_WIDTH = 2

    # テトリミノを描画
    for dx, row in enumerate(current_tetromino):
        for dy, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(screen, current_color,
                                (GAME_OFFSET_X + x * BLOCK_SIZE + dy * BLOCK_SIZE,
                                GAME_OFFSET_Y + y * BLOCK_SIZE + dx * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLOCK_BORDER_COLOR,
                                (GAME_OFFSET_X + x * BLOCK_SIZE + dy * BLOCK_SIZE,
                                GAME_OFFSET_Y + y * BLOCK_SIZE + dx * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE), BLOCK_BORDER_WIDTH)

    # ボード上の固定されたブロックを描画

    for row in range(GAME_HEIGHT):
        for col in range(GAME_WIDTH):
            if board[row][col] != 0:
                pygame.draw.rect(screen, board[row][col],
                                (GAME_OFFSET_X + col * BLOCK_SIZE, 
                                GAME_OFFSET_Y + row * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLOCK_BORDER_COLOR,
                                (GAME_OFFSET_X + col * BLOCK_SIZE, 
                                GAME_OFFSET_Y + row * BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE), BLOCK_BORDER_WIDTH)

    # 残り時間の表示
    minutes = remaining_time // 60000  # 分単位
    seconds = (remaining_time % 60000) // 1000  # 秒単位
    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))  # スコアの上に表示

    # スコア表示
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))  # スコアの位置を下にずらして表示

    # 前回のスコア表示（2回目以降のゲーム画面上に表示）
    if last_score != 0:  # 前回のスコアが0でない場合のみ表示
        last_score_text = font.render(f"Last Score: {last_score}", True, (0, 0, 0))
        screen.blit(last_score_text, (10, 90))  # スコアの下に表示

    # 次のテトリミノを描画
    margin_x, margin_y = 2, 2 # マージンを設定
    tetromino_width = len(next_tetromino[0])  # テトリミノの幅を取得
    small_block_size = BLOCK_SIZE // 2  # ブロックサイズを半分にする
    for dx, row in enumerate(next_tetromino):
        for dy, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(screen, next_color,
                                (SCREEN_WIDTH - (margin_x + tetromino_width - dy) * small_block_size,
                                (dx + margin_y) * small_block_size, small_block_size, small_block_size))

    # フォントの設定
    font = pygame.font.Font(None, 24)

    # テキストを描画
    text = font.render("Next Block:", True, (0, 0, 0))

    # テキストを画面に描画
    screen.blit(text, (SCREEN_WIDTH - (margin_x + tetromino_width) * BLOCK_SIZE, 0))

    # 境界線の描画
    BORDER_COLOR = (230, 230,230)  # black
    BORDER_WIDTH = 2

    # 右側の境界線の描画
    game_screen_width = GAME_OFFSET_X + GAME_WIDTH * BLOCK_SIZE
    pygame.draw.line(screen, BORDER_COLOR, (game_screen_width, 0), (game_screen_width, SCREEN_HEIGHT), BORDER_WIDTH)
    
    # 左側の境界線の描画
    pygame.draw.line(screen, BORDER_COLOR, (GAME_OFFSET_X, 0), (GAME_OFFSET_X, SCREEN_HEIGHT), BORDER_WIDTH)

    # ゲームスクリーン内の升目を描画
    GRID_COLOR = (230, 230, 230)  # Gray color
    for i in range(GAME_WIDTH):
        pygame.draw.line(screen, GRID_COLOR, 
                        (GAME_OFFSET_X + i * BLOCK_SIZE, GAME_OFFSET_Y), 
                        (GAME_OFFSET_X + i * BLOCK_SIZE, GAME_OFFSET_Y + GAME_HEIGHT * BLOCK_SIZE), 
                        BORDER_WIDTH)
    for i in range(GAME_HEIGHT):
        pygame.draw.line(screen, GRID_COLOR, 
                        (GAME_OFFSET_X, GAME_OFFSET_Y + i * BLOCK_SIZE), 
                        (GAME_OFFSET_X + GAME_WIDTH * BLOCK_SIZE, GAME_OFFSET_Y + i * BLOCK_SIZE), 
                        BORDER_WIDTH)
    #画面の更新
    pygame.display.flip()

    # 残り時間が0になったらゲームオーバーかクリアかを判別
    if remaining_time == 0:
        running = False
        game_over = True
        if score >= 1000:
            # スコアが1000以上でクリア条件を満たしている場合
            clear = True
        else:
            # スコアが1000未満でゲームオーバーの場合
            clear = False

        # ゲームオーバー判定
    if check_game_over():
        running = False
        game_over = True  # ゲームオーバーフラグを追加
    else:
        game_over = False

    # ゲームオーバー時の処理
    if game_over:
        # クリア条件のチェック（スコアが1000以上で、残り時間が0）
        if clear:
            # クリア画面の表示
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)  # 半透明度を設定（0〜255）
            overlay.fill((0, 0, 0))  # 黒色で塗りつぶし
            screen.blit(overlay, (0, 0))  # オーバーレイを画面に描画

            # クリアテキストのフォントサイズを大きくする
            clear_font = pygame.font.Font(None, 72)  # フォントサイズを72に設定

            # クリアテキストを描画（影付き）
            clear_text = clear_font.render("CLEAR!", True, (0, 0, 128))  # 青色でテキストを設定
            text_rect = clear_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(clear_text, text_rect)  # テキストを描画

        else:
            # 半透明のオーバーレイを描画
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)  # 半透明度を設定（0〜255）
            overlay.fill((0, 0, 0))  # 黒色で塗りつぶし
            screen.blit(overlay, (0, 0))  # オーバーレイを画面に描画

            # ゲームオーバーテキストのフォントサイズを大きくする
            game_over_font = pygame.font.Font(None, 72)  # フォントサイズを72に設定
            score_font = pygame.font.Font(None, 48)  # スコアのフォントサイズを48に設定

            # ゲームオーバーテキストを描画（影付き）
            game_over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 - 50 + 2))
            screen.blit(game_over_text, text_rect)  # 影を描画

            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(game_over_text, text_rect)  # テキストを描画

        # スコアテキストを描画
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(score_text, score_rect)

    
    # 画面の更新
    pygame.display.flip()

    # 「Enterキーを押してリトライ」というメッセージを表示（日本語フォント使用）
    retry_text = japanese_font.render("Enterキーを押してリトライ", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    screen.blit(retry_text, retry_rect)

    # 画面の更新
    pygame.display.flip()

    # プレイヤーの入力を待つ
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESCキーが押されたら終了
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:  # Enterキーが押されたらゲームをリセット
                    reset_game()
                    waiting_for_input = False

    running = True
    clock.tick(60)

    # 画面の更新
    pygame.display.flip()

pygame.quit()
sys.exit()

# 試していないので編集（追加して）試すところからスタート