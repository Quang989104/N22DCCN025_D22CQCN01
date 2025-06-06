import pygame
import sys
import subprocess

BOARD_SIZE = 15
CELL_SIZE = 30
WIDTH, HEIGHT = CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE + 100
LINE_COLOR = (0, 0, 0)
BG_COLOR = (240, 217, 181)

PLAYER1 = 1
PLAYER2 = 2
EMPTY = 0
WIN_COUNT = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Caro - 2 Người Chơi")
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

icon = pygame.image.load("images/image.png")  
pygame.display.set_icon(icon)

board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False
winner = None
current_turn = PLAYER1

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

def draw_board():
    screen.fill((10, 10, 20))
    for x in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, (50, 50, 60), (x * CELL_SIZE, 0), (x * CELL_SIZE, BOARD_SIZE * CELL_SIZE))
    for y in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, (50, 50, 60), (0, y * CELL_SIZE), (BOARD_SIZE * CELL_SIZE, y * CELL_SIZE))
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            cell_value = board[y][x]
            center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            if cell_value == PLAYER1:  # O
                pygame.draw.circle(screen, (0, 255, 255), center, CELL_SIZE // 2 - 8, 4)
            elif cell_value == PLAYER2:  # X
                offset = CELL_SIZE // 2 - 10
                pygame.draw.line(screen, (255, 77, 77),
                                 (center[0] - offset, center[1] - offset),
                                 (center[0] + offset, center[1] + offset), 4)
                pygame.draw.line(screen, (255, 77, 77),
                                 (center[0] - offset, center[1] + offset),
                                 (center[0] + offset, center[1] - offset), 4)

def is_valid_move(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == EMPTY

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

def reset_game():
    global board, game_over, winner, current_turn
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game_over = False
    winner = None
    current_turn = PLAYER1

def go_home():
    pygame.quit()
    subprocess.Popen([sys.executable, "MAIN.py"])
    sys.exit()

def hide_message():
    global game_over, winner, current_turn
    game_over = False
    winner = None
    current_turn = PLAYER1

reset_button = Button("Reset", 30, HEIGHT - 80, 120, 50, reset_game)
home_button = Button("Home", WIDTH - 150, HEIGHT - 80, 120, 50, go_home)
ok_button = Button("OK", WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 50, hide_message)

def draw_buttons():
    reset_button.draw()
    home_button.draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my < BOARD_SIZE * CELL_SIZE:
                    row, col = my // CELL_SIZE, mx // CELL_SIZE
                    if is_valid_move(row, col):
                        board[row][col] = current_turn
                        draw_board()
                        if check_win(row, col, current_turn):
                            game_over = True
                            winner = "Player 1" if current_turn == PLAYER1 else "Player 2"
                        else:
                            current_turn = PLAYER2 if current_turn == PLAYER1 else PLAYER1

        reset_button.handle_event(event)
        home_button.handle_event(event)
        if game_over:
            ok_button.handle_event(event)

    draw_board()
    draw_buttons()

    if game_over:
        result_text = font.render(winner + " Win", True, (255, 0, 0))
        text_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, (0, 0, 0, 180), text_rect.inflate(20, 20))
        screen.blit(result_text, text_rect)
        ok_button_width = 35
        ok_button_height = 35
        ok_button_x = WIDTH // 2 - ok_button_width // 2
        ok_button_y = text_rect.bottom + 10
        ok_button = Button("x", ok_button_x, ok_button_y, ok_button_width, ok_button_height, hide_message)
        ok_button.draw()

    pygame.display.flip()
    clock.tick(60)
