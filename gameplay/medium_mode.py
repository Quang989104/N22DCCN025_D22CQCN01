from gameplay.base_mode import BaseGameMode
from ai.minimax import minimax

class MediumAIMode(BaseGameMode):
    def __init__(self, root, back_to_menu_callback):
        super().__init__(root, back_to_menu_callback, mode_name="Minimax AI")
   
        self.player_symbol = 'X' 
        self.ai_symbol = 'O'      
    
    def ai_move(self):
        if self.game_over:
            return
            
        _, move = minimax(
            self.board, 
            depth=2,  
            is_maximizing=True,
            player=self.ai_symbol,    
            opponent=self.player_symbol  
        )
        
        if move:
            row, col = move
        
            self.place_move(row, col, self.ai_symbol)
            
          
            if self.check_win(row, col):
                self.player_info.config(text="🤖 AI đã chiến thắng!")
                self.game_over = True
                return
                
       
            if self.is_board_full():
                self.player_info.config(text="Hòa!")
                self.game_over = True
                return
                
      
            self.player_info.config(text=f"Lượt của: người chơi")