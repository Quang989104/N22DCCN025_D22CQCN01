import random

def evaluate_cell(board, x, y, symbol):
    score = 0
    opponent = 'O' if symbol == 'X' else 'X'
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def count_line(dx, dy, s):
        cnt = 0
        for dir in [1, -1]:
            i, j = x, y
            while True:
                i += dx * dir
                j += dy * dir
                if 0 <= i < len(board) and 0 <= j < len(board) and board[i][j] == s:
                    cnt += 1
                else:
                    break
        return cnt

    for dx, dy in directions:
        score += count_line(dx, dy, symbol) * 10
        score += count_line(dx, dy, opponent) * 8

    return score


def best_move(board, symbol='O'):
    size = len(board)
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == '']

    scored_moves = []
    max_score = -1

    for x, y in empty_cells:
        score = evaluate_cell(board, x, y, symbol)
        if score > max_score:
            scored_moves = [(x, y)]
            max_score = score
        elif score == max_score:
            scored_moves.append((x, y))

    return random.choice(scored_moves) if scored_moves else None
