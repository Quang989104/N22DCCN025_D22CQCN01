import tkinter as tk
import sys
import subprocess
from gameplay.medium_mode import MediumAIMode

def back_to_main_menu():
    root.destroy()
    subprocess.Popen([sys.executable, "MAIN.py"])

def main():
    global root
    root = tk.Tk()

    window_width = 20 * 30
    window_height = 20 * 30 + 100

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.title("Caro Game - Medium Mode")
    
    app = MediumAIMode(root, back_to_main_menu)
    
    root.mainloop()

if __name__ == '__main__':
    main()
