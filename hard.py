import pygame
import sys
import math
import time  # Import module time
import threading
import subprocess


# --- Constants ---
BOARD_SIZE = 15
CELL_SIZE = 30
WIDTH, HEIGHT = CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE + 100
LINE_COLOR = (0, 0, 0)
BG_COLOR = (240, 217, 181)
PLAYER = 1
AI = 2
EMPTY = 0
WIN_COUNT = 5
DEPTH = 4  # độ sâu AI
TIME_LIMIT = 15  # Giới hạn thời gian 6 giây
ai_cancelled = False


icon = pygame.image.load("images/image.png")  # Đảm bảo file ảnh có trong thư mục
pygame.display.set_icon(icon)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro AI")
font = pygame.font.SysFont(None, 40)

# --- Game State ---
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False
winner = None
current_turn = PLAYER

#Button
class Button:
    def __init__(self, text, x, y, w, h, callback, bg_color=(70, 130, 180), text_color=(0, 0, 0), hover_color=(100, 160, 210)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)

        txt = font.render(self.text, True, self.text_color)
        text_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()


# --- Drawing --- 
# --- Drawing --- 
def draw_board(last_move=None):
    screen.fill((10, 10, 20))  # Nền tối

    # Vẽ lưới
    for x in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, (50, 50, 60), (x * CELL_SIZE, 0), (x * CELL_SIZE, BOARD_SIZE * CELL_SIZE))
    for y in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, (50, 50, 60), (0, y * CELL_SIZE), (BOARD_SIZE * CELL_SIZE, y * CELL_SIZE))

    # Vẽ các quân cờ
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            cell_value = board[y][x]
            center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            if (y, x) == last_move:
                pygame.draw.rect(screen, (255, 100, 150), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)

            if cell_value == PLAYER:  # O
                pygame.draw.circle(screen, (0, 255, 255), center, CELL_SIZE // 2 - 8, 4)
            elif cell_value == AI:  # X
                offset = CELL_SIZE // 2 - 10
                pygame.draw.line(screen, (255, 77, 77),
                                 (center[0] - offset, center[1] - offset),
                                 (center[0] + offset, center[1] + offset), 4)
                pygame.draw.line(screen, (255, 77, 77),
                                 (center[0] - offset, center[1] + offset),
                                 (center[0] + offset, center[1] - offset), 4)


def draw_piece(row, col):
    cell_value = board[row][col]
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    
    if cell_value == PLAYER:  # O
        pygame.draw.circle(screen, (0, 255, 255), center, CELL_SIZE // 2 - 8, 4)
    elif cell_value == AI:  # X
        offset = CELL_SIZE // 2 - 10
        pygame.draw.line(screen, (255, 77, 77),
                         (center[0] - offset, center[1] - offset),
                         (center[0] + offset, center[1] + offset), 4)
        pygame.draw.line(screen, (255, 77, 77),
                         (center[0] - offset, center[1] + offset),
                         (center[0] + offset, center[1] - offset), 4)



# --- Utility --- 
def is_valid_move(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == EMPTY
def get_candidate_moves():
    candidates = set()
    # Duyệt qua tất cả các ô trên bàn cờ
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:  # Kiểm tra nếu ô hiện tại có quân cờ
                # Duyệt qua các ô xung quanh theo 8 hướng: ngang, dọc và 4 hướng chéo
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), 
                                (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = r + dr, c + dc
                    if is_valid_move(nr, nc):
                        candidates.add((nr, nc))
    # Nếu không tìm thấy candidate nào, trả về tất cả các ô trống trên bàn cờ
    return list(candidates) or [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == EMPTY]





# --- Minimax --- (Cải tiến)
def minimax(depth, alpha, beta, maximizing, start_time):
    if depth == 0:
        return evaluate(), None

    moves = get_candidate_moves()  # Lấy các nước đi khả thi
    best_move = None

    # Kiểm tra thời gian
    if time.time() - start_time > TIME_LIMIT:
        # Nếu quá thời gian, chọn nước đi có điểm đánh giá cao nhất
        return evaluate(), best_move

    if maximizing:
        max_eval = -math.inf
        for r, c in moves:
            board[r][c] = AI
            if check_win(r, c, AI):
                board[r][c] = EMPTY
                return 100000, (r, c)
            eval, _ = minimax(depth - 1, alpha, beta, False, start_time)
            board[r][c] = EMPTY
            if eval > max_eval:
                max_eval = eval
                best_move = (r, c)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for r, c in moves:
            board[r][c] = PLAYER
            if check_win(r, c, PLAYER):
                board[r][c] = EMPTY
                return -100000, (r, c)
            eval, _ = minimax(depth - 1, alpha, beta, True, start_time)
            board[r][c] = EMPTY
            if eval < min_eval:
                min_eval = eval
                best_move = (r, c)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
    
def score_line(count):
    if count >= 5: return 100000
    return 10 ** count

# --- Tối ưu hóa hàm đánh giá ---
def evaluate():
    total = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                total += score_position(r, c, board[r][c]) * (1 if board[r][c] == AI else -1)
    return total

def score_position(r, c, player):
    score = 0
    for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
        count = 1
        for d in [1, -1]:
            nr, nc = r + dx * d, c + dy * d
            while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
                nr += dx * d
                nc += dy * d
        score += score_line(count)
    return score



def check_win(r, c, player):
    def count(dx, dy):
        cnt = 1
        for d in [1, -1]:
            nr, nc = r + dx * d, c + dy * d
            while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                cnt += 1
                nr += dx * d
                nc += dy * d
        return cnt
    for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
        if count(dx, dy) >= WIN_COUNT:
            return True
    return False


# --- Reset ---
def reset_game():
    global board, game_over, winner, current_turn, ai_cancelled
    ai_cancelled = False
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game_over = False
    winner = None
    current_turn = PLAYER
def go_home():
    pygame.quit()                         # Đóng pygame
    subprocess.Popen([sys.executable, "MAIN.py"])  # Chạy file caroAi.py
    sys.exit()   

reset_button = Button("Reset", 30, HEIGHT - 80, 120, 50, reset_game)
home_button = Button("Home", WIDTH - 150, HEIGHT - 80, 120, 50, go_home)
def draw_buttons():
    # Vẽ nút Reset
    reset_button.draw()
    home_button.draw()

# --- Main Loop ---
# --- Button "OK" --- 
ok_button = Button("OK", WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 50, lambda: hide_message())

# --- Hàm ẩn thông báo khi click vào nút OK ---
def hide_message():
    global game_over, winner
    game_over = False  # Ẩn thông báo chiến thắng
    winner = None  # Xóa thông tin người thắng

def ai_move():
    global current_turn, game_over, winner, ai_cancelled

    ai_cancelled = False  # Reset cờ khi AI bắt đầu chạy

    if game_over:
        return

    start_time = time.time()
    _, move = minimax(DEPTH, -math.inf, math.inf, True, start_time)
    if move:
        r, c = move
        board[r][c] = AI
        if check_win(r, c, AI):
            game_over = True
            winner = "Ai"
        current_turn = PLAYER


# --- Main Loop ---
clock = pygame.time.Clock()
ai_thread_running = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and current_turn == PLAYER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my < BOARD_SIZE * CELL_SIZE:
                    row, col = my // CELL_SIZE, mx // CELL_SIZE
                    if is_valid_move(row, col):
                        board[row][col] = PLAYER
                        if check_win(row, col, PLAYER):
                            game_over = True
                            winner = "Player"
                        else:
                            current_turn = AI

        # Nút Reset
        reset_button.handle_event(event)
        home_button.handle_event(event)
        if game_over:
            ok_button.handle_event(event)

    
    # Tạo thread cho AI nếu đến lượt nó
    if not game_over and current_turn == AI and not ai_thread_running:
        ai_thread_running = True
        threading.Thread(target=lambda: [ai_move(), setattr(sys.modules[__name__], 'ai_thread_running', False)]).start()

    draw_board()
    draw_buttons()

    if game_over:
        # Tạo text kết quả
        result_text = font.render(winner+" Win", True, (255, 0, 0))  # Màu đỏ
        text_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Vị trí chính giữa

        # Vẽ nền mờ phía sau thông báo để dễ đọc
        pygame.draw.rect(screen, (0, 0, 0, 180), text_rect.inflate(20, 20))  # Thêm khoảng cách cho nền
        screen.blit(result_text, text_rect)  # Hiển thị text kết quả

        # --- Button "OK" --- 
        # --- Button "X" --- 
        ok_button_width = 35  # Chiều rộng nút "X" bằng 1/4 chiều rộng thông báo
        ok_button_height = 35  # Chiều cao nút "X"
        ok_button_x = WIDTH // 2  - ok_button_width // 2 # Đảm bảo nút nằm giữa màn hình
        ok_button_y = text_rect.bottom + 10  # Nút nằm dưới thông báo
        

# Tạo nút "X" với vị trí đã chỉnh
        ok_button = Button("x", ok_button_x, ok_button_y, ok_button_width, ok_button_height, lambda: hide_message())
        
        ok_button.draw()

    pygame.display.flip()
    clock.tick(60)




