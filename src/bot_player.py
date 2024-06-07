import datetime
import chess
from game import Game
from board import Board
from dragger import Dragger
import agents
from translate_move import TranslateMove

from move import Move
from square import Square


class BotPlayer:
    def __init__(self, agent_type, depth):
        self.agent_type = agent_type
        self.depth = depth

    def play_bot_turn(self, screen, game: Game, board: Board, dragger: Dragger, bot_board):
        self._display_game_state(screen, game, dragger)
        if not self._is_game_continuing(board):
            return

        move = self._calculate_bot_move(game, bot_board)
        if move is None:
            return print('Game over')

        self._execute_bot_move(move, bot_board, board, game, screen, dragger)
        print(bot_board)
        print('----------------')
        return bot_board

    def _display_game_state(self, screen, game, dagger):
        game.display_all(screen)
        if dagger.dragging:
            dagger.update_blit(screen)

    @staticmethod
    def _is_game_continuing(board):
        if board is None or board == 'Game over':
            print('Game over')
            return False
        return True

    def _calculate_bot_move(self, game, bot_board):
        agent = self.get_agent(bot_board, game.next_player)
        time_before = datetime.datetime.now()
        move = agent.get_action()
        if move:
            time_after = datetime.datetime.now()
            print('----------------')
            print(f'Bot time: {(time_after - time_before).seconds} seconds')
            print(f'Move Bot: {move}')

        return move

    def _execute_bot_move(self, move, bot_board, board, game, screen, dragger):
        bot_move = chess.Move.from_uci(str(move))
        bot_board.push(bot_move)

        # Correctly split the move into column and row components for both origin and destination
        origin_col, origin_row = str(move)[:2]
        dest_col, dest_row = str(move)[2:4]

        # Assuming translate_to_interface requires separate column and row arguments
        origin = TranslateMove.translate_to_interface(origin_col, origin_row)
        destination = TranslateMove.translate_to_interface(dest_col, dest_row)

        self._simulate_drag_and_drop(origin, destination, board, game, screen, dragger)

    def _simulate_drag_and_drop(self, origin, destination, board, game, screen, dragger):
        event_pos = (origin[0] * 100, origin[1] * 100)
        dragger.update_mouse(event_pos)
        if not board.squares[origin[1]][origin[0]].has_piece():
            return

        piece = board.squares[origin[1]][origin[0]].piece
        if piece.color != game.next_player:
            return
        board.calc_moves(piece, origin[1], origin[0], bool=True)
        dragger.save_initial(event_pos)

        self._perform_drag_drop_operations(piece, origin, destination, board, game, screen, dragger)

    def _perform_drag_drop_operations(self, piece, origin, destination, board, game, screen, dragger):
        dragger.drag_piece(piece)
        game.display_all(screen)

        if not dragger.dragging:
            return

        move = self._create_move(origin, destination)
        if board.valid_move(dragger.piece, move):
            self._execute_move_and_update_game(move, board, game, screen, dragger)
        dragger.undrag_piece()

    @staticmethod
    def _create_move(origin, destination):
        initial = Square(*origin[::-1])
        final = Square(*destination[::-1])
        return Move(initial, final)

    def _execute_move_and_update_game(self, move, board, game, screen, dragger):
        captured = board.squares[move.final.row][move.final.col].has_piece()
        board.move(dragger.piece, move)
        board.set_true_en_passant(dragger.piece)
        game.play_sound(captured)
        game.show_bg(screen)
        game.show_last_move(screen)
        game.show_pieces(screen)
        game.next_turn()

    def get_agent(self, bot_board, next_player):
        if self.agent_type == "MinimaxAgent":
            return agents.MinimaxAgent(bot_board, next_player, self.depth)
        elif self.agent_type == "AlphaBetaAgent":
            return agents.AlphaBetaAgent(bot_board, next_player, self.depth)
        elif self.agent_type == "ExpectimaxAgent":
            return agents.ExpectimaxAgent(bot_board, next_player, self.depth)
        elif self.agent_type == "RandomAgent":
            return agents.RandomAgent(bot_board, next_player)
