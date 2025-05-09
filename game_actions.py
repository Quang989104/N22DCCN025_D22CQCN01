import sys
import tkinter as tk
from tkinter import messagebox
import two_player_game

def play_with_friend(root):
    root.withdraw() 
    two_player_game.start_game()  

def exit_game(root):
    root.destroy()
    sys.exit()

def toggle_ai_levels(level_easy, level_medium, level_hard):
    if level_easy.winfo_ismapped():
        level_easy.place_forget()
        level_medium.place_forget()
        level_hard.place_forget()
    else:
        level_easy.place(relx=0.5, y=320, anchor="center")
        level_medium.place(relx=0.5, y=370, anchor="center")
        level_hard.place(relx=0.5, y=420, anchor="center")

def start_ai_game(level):
    messagebox.showinfo("Thông báo", f"Đang vào chế độ Chơi với Máy - Cấp độ: {level}\n(Tính năng đang phát triển)")
