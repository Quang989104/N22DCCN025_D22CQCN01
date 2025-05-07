import tkinter as tk
from gameplay.base_mode import BaseGameMode
from ai.ml_ai import load_ml_model, predict_move

class MLAIMode(BaseGameMode):
    def __init__(self, root, back_to_menu_callback):
        super().__init__(root, back_to_menu_callback, mode_name="Machine Learning AI")
        
        # Tải mô hình AI đã huấn luyện
        self.model_file = "caro_ai_model.pkl"
        self.ai_model = load_ml_model(self.model_file)
        
        if self.ai_model is None:
            # Hiển thị thông báo nếu không tìm thấy mô hình
            tk.messagebox.showwarning(
                "Model Not Found", 
                f"Không tìm thấy file mô hình AI '{self.model_file}'.\nAI sẽ chơi ngẫu nhiên."
            )
    
    def ai_move(self):
        if self.game_over:
            return
            
        # Use ML model to predict next move
        move = predict_move(self.ai_model, self.board, 'O')
        
        if move:
            row, col = move
            # Place AI's move
            self.place_move(row, col, 'O')
            
            # Check if AI won
            if self.check_win(row, col):
                self.player_info.config(text="AI thắng!")
                self.game_over = True
                return
                
            # Check for draw
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
                
            # Update status back to player
            self.player_info.config(text=f"Lượt của: {self.current_player} ({self.mode_name})")