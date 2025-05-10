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
        self.current_player = 'X'  # Người chơi luôn bắt đầu với X
        self.game_over = False
        self.mode_name = mode_name
        
        # Thiết lập kích thước cửa sổ
        window_width = self.board_size * self.cell_size
        window_height = self.board_size * self.cell_size + 100  # Không gian thêm cho các điều khiển
        self.root.geometry(f"{window_width}x{window_height}")
        
        self.create_widgets()
        draw_board(self.canvas, self.board_size, self.cell_size)
        
        # Tạo game_data.jsonl nếu chưa tồn tại
        self.game_data_file = "game_data.jsonl"
        if not os.path.exists(self.game_data_file):
            with open(self.game_data_file, "w", encoding="utf-8") as f:
                pass
    
    def create_widgets(self):
        # Tạo khung cho bảng
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        
        # Tạo canvas cho bảng
        self.canvas = tk.Canvas(
            board_frame, 
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            bg='white'
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Tạo khung cho điều khiển
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        # Nhãn thông tin người chơi
        self.player_info = tk.Label(
            control_frame, 
            text=f"Lượt của: người chơi",
            font=("Arial", 12)
        )
        self.player_info.pack(side=tk.LEFT, padx=10)
        
        # Khung cho các nút
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        # Nút chơi lại và quay lại
        tk.Button(
            button_frame, 
            text="Chơi lại", 
            command=self.reset_board,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Sửa nút "Quay lại menu" để gọi hàm callback "back_to_menu"
        tk.Button(
            button_frame, 
            text="Quay lại menu", 
            command=self.handle_back_to_menu,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def handle_back_to_menu(self):
        """Hàm này đảm bảo rằng chúng ta sẽ gọi hàm back_to_menu đúng cách"""
        # Reset bảng trước khi quay lại menu
        self.reset_board()
        
        # Đảm bảo rằng callback được gọi sau một khoảng thời gian ngắn
        # Điều này giúp tránh các vấn đề timing trong Tkinter
        if self.back_to_menu:
            self.root.after(100, self.back_to_menu)
    
    def on_click(self, event):
        if self.game_over:
            return
            
        # Tính toán hàng và cột từ vị trí click chuột
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Kiểm tra xem ô có hợp lệ và trống không
        if (0 <= row < self.board_size and 
            0 <= col < self.board_size and 
            self.board[row][col] == ""):
            
            # Đặt nước đi của người chơi
            self.place_move(row, col, self.current_player)
            
            # Kiểm tra nếu người chơi thắng
            if self.check_win(row, col):
                self.player_info.config(text=f"🎉 Người chơi đã chiến thắng!")
                self.game_over = True
                return
                
            # Kiểm tra hòa
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
                
            # Cập nhật trạng thái và chờ nước đi của AI
            self.player_info.config(text="AI đang suy nghĩ...")
            self.root.update()  # Cập nhật UI
            
            # Lên lịch cho nước đi của AI sau một chút độ trễ
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """Sẽ được triển khai bởi các lớp con"""
        raise NotImplementedError("Các lớp con phải triển khai phương thức ai_move")
    
    def place_move(self, row, col, player):
        """Đặt một nước đi trên bảng và cập nhật hiển thị"""
        self.board[row][col] = player
        draw_piece(self.canvas, row, col, player, self.cell_size)
        self.log_move(row, col, player)
        
        # Chuyển đổi người chơi hiện tại nếu cần
        if player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
    
    def reset_board(self):
        """Reset bảng và trạng thái trò chơi"""
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.canvas.delete("all")
        draw_board(self.canvas, self.board_size, self.cell_size)
        self.current_player = 'X'
        self.game_over = False
        self.player_info.config(text=f"Lượt của: người chơi")
    
    def check_win(self, row, col):
        """Kiểm tra xem nước đi cuối cùng tại (row, col) có dẫn đến chiến thắng không"""
        # Lấy người chơi đã thực hiện nước đi
        player = self.board[row][col]
        
        # Kiểm tra 4 hướng: ngang, dọc, chéo, chéo ngược
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1  # Bắt đầu với 1 cho quân cờ hiện tại
            
            # Kiểm tra cả hai hướng dương và âm
            for direction in [1, -1]:
                nx, ny = row, col
                
                # Tiếp tục kiểm tra theo hướng này miễn là tìm thấy các quân cờ phù hợp
                while True:
                    nx += direction * dx
                    ny += direction * dy
                    
                    # Kiểm tra ranh giới và xem quân cờ có khớp không
                    if (0 <= nx < self.board_size and 
                        0 <= ny < self.board_size and 
                        self.board[nx][ny] == player):
                        count += 1
                    else:
                        break
            
            # Nếu tìm thấy 5 quân cờ liên tiếp trở lên, đó là chiến thắng
            if count >= 5:
                # Làm nổi bật đường thắng
                self.highlight_winning_line(row, col, dx, dy)
                return True
                
        return False
    
    def highlight_winning_line(self, row, col, dx, dy):
        """Làm nổi bật đường thắng trên bảng"""
        player = self.board[row][col]
        positions = [(row, col)]  # Bắt đầu với nước đi cuối cùng
        
        # Tìm tất cả các vị trí trong đường thắng
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
        
        # Làm nổi bật mỗi vị trí
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
        """Kiểm tra xem bảng đã đầy chưa"""
        for row in self.board:
            if "" in row:
                return False
        return True
    
    def log_move(self, row, col, player):
        """Ghi lại nước đi vào file JSON Line để huấn luyện AI sau này"""
        try:
            # Đơn giản hóa dữ liệu để tiết kiệm không gian
            data = {
                "move": [row, col],
                "player": player
                # Có thể lược bỏ trạng thái bảng để tiết kiệm không gian
            }
            
            with open(self.game_data_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"Lỗi khi ghi lại nước đi: {e}")