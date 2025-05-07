
from ai1 import best_move
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class CaroGame:
    def __init__(self, root, size=15, vs_ai=True):
        self.root = root
        self.size = size
        self.cell_size = 40
        self.symbols = ['X', 'O']
        self.turn = 0
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.buttons = []
        self.vs_ai = vs_ai

        self.build_gui()

    def build_gui(self):
        self.root.title("Cờ Caro")

    # Xây dựng bảng Caro
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.root, width=2, height=1, font=('Arial', 16),
                command=lambda x=i, y=j: self.handle_click(x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    # Thêm nút Reset ở góc dưới trái
        self.reset_button = tk.Button(self.root, text="Reset", font=('Arial', 14), command=self.reset_game)
        self.reset_button.grid(row=self.size, column=1, columnspan=2, sticky='w')

    # Thêm nút Home ở góc dưới phải
        self.home_button = tk.Button(self.root, text="Home", font=('Arial', 14), command=self.go_home)
        self.home_button.grid(row=self.size, column=self.size//2, columnspan=self.size//2, sticky='e')



    def handle_click(self, x, y):
        if self.board[x][y] != '':
            return

        self.place_symbol(x, y, self.symbols[self.turn])

        if self.check_win(x, y, self.symbols[self.turn]):
            messagebox.showinfo("Kết thúc", f"Người chơi {self.symbols[self.turn]} thắng!")
            self.disable_all()
            return

        self.turn = 1 - self.turn

        if self.vs_ai and self.symbols[self.turn] == 'O':
            self.root.after(300, self.ai_turn)

    def ai_turn(self):
        move = best_move(self.board, symbol='O')
        if move:
            x, y = move
            self.place_symbol(x, y, 'O')
            if self.check_win(x, y, 'O'):
                messagebox.showinfo("Kết thúc", "AI (O) thắng!")
                self.disable_all()
            else:
                self.turn = 1 - self.turn

    def place_symbol(self, x, y, symbol):
        self.board[x][y] = symbol
        self.buttons[x][y].config(text=symbol, disabledforeground='blue' if symbol == 'X' else 'red')
        self.buttons[x][y].config(state='disabled')

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')

    def check_win(self, x, y, symbol):
        def count(dx, dy):
            count = 1
            for dir in [1, -1]:
                i, j = x, y
                while True:
                    i += dx * dir
                    j += dy * dir
                    if 0 <= i < self.size and 0 <= j < self.size and self.board[i][j] == symbol:
                        count += 1
                    else:
                        break
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(count(dx, dy) >= 5 for dx, dy in directions)

    def reset_game(self):
        # Reset lại trò chơi
        self.turn = 0
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(text='', state='normal')

    def go_home(self):                      # Đóng pygame
        subprocess.Popen([sys.executable, "MAIN.py"])  # Chạy file caroAi.py
        sys.exit()

# Khởi tạo cửa sổ ứng dụng
root = tk.Tk()
game = CaroGame(root)
root.update_idletasks()

# Lấy kích thước thật sự sau khi GUI đã dựng xong
window_width = root.winfo_width()
window_height = root.winfo_height()

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tính toán vị trí căn giữa
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Đặt lại vị trí cửa sổ (không set lại width, height nữa)
root.geometry(f"+{x}+{y}")

root.mainloop()
