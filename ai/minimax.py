import copy
import random

WIN_CONDITION = 5

def evaluate_position(board, player, opponent):

    """
    Đánh giá trạng thái bảng cho người chơi đã cho.
    Trả về điểm số cho biết vị trí thuận lợi như thế nào.
    """
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # ngang, dọc, chéo, chéo ngược
    size = len(board)
    

    # Phát hiện các mẫu đặc biệt
    # Năm liên tiếp (thắng)
    win_score = detect_pattern(board, size, directions, player, 5, 0)
    if win_score > 0:
        return 10000  # Win
    
    # Đối thủ thua năm trận liên tiếp (thua)
    opponent_win = detect_pattern(board, size, directions, opponent, 5, 0)
    if opponent_win > 0:
        return -10000  # Lose
    
    # Mở bốn (mối đe dọa rất cao)
    open_four = detect_pattern(board, size, directions, player, 4, 2)
    score += open_four * 2000
    
    # Đối thủ mở bốn (phải chặn)
    opponent_open_four = detect_pattern(board, size, directions, opponent, 4, 2)
    score -= opponent_open_four * 2500  # Higher priority to block
    
    # Bán mở bốn (một bên bị chặn)
    semi_open_four = detect_pattern(board, size, directions, player, 4, 1)
    score += semi_open_four * 500
    
    
    # Đối thủ bán mở bốn
    opponent_semi_open_four = detect_pattern(board, size, directions, opponent, 4, 1)
    score -= opponent_semi_open_four * 600
    
    # Mở ba
    open_three = detect_pattern(board, size, directions, player, 3, 2)
    score += open_three * 200
    
    # đối thủ mở ba
    opponent_open_three = detect_pattern(board, size, directions, opponent, 3, 2)
    score -= opponent_open_three * 250
    
    # mở ba nửa
    semi_open_three = detect_pattern(board, size, directions, player, 3, 1)
    score += semi_open_three * 50
    
    # bán mở ba của đối thủ
    opponent_semi_open_three = detect_pattern(board, size, directions, opponent, 3, 1)
    score -= opponent_semi_open_three * 60
    
    # Phần thưởng kiểm soát trung tâm (các quân cờ gần trung tâm có giá trị hơn)
    center = size // 2
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                # Khoảng cách từ tâm (càng gần càng tốt)
                distance = abs(i - center) + abs(j - center)
                score += max(0, (size - distance)) // 2
    
    return score

def detect_pattern(board, size, directions, player, length, open_ends_required):
    """
    Detect patterns of specific length and open ends
    Returns the count of such patterns found
    """
    count = 0
    
    for i in range(size):
        for j in range(size):
            if board[i][j] != player:
                continue
                
            for dx, dy in directions:
                # Check if this could be the start of a pattern
                if i - dx >= 0 and j - dy >= 0 and board[i-dx][j-dy] == player:
                    continue  # Not the start of a pattern
                
                # Count consecutive pieces
                consecutive = 0
                x, y = i, j
                
                while 0 <= x < size and 0 <= y < size and board[x][y] == player:
                    consecutive += 1
                    x += dx
                    y += dy
                
                if consecutive == length:
                    # Count open ends
                    open_ends = 0
                    
                    # Check before the pattern
                    if i - dx >= 0 and j - dy >= 0 and board[i-dx][j-dy] == "":
                        open_ends += 1
                        
                    # Check after the pattern
                    if 0 <= x < size and 0 <= y < size and board[x][y] == "":
                        open_ends += 1
                    
                    if open_ends >= open_ends_required:
                        count += 1
    
    return count

def evaluate_lines(board, size, directions, player, weight):
    """Helper function to evaluate lines for a specific player"""
    score = 0
    
    for x in range(size):
        for y in range(size):
            if board[x][y] != player:
                continue
                
            for dx, dy in directions:
                # Check for consecutive pieces
                consecutive = count_consecutive(board, size, x, y, dx, dy, player)
                
                # Apply scoring based on consecutive pieces
                if consecutive == 5:  # Win condition
                    score += 10000 * weight
                elif consecutive == 4:  # Near win
                    # Check if open-ended
                    open_ends = count_open_ends(board, size, x, y, dx, dy, player, 4)
                    if open_ends > 0:
                        score += (500 * open_ends) * weight
                    else:
                        score += 100 * weight
                elif consecutive == 3:
                    open_ends = count_open_ends(board, size, x, y, dx, dy, player, 3)
                    if open_ends > 0:
                        score += (50 * open_ends) * weight
                    else:
                        score += 10 * weight
                elif consecutive == 2:
                    open_ends = count_open_ends(board, size, x, y, dx, dy, player, 2)
                    if open_ends > 0:
                        score += (5 * open_ends) * weight
    
    return score

def count_consecutive(board, size, x, y, dx, dy, player):
    """Count consecutive pieces from a starting position in a direction"""
    count = 0
    for i in range(WIN_CONDITION):
        nx, ny = x + i*dx, y + i*dy
        if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == player:
            count += 1
        else:
            break
    return count

def count_open_ends(board, size, x, y, dx, dy, player, length):
    """Count open ends for a sequence of pieces"""
    open_ends = 0
    
    # Check before the sequence
    start_x, start_y = x - dx, y - dy
    if 0 <= start_x < size and 0 <= start_y < size and board[start_x][start_y] == "":
        open_ends += 1
        
    # Check after the sequence
    end_x, end_y = x + length*dx, y + length*dy
    if 0 <= end_x < size and 0 <= end_y < size and board[end_x][end_y] == "":
        open_ends += 1
        
    return open_ends

def minimax(board, depth, is_maximizing, player, opponent, alpha=float('-inf'), beta=float('inf')):    
    """
    Thuật toán Minimax với cắt tỉa alpha-beta để tìm nước đi tốt nhất.
    Trả về (điểm, nước đi) trong đó nước đi là (hàng, cột).
    """    
    # Trường hợp cơ bản: nếu đạt độ sâu tối đa, hãy đánh giá bảng
    if depth == 0:
        return evaluate_position(board, player, opponent), None
    
    # Nhận các nước đi có thể, ưu tiên các nước đi gần các quân cờ hiện có
    moves = get_smart_moves(board)
    if not moves:
        return 0, None  # Không có nước đi nào khả dụng, trò chơi hòa
    
    best_move = None
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in moves:
            row, col = move           
            # Hãy di chuyển
            new_board = copy.deepcopy(board)
            new_board[row][col] = player
            
            # Kiểm tra xem nước đi này có thắng không
            if is_winning_move(new_board, row, col, player):
                return 10000, move
            
            # Gọi minimax đệ quy
            eval_score, _ = minimax(new_board, depth - 1, False, player, opponent, alpha, beta)
            
            # Cập nhật nước đi tốt nhất
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
           
            # Cắt tỉa Alpha-beta
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            row, col = move
            # Hãy di chuyển
            new_board = copy.deepcopy(board)
            new_board[row][col] = opponent
            
            # Kiểm tra xem nước đi này có thắng cho đối thủ không
            if is_winning_move(new_board, row, col, opponent):
                return -10000, move
            
            # Gọi minimax đệ quy
            eval_score, _ = minimax(new_board, depth - 1, True, player, opponent, alpha, beta)
            
            # Cập nhật nước đi tốt nhất
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move                
            
            # Cắt tỉa Alpha-beta
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
                
        return min_eval, best_move

def get_smart_moves(board):
    """
    Get strategic moves to reduce the search space.
    """
    size = len(board)
    moves = []
    has_pieces = False
    
    # Check if there are any pieces on the board
    for i in range(size):
        for j in range(size):
            if board[i][j] != "":
                has_pieces = True
                break
        if has_pieces:
            break
    
    # If no pieces, play near the center
    if not has_pieces:
        center = size // 2
        return [(center, center)]
    
    # First priority: Find cells that would create a line of 4 or block opponent's line of 4
    for i in range(size):
        for j in range(size):
            if board[i][j] != "":
                player = board[i][j]
                opponent = "O" if player == "X" else "X"
                
                # Check adjacent cells for strategic positions
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if di == 0 and dj == 0:
                            continue
                        
                        # Look for patterns like "XX_X" or "OO_O"
                        for pl in [player, opponent]:  # Check both for player's move and blocking opponent
                            count = 0
                            empty_pos = None
                            
                            # Check up to 4 cells in this direction
                            for step in range(4):
                                ni = i + di * step
                                nj = j + dj * step
                                
                                if not (0 <= ni < size and 0 <= nj < size):
                                    break
                                
                                if board[ni][nj] == pl:
                                    count += 1
                                elif board[ni][nj] == "":
                                    if empty_pos is None:  # Only consider first empty cell
                                        empty_pos = (ni, nj)
                                else:
                                    # Found opponent's piece, break
                                    break
                            
                            # If we found a strategic pattern (3 pieces and 1 empty)
                            if count >= 3 and empty_pos is not None and empty_pos not in moves:
                                moves.append(empty_pos)
    
    # If no high-priority moves found, consider cells adjacent to existing pieces
    if not moves:
        for i in range(size):
            for j in range(size):
                if board[i][j] != "":
                    # Check adjacent cells (including diagonals)
                    for di in range(-2, 3):
                        for dj in range(-2, 3):
                            ni, nj = i + di, j + dj
                            if (0 <= ni < size and 0 <= nj < size and 
                                board[ni][nj] == "" and 
                                (ni, nj) not in moves):
                                moves.append((ni, nj))
    
    # If still no moves, get all empty cells
    if not moves:
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    moves.append((i, j))
    
    # Shuffle moves to add some randomness
    random.shuffle(moves)
    return moves[:15]  # Limit to 15 moves for better performance

def is_winning_move(board, row, col, player):
    """Check if the given move results in a win"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    size = len(board)
    
    for dx, dy in directions:
        count = 1  # Count the piece we just placed
        
        # Check in both directions
        for direction in [1, -1]:
            nx, ny = row, col
            while True:
                nx += direction * dx
                ny += direction * dy
                if (0 <= nx < size and 0 <= ny < size and 
                    board[nx][ny] == player):
                    count += 1
                else:
                    break
                    
        if count >= WIN_CONDITION:
            return True
            
    return False

def get_all_moves(board):
    """Get all possible moves (empty cells) on the board"""
    moves = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "":
                moves.append((i, j))
    return moves