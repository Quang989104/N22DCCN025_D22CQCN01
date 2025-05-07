import pygame
import sys
import subprocess
import random
import tkinter as tk
from ui_utils import draw_gradient, create_button
from game_actions import play_with_friend, exit_game, toggle_ai_levels, start_ai_game



pygame.init()

icon = pygame.image.load("images/image.png")  
pygame.display.set_icon(icon)


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CARO")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (200, 230, 255)
BLUE = (70, 130, 180)
DARK_RED = (178, 34, 34)
HOVER_COLOR = (135, 206, 250)


font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 40)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, action, border_color, fill_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.border_color = border_color
        self.fill_color = fill_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        color = HOVER_COLOR if self.hovered else self.fill_color
        
        pygame.draw.rect(surface, self.border_color, self.rect, border_radius=20, width=5)
        pygame.draw.rect(surface, color, self.rect.inflate(-10, -10), border_radius=20)
        draw_text(self.text, font, self.text_color, surface, self.rect.centerx, self.rect.centery)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()


MENU_MAIN = 0
MENU_AI = 1
current_menu = MENU_MAIN  


def start_game_ai():
    global current_menu
    current_menu = MENU_AI  

def start_game_human():
    pygame.quit()                        
    subprocess.Popen([sys.executable, "playerVsplayer.py"]) 
    sys.exit() 

def quit_game():
    pygame.quit()
    sys.exit()

def back_to_main():
    global current_menu
    current_menu = MENU_MAIN  

def play_easy():
    pygame.quit()                         
    subprocess.Popen([sys.executable, "easy.py"])  
    sys.exit() 

def play_medium():
    pygame.quit()                         
    subprocess.Popen([sys.executable, "medium.py"])  
    sys.exit()   

def play_hard():
    subprocess.Popen([sys.executable, "hard.py"])
    pygame.quit()                           
    sys.exit()                            



buttons_main = [
    Button(250, 180, 300, 70, "Play with AI", start_game_ai, BLUE, WHITE, BLUE),
    Button(250, 315, 300, 70, "Player vs Player", start_game_human, BLUE, WHITE, BLUE),
    Button(250, 450, 300, 70, "Exit game", quit_game, DARK_RED, WHITE, DARK_RED)
]


buttons_ai = [
    Button(250, 180, 300, 70, "Easy", play_easy, BLUE, WHITE, BLUE),
    Button(250, 270, 300, 70, "Medium", play_medium, BLUE, WHITE, BLUE),
    Button(250, 360, 300, 70, "Hard", play_hard, BLUE, WHITE, BLUE),
    Button(250, 450, 300, 70, "Back", back_to_main, DARK_RED, WHITE, DARK_RED)
]


class MovingText:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])
        self.text = random.choice(["X", "O"])
        self.color = random.choice([(70, 130, 180), (220, 20, 60)])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= WIDTH:
            self.speed_x *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        draw_text(self.text, small_font, self.color, surface, self.x, self.y)


moving_texts = [MovingText() for _ in range(10)]


running = True
while running:
    screen.fill(LIGHT_BLUE)

    
    for moving_text in moving_texts:
        moving_text.move()
        moving_text.draw(screen)

    
    draw_text("GAME CARO", font, BLACK, screen, WIDTH // 2, 70)

    
    if current_menu == MENU_MAIN:
        for button in buttons_main:
            button.draw(screen)
    elif current_menu == MENU_AI:
        draw_text("Choose difficulty", font, BLACK, screen, WIDTH // 2, 130)
        for button in buttons_ai:
            button.draw(screen)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_menu == MENU_MAIN:
            for button in buttons_main:
                button.check_click(event)
        elif current_menu == MENU_AI:
            for button in buttons_ai:
                button.check_click(event)

    pygame.display.flip()
    pygame.time.delay(30)



pygame.quit()