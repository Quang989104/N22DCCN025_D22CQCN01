import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pickle
import os

def load_game_data(file_path):
    """
    Đọc dữ liệu từ file game_data.jsonl
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip(): 
                try:
                    game_move = json.loads(line)
                    data.append(game_move)
                except json.JSONDecodeError:
                    print(f"Ignore invalid JSON line: {line}")
    return data

def preprocess_data(game_data):
    """
    Chuyển đổi dữ liệu thành định dạng phù hợp cho huấn luyện
    X: features (trạng thái bàn cờ)
    y: labels (nước đi tiếp theo)
    """
    X = [] 
    y = [] 
    
    for move_data in game_data:
        board = move_data["board"]
        move = move_data["move"]
        player = move_data["player"]
        
        board_flat = []
        for row in board:
            for cell in row:
                if cell == "":
                    board_flat.append(0)
                elif cell == "X":
                    board_flat.append(1)
                elif cell == "O":
                    board_flat.append(-1)
        
     
        player_value = 1 if player == "X" else -1
        board_flat.append(player_value)
        
        X.append(board_flat)
        
        move_position = move[0] * len(board[0]) + move[1]
        y.append(move_position)
    
    return np.array(X), np.array(y)

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation='relu',
        solver='adam',
        alpha=0.0001,
        batch_size='auto',
        learning_rate='adaptive',
        max_iter=1000,
        verbose=True
    )
    
    model.fit(X_train, y_train)
    
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    
    return model

def save_model(model, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {file_path}")

def main():
    data_file = "game_data.jsonl"
    
    if not os.path.exists(data_file):
        print(f"Error: Data file {data_file} not found!")
        return
    
    print("Loading game data...")
    game_data = load_game_data(data_file)
    print(f"Loaded {len(game_data)} moves.")
    
    if len(game_data) < 100:
        print("Warning: Dataset is very small. Consider collecting more data for better results.")
    
    print("Preprocessing data...")
    X, y = preprocess_data(game_data)
    
    print("Training model...")
    model = train_model(X, y)
    
    model_file = "caro_ai_model.pkl"
    save_model(model, model_file)

if __name__ == "__main__":
    main()