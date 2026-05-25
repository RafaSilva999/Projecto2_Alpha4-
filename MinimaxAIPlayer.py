import math
import random
from Player import Player

class MinimaxAIPlayer(Player):
    def __init__(self, piece, max_depth=4):
        self.piece = piece
        self.max_depth = max_depth
        self.opponent_piece = 1 if piece == 2 else 2

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        
        column, score = self.minimax(board, self.max_depth, -math.inf, math.inf, True)
        if column is None:
            return random.choice(valid_moves)
        return column
        
    def is_terminal_node(self, board):
            return board.check_winner(self.piece) or board.check_winner(self.opponent_piece) or board.is_board_full()
        
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_moves = board.get_valid_moves()
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_winner(self.piece):
                    return (None, 100000000000000)
                elif board.check_winner(self.opponent_piece):
                    return (None, -10000000000000)
                else:  # Game over, sem mais valid moves
                    return (None, 0)
            else:  # Depth é zero
                return (None, self.evaluate_board(board, self.piece))
            
        if maximizing_player:
            value = -math.inf
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                board_copy = board.copy()
                board_copy.drop_piece(col, self.piece)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        
        else: #Adversário
            value = math.inf
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                board_copy = board.copy()
                board_copy.drop_piece(col, self.opponent_piece)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value
        
    def evaluate_board(self, board, player):
        score = 0
        grid = board.grid
        rows = len(grid)
        cols = len(grid[0])
        opponent_player = 1 if player == 2 else 2

        #dar prioridade ao centro
        center_array = [int(grid[i][cols//2]) for i in range(rows)]
        center_count = center_array.count(player)
        score += center_count * 3

        for i in range(rows):
            for j in range(cols-3):
                window = [int(grid[i][j+k]) for k in range(4)]
                score += self.evaluate_window(window, player, opponent_player)
        
        for i in range(rows-3):
            for j in range(cols):
                window = [int(grid[i+k][j]) for k in range(4)]
                score += self.evaluate_window(window, player, opponent_player)
        
        for i in range(rows-3):
            for j in range(cols-3):
                window = [int(grid[i+k][j+k]) for k in range(4)]
                score += self.evaluate_window(window, player, opponent_player)

        for i in range(rows-3):
            for j in range(cols-3):
                window = [int(grid[i+3-k][j+k]) for k in range(4)]
                score += self.evaluate_window(window, player, opponent_player)
        
        return score
    
    def evaluate_window(self, window, piece, opponent_piece):
        score = 0
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
        
        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4
        
        return score