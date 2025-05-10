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
