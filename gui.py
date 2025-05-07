import tkinter as tk
from gameplay.medium_mode import MediumAIMode
from gameplay.ml_mode import MLAIMode
import subprocess
import sys

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro Game")
        self.root.resizable(False, False)
        self.start_medium_ai()
        self.center_window(20*30, 23*30+5)


    def main_menu(self):
        self.clear_window()                      
        subprocess.Popen([sys.executable, "MAIN.py"])  
        sys.exit() 
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


    def ai_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Chọn độ khó", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Trung Bình (Minimax)", command=self.start_medium_ai, width=25, height=2).pack(pady=10)
        tk.Button(self.root, text="AI Học Máy (ML)", command=self.start_ml_ai, width=25, height=2).pack(pady=10)
        tk.Button(self.root, text="Quay Lại", command=self.main_menu, width=25, height=2).pack(pady=10)

    def start_medium_ai(self):
        self.clear_window()
        MediumAIMode(self.root, self.main_menu)
        
    def start_ml_ai(self):
        self.clear_window()
        MLAIMode(self.root, self.main_menu)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()