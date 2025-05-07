from gameplay.base_mode import BaseGameMode
from ai.minimax import minimax

class MediumAIMode(BaseGameMode):
    def __init__(self, root, back_to_menu_callback):
        super().__init__(root, back_to_menu_callback, mode_name="Minimax AI")
    
    def ai_move(self):
        if self.game_over:
            return
            
        # Use minimax to find best move for AI
        _, move = minimax(
            self.board, 
            depth=2,  # Increase for stronger AI (but slower)
            is_maximizing=True,
            player='O',  # AI is O
            opponent='X'  # Player is X
        )
        
        if move:
            row, col = move
            # Place AI's move
            self.place_move(row, col, 'O')
            
            # Check if AI won
            if self.check_win(row, col):
                self.player_info.config(text="🤖 AI đã chiến thắng!")
                self.game_over = True
                return
                
            # Check for draw
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
                
            # Update status back to player
            self.player_info.config(text=f"Lượt của: {self.current_player} ({self.mode_name})")