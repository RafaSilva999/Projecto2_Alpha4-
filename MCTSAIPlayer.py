import math
import random
from Player import Player

class MCTSAIPlayer(Player):
    def __init__(self, piece, max_iterations=1000):
        super().__init__(piece)
        self.max_iterations = max_iterations
        self.opponent_piece = 1 if piece == 2 else 2

    
    
    def get_move(self, board):
        #tenho que implementar o ciclo principal do MCTS e no final retornar um numero inteiro que reprensenta a coluna onde o jogador irá jogar
        
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        
        root = MCTSNode(board.copy(), self.piece)
        for _ in range(self.max_iterations):
            node = root
            # Seleção
            while node.is_fully_expanded() and node.children:
                node = max(node.children, key=lambda n: n.ucb())
            # Expanção
            if not node.is_fully_expanded():
                move = random.choice(node.untried_moves)
                new_board = node.board.copy()
                new_board.drop_piece(move, node.piece)
                child_node = MCTSNode(new_board, 3 - node.piece, parent=node, move=move)
                node.children.append(child_node)
                node.untried_moves.remove(move)
                node = child_node
            # Simulação
            winner = self.simulate_random_game(node.board.copy(), node.piece)
            # Backpropagation
            while node is not None:
                node.visits += 1
                if winner == node.piece:
                    node.wins += 1
                elif winner != 0:
                    node.wins -= 1
                node = node.parent

        best_child = max(root.children, key=lambda n: n.visits)
        return best_child.move
    def simulate_random_game(self, board, piece):
        current_piece = piece
        while True:
            if board.check_winner(1):
                return 1
            if board.check_winner(2):
                return 2
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                return 0  # Draw
            move = random.choice(valid_moves)
            board.drop_piece(move, current_piece)
            current_piece = 3 - current_piece  

class MCTSNode:
    def __init__(self, board, piece, parent=None, move=None):
        self.board = board
        self.piece = piece
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_valid_moves()
    
    def ucb(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    def is_terminal(self):
        return (
            self.board.check_winner(1) or self.board.check_winner(2) or self.board.is_board_full()
        )