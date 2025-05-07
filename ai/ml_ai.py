import numpy as np
import pickle
import random
import os
from tkinter import messagebox 

def load_ml_model(model_file):
    """
    Tải mô hình AI đã được huấn luyện
    """
    try:
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        print(f"Model file {model_file} not found!")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def board_to_features(board, player):
    """
    Chuyển đổi trạng thái bàn cờ thành feature vector
    """
    board_size = len(board)
    features = []
    
    # Chuyển đổi bàn cờ thành mảng phẳng
    for row in board:
        for cell in row:
            if cell == "":
                features.append(0)
            elif cell == "X":
                features.append(1)
            elif cell == "O":
                features.append(-1)
    
    # Thêm thông tin người chơi hiện tại
    player_value = 1 if player == "X" else -1
    features.append(player_value)
    
    return np.array([features])

def predict_move(model, board, player):
    """
    Dự đoán nước đi tốt nhất dựa trên mô hình AI
    """
    if model is None:
        # Nếu không có mô hình, trả về một nước đi ngẫu nhiên
        return get_random_move(board)
    
    board_size = len(board)
    features = board_to_features(board, player)
    
    # Lấy các dự đoán xác suất cho tất cả các vị trí
    move_probs = model.predict_proba(features)[0]
    
    # Tạo danh sách các nước đi hợp lệ (các ô trống)
    valid_moves = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == "":
                move_idx = i * board_size + j
                valid_moves.append((move_idx, move_probs[move_idx] if move_idx < len(move_probs) else 0))
    
    if not valid_moves:
        return None  # Không còn nước đi hợp lệ
    
    # Sắp xếp các nước đi theo xác suất giảm dần
    valid_moves.sort(key=lambda x: x[1], reverse=True)
    
    # Chọn một trong 3 nước đi tốt nhất (thêm một chút ngẫu nhiên)
    top_n = min(3, len(valid_moves))
    selected_move_idx = valid_moves[random.randint(0, top_n-1)][0]
    
    # Chuyển đổi về tọa độ (row, col)
    row = selected_move_idx // board_size
    col = selected_move_idx % board_size
    
    return row, col

def get_random_move(board):
    """
    Chọn một nước đi ngẫu nhiên từ các ô trống
    """
    empty_cells = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "":
                empty_cells.append((i, j))
    
    if empty_cells:
        return random.choice(empty_cells)
    else:
        return None