from gameplay.base_mode import BaseGameMode
from ai.minimax import minimax

class MediumAIMode(BaseGameMode):
    def __init__(self, root, back_to_menu_callback):
        super().__init__(root, back_to_menu_callback, mode_name="Minimax AI")
    
    def ai_move(self):
        if self.game_over:
            return
            
        _, move = minimax(
            self.board, 
            depth=2,  
            is_maximizing=True,
            player='O', 
            opponent='X'  
        )
        
        if move:
            row, col = move
            self.place_move(row, col, 'O')
            
            if self.check_win(row, col):
                self.player_info.config(text="🤖 AI đã chiến thắng!")
                self.game_over = True
                return
                
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
            self.player_info.config(text=f"Lượt của: {self.current_player} ({self.mode_name})")