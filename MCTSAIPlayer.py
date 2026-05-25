import math
import random
from Player import Player

class MCTSAIPlayer(Player):
    def __init__(self, piece, max_iterations=1000):
        super().__init__(piece)
        self.max_iterations = max_iterations
        
    
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
                new_board.make_move(move, node.piece)
                child_node = MCTSNode(new_board, 3 - node.piece, parent=node, move=move)
                node.children.append(child_node)
                node.untried_moves.remove(move)
                node = child_node
            # Simulação
            winner = self.simulate_random_game(node.board.copy(), node.piece)
            # Backpropagation
            while node is not None:
                node.visits += 1
                if winner == self.piece:
                    node.wins += 1
                elif winner == 3 - self.piece:
                    node.wins -= 1
                node = node.parent

        best_child = max(root.children, key=lambda n: n.visits)
        return best_child.move

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
    
    def best_child(self, c=math.sqrt(2)):
        return max(self.children, key = lambda child: child.ucb(c))
    
    def expand(self):
        move = self._pick_untried_move()
        self.untried_moves.remove(move)

        new_board = self.board.copy()
        new_board.drop_piece(move, self.piece)

        enemy = 2 if self.piece == 1 else 1
        child = MCTSNode(new_board, enemy, parent=self, move=move)
        self.children.append(child)
        return child
    
    def _pick_untried_move(self):
        cols = self.board.cols
        center = cols // 2
        order = sorted(self.untried_moves, key = lambda c: abs(c- center))
        candidatos = order[:min(3, len(order))]
        return random.choice(candidatos)