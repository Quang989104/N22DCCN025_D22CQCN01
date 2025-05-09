import tkinter as tk
import json
import os
from utils.draw import draw_board, draw_pieces, draw_piece

class BaseGameMode:
    def __init__(self, root, back_to_menu_callback, mode_name="Base"):
        self.root = root
        self.back_to_menu = back_to_menu_callback
        self.board_size = 20
        self.cell_size = 30
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'  
        self.game_over = False
        self.mode_name = mode_name
        
        window_width = self.board_size * self.cell_size
        window_height = self.board_size * self.cell_size + 100  
        self.root.geometry(f"{window_width}x{window_height}")
        
        self.create_widgets()
        draw_board(self.canvas, self.board_size, self.cell_size)
        
        self.game_data_file = "game_data.jsonl"
        if not os.path.exists(self.game_data_file):
            with open(self.game_data_file, "w", encoding="utf-8") as f:
                pass
    
    def create_widgets(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(
            board_frame, 
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            bg='white'
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        self.player_info = tk.Label(
            control_frame, 
            text=f"Lượt của: {self.current_player} ({self.mode_name})",
            font=("Arial", 12)
        )
        self.player_info.pack(side=tk.LEFT, padx=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        tk.Button(
            button_frame, 
            text="Chơi lại", 
            command=self.reset_board,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="Quay lại menu", 
            command=self.back_to_menu,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def on_click(self, event):
        if self.game_over:
            return
            
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if (0 <= row < self.board_size and 
            0 <= col < self.board_size and 
            self.board[row][col] == ""):
            
            self.place_move(row, col, self.current_player)
            
            if self.check_win(row, col):
                self.player_info.config(text=f"🎉 Người chơi đã chiến thắng!")
                self.game_over = True
                return
                
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
                
            self.player_info.config(text="AI đang suy nghĩ...")
            self.root.update() 
           
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement ai_move method")
    
    def place_move(self, row, col, player):
        """Place a move on the board and update display"""
        self.board[row][col] = player
        draw_piece(self.canvas, row, col, player, self.cell_size)
        self.log_move(row, col, player)
        
        if player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
    
    def reset_board(self):
        """Reset the game board and state"""
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.canvas.delete("all")
        draw_board(self.canvas, self.board_size, self.cell_size)
        self.current_player = 'X'
        self.game_over = False
        self.player_info.config(text=f"Lượt của: {self.current_player} ({self.mode_name})")
    
    def check_win(self, row, col):
        player = self.board[row][col]
        
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1  
            for direction in [1, -1]:
                nx, ny = row, col
                
                while True:
                    nx += direction * dx
                    ny += direction * dy
                    
                    if (0 <= nx < self.board_size and 
                        0 <= ny < self.board_size and 
                        self.board[nx][ny] == player):
                        count += 1
                    else:
                        break
            
            if count >= 5:
                self.highlight_winning_line(row, col, dx, dy)
                return True
                
        return False
    
    def highlight_winning_line(self, row, col, dx, dy):
        """Highlight the winning line on the board"""
        player = self.board[row][col]
        positions = [(row, col)]  
        
        for direction in [1, -1]:
            nx, ny = row, col
            while True:
                nx += direction * dx
                ny += direction * dy
                if (0 <= nx < self.board_size and 
                    0 <= ny < self.board_size and 
                    self.board[nx][ny] == player):
                    positions.append((nx, ny))
                else:
                    break
        
        highlight_color = "green"
        for r, c in positions:
            x0 = c * self.cell_size
            y0 = r * self.cell_size
            x1 = (c + 1) * self.cell_size
            y1 = (r + 1) * self.cell_size
            
            self.canvas.create_rectangle(
                x0, y0, x1, y1, 
                outline=highlight_color, 
                width=2
            )
    
    def is_board_full(self):
        """Check if the board is completely filled"""
        for row in self.board:
            if "" in row:
                return False
        return True
    
    def log_move(self, row, col, player):
        """Log the move to a JSON Line file for AI training"""
        try:
            data = {
                "board": [row[:] for row in self.board],  
                "move": [row, col],
                "player": player
            }
            
            with open(self.game_data_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"Error logging move: {e}")