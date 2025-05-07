import tkinter as tk

def draw_board(canvas, board_size, cell_size):
    """Draw the Caro game board grid"""
    canvas.delete("all")  # Clear everything before drawing
    
    # Draw the background
    canvas.create_rectangle(0, 0, board_size * cell_size, board_size * cell_size, 
                          fill="white", outline="")
    
    # Draw grid lines
    for i in range(board_size + 1):
        # Vẽ các dòng ngang (horizontal lines)
        canvas.create_line(0, i * cell_size, board_size * cell_size, i * cell_size, 
                          tags="grid_line", width=1)
        # Vẽ các dòng dọc (vertical lines)
        canvas.create_line(i * cell_size, 0, i * cell_size, board_size * cell_size, 
                          tags="grid_line", width=1)

def draw_pieces(canvas, board, cell_size):
    """Draw all pieces on the board"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != "":
                draw_piece(canvas, i, j, board[i][j], cell_size)

def draw_piece(canvas, row, col, player, cell_size=30):
    """Draw a single piece (X or O) at the specified position"""
    x0 = col * cell_size + 5
    y0 = row * cell_size + 5
    x1 = (col + 1) * cell_size - 5
    y1 = (row + 1) * cell_size - 5
    
    if player == "X":
        # Draw X in blue
        canvas.create_line(x0, y0, x1, y1, fill="blue", width=2, tags="piece")
        canvas.create_line(x0, y1, x1, y0, fill="blue", width=2, tags="piece")
    elif player == "O":
        # Draw O in red
        canvas.create_oval(x0, y0, x1, y1, outline="red", width=2, tags="piece")