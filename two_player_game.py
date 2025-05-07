import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import subprocess

BOARD_SIZE = 15
CELL_SIZE = 35

def start_game():
    window = tk.Toplevel()
        # Căn giữa cửa sổ
    window_width = BOARD_SIZE * CELL_SIZE + 100
    window_height = BOARD_SIZE * CELL_SIZE + 150
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.geometry(f"{BOARD_SIZE * CELL_SIZE + 100}x{BOARD_SIZE * CELL_SIZE + 150}")
    window.title("🎯 CỜ CARO: Người vs Người")
    window.configure(bg="#121212")
    window.resizable(False, False)

    from PIL import Image
    import os

    # Đường dẫn ảnh
    image_path = os.path.join(os.path.dirname(__file__), "images")

    x_image = Image.open(os.path.join(image_path, "x.png")).resize((24, 20))
    o_image = Image.open(os.path.join(image_path, "o_icon.png")).resize((20, 20))

    x_icon = ImageTk.PhotoImage(x_image, master=window)
    o_icon = ImageTk.PhotoImage(o_image, master=window)

    current_player = ["X"]
    board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    buttons = []
    move_stack = []

    def make_move(row, col):
        if board[row][col] != "":
            return
        board[row][col] = current_player[0]
        icon = x_icon if current_player[0] == "X" else o_icon
        buttons[row][col].config(image=icon)
        move_stack.append((row, col, current_player[0]))
        if check_win(row, col):
            highlight_winner(row, col)
            messagebox.showinfo("🎉 Chiến thắng", f"Người chơi {current_player[0]} đã thắng!")
            disable_board()
            return
        current_player[0] = "O" if current_player[0] == "X" else "X"

    def disable_board():
        for row in buttons:
            for btn in row:
                btn.config(state="disabled")

    def highlight_winner(r, c):
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            coords = [(r, c)]
            for d in [-1, 1]:
                i, j = r + d * dx, c + d * dy
                while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == board[r][c]:
                    coords.append((i, j))
                    i += d * dx
                    j += d * dy
            if len(coords) >= 5:
                for x, y in coords:
                    buttons[x][y].config(bg="#ffeb3b")
                break

    def check_win(r, c):
        def count(dx, dy):
            total = 1
            for d in [-1, 1]:
                i, j = r + d * dx, c + d * dy
                while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == current_player[0]:
                    total += 1
                    i += d * dx
                    j += d * dy
            return total
        return (
            count(1, 0) >= 5 or
            count(0, 1) >= 5 or
            count(1, 1) >= 5 or
            count(1, -1) >= 5
        )

    def undo_move():
        if not move_stack:
            return
        row, col, last_player = move_stack.pop()
        board[row][col] = ""
        buttons[row][col].config(image="", bg="white")
        current_player[0] = last_player

    def reset_board():
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                board[r][c] = ""
                buttons[r][c].config(image="", bg="white", state="normal")
        move_stack.clear()
        current_player[0] = "X"

    def go_home():                        # Đóng pygame
        subprocess.Popen([sys.executable, "MAIN.py"]) 
        sys.exit() 

    def on_close():
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát không?"):
            window.destroy()

    # Đảm bảo khi người dùng nhấn nút X để đóng cửa sổ, hàm on_close sẽ được gọi
    window.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window, text="🧩 Cờ Caro - Người với Người 🧩", font=("Comic Sans MS", 20, "bold"),
             bg="#121212", fg="white").pack(pady=10)

    frame = tk.Frame(window, bg="white")
    frame.pack()


    for row in range(BOARD_SIZE):
        row_buttons = []
        for col in range(BOARD_SIZE):
            
            btn = tk.Button(frame, width=3, height=1,
                            bg="white", relief="solid",
                            command=lambda r=row, c=col: make_move(r, c))

            btn.grid(row=row, column=col, padx=1, pady=1)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    btn_frame = tk.Frame(window, bg="#121212")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="🔁 Chơi lại", font=("Arial", 12), command=reset_board,
            bg="#2196f3", fg="white", width=12).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="↩️ Undo", font=("Arial", 12), command=undo_move,
            bg="#ff9800", fg="white", width=12).grid(row=0, column=1, padx=10)

    # Nút "Home"
    tk.Button(btn_frame, text="🏠 Home", font=("Arial", 12), command=go_home,
            bg="#4caf50", fg="white", width=12).grid(row=1, column=0, padx=10, pady=10)