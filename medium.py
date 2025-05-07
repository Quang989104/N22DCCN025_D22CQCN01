import tkinter as tk
from gui import GameGUI
from gameplay.medium_mode import MediumAIMode
from gameplay.ml_mode import MLAIMode

if __name__ == '__main__':
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()