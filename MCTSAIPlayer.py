import math
import random
from Player import Player


class MCTSAIPlayer(Player):
    def __init__(self, piece, max_iterations=1000):
        super().__init__(piece)
        self.max_iterations = max_iterations
        self.opponent_piece = 1 if piece == 2 else 2

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None

        root = MCTSNode(board.copy(), self.piece)
        for _ in range(self.max_iterations):
            node = root

            # Seleção
            node = self._select(root)

            # Expansão
            if not node.is_terminal() and not node.is_fully_expanded():
                node = self._expand(node)
            #Simulação

            reward = self._simulate(node)
            self._backpropagate(node, reward)

        if not root.children:
            return random.choice(board.get_valid_moves())

        best_child = max(root.children, key=lambda n: n.visits)
        return best_child.move
    
    def _expand(self, node):
        move = node.untried_moves[0]  # primeiro por ordem
        new_board = node.board.copy()
        new_board.drop_piece(move, node.piece)
        child_piece = 3 - node.piece
        child_node = MCTSNode(new_board, child_piece, parent=node, move=move)
        node.children.append(child_node)
        node.untried_moves.pop(0)
        return child_node
    
    def _select(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node
            else:
                node = max(node.children, key=lambda n: n.ucb())
        return node
    
    def _simulate(self, node):
        board = node.board.copy()
        current_piece = node.piece
        while True:
            
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                return 0  # empate

            move = random.choice(valid_moves)
            board.drop_piece(move, current_piece)

            if board.check_winner(current_piece):
                return 1 if current_piece == self.piece else 0

            if board.is_board_full():
                return 0

            current_piece = 3 - current_piece
    
    def _backpropagate(self, node, reward):
        current = node
        while current is not None:
            current.visits += 1
            current.wins += reward
            current = current.parent

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
            self.board.check_winner(1) or
            self.board.check_winner(2) or
            self.board.is_board_full()
        )
    def _expand(self, node):
        move = node.untried_moves[0]
        new_board = node.board.copy()
        new_board.drop_piece(move, node.piece)
        child_piece = 3 - node.piece
        child_node = MCTSNode(new_board, child_piece, parent=node, move=move)
        node.children.append(child_node)
        node.untried_moves.pop(0)
        return child_node