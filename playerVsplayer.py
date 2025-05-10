import tkinter as tk
from ui_utils import draw_gradient, create_button
from game_actions import play_with_friend

root = tk.Tk()
root.title("🎮 Menu Game")
root.geometry("600x500")
root.resizable(False, False)

canvas = tk.Canvas(root, width=600, height=500)
canvas.pack(fill="both", expand=True)
draw_gradient(canvas, root, "#8e2de2", "#4a00e0")


play_with_friend(root)
root.mainloop()
