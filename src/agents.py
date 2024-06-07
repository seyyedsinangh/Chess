import datetime
import random

import chess

import utiles


class Agent:
    """
        Base class for agents.
    """

    def __init__(self, board: chess.Board, next_player) -> None:
        self.board = board
        self.next_player = next_player

    def get_action(self):
        """
            This method receives a GameState object and returns an action based on its strategy.
        """
        pass

    """
            get possible moves : 
                possibleMoves = board.legal_moves

            create a move object from possible move : 
                move = chess.Move.from_uci(str(possible_move))

            push the move : 
                board.push(move)

            pop the last move:
                board.pop(move)
    """


class RandomAgent(Agent):
    def __init__(self, board: chess.Board, next_player):
        super().__init__(board, next_player)

    def get_action(self):
        return self.random()

    def random(self):
        possible_moves_list = list(self.board.legal_moves)

        random_move = random.choice(possible_moves_list)
        return chess.Move.from_uci(str(random_move))


class MinimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        x, best_move = self.minimax(self.depth, 'white' if self.board.turn else 'black', self.board.turn)
        return best_move

    def minimax(self, depth, turn, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            evaluation = evaluate_board_state(self.board, turn)
            return evaluation if turn == 'white' else -evaluation, None
        possible_moves_list = list(self.board.legal_moves)
        best_move = None
        if is_maximizing:
            best_value = float("-inf")
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.minimax(depth - 1, next_turn, not is_maximizing)
                self.board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move
        else:
            best_value = float("inf")
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.minimax(depth - 1, next_turn, not is_maximizing)
                self.board.pop()
                if value < best_value:
                    best_value = value
                    best_move = move
        return best_value, best_move


class AlphaBetaAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        x, best_move = self.alpha_beta(self.depth, 'white' if self.board.turn else 'black', self.board.turn,
                                       float('-inf'), float('inf'))
        return best_move

    def alpha_beta(self, depth, turn, is_maximizing, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            evaluation = evaluate_board_state(self.board, turn)
            return evaluation if turn == 'white' else -evaluation, None
        possible_moves_list = list(self.board.legal_moves)
        best_move = None
        if is_maximizing:
            best_value = float("-inf")
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.alpha_beta(depth - 1, next_turn, not is_maximizing, alpha, beta)
                self.board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move
                if beta <= best_value:
                    break
                alpha = max(alpha, best_value)
        else:
            best_value = float("inf")
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.alpha_beta(depth - 1, next_turn, not is_maximizing, alpha, beta)
                self.board.pop()
                if value < best_value:
                    best_value = value
                    best_move = move
                if alpha >= best_value:
                    break
                beta = min(beta, best_value)

        return best_value, best_move


class ExpectimaxAgent(Agent):
    def __init__(self, board: chess.Board, next_player, depth):
        self.depth = depth
        super().__init__(board, next_player)

    def get_action(self):
        x, best_move = self.expectimax(self.depth, 'white' if self.board.turn else 'black', True)
        return best_move

    def expectimax(self, depth, turn, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            evaluation = evaluate_board_state(self.board, turn)
            return evaluation if is_maximizing else -evaluation, None
        possible_moves_list = list(self.board.legal_moves)
        best_move = possible_moves_list[0]
        if is_maximizing:
            best_value = float("-inf")
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.expectimax(depth - 1, next_turn, not is_maximizing)
                self.board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move
        else:
            value_sum = 0
            for move in possible_moves_list:
                move = chess.Move.from_uci(str(move))
                self.board.push(move)
                next_turn = 'white' if turn == 'black' else 'black'
                value, x = self.expectimax(depth - 1, next_turn, not is_maximizing)
                self.board.pop()
                value_sum += value
            best_value = value_sum / len(possible_moves_list)
        return best_value, best_move


def evaluate_board_state(board, turn):
    node_evaluation = 0
    node_evaluation += utiles.check_status(board, turn)
    node_evaluation += utiles.evaluationBoard(board)
    node_evaluation += utiles.checkmate_status(board, turn)
    node_evaluation += utiles.good_square_moves(board, turn)
    if turn == 'white':
        return node_evaluation
    return -node_evaluation
