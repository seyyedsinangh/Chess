import argparse
import time

import chess
import pygame
import sys

from game import Game
from square import Square
from move import Move
from bot_player import BotPlayer
from const import WIDTH, HEIGHT, SQSIZE
from translate_move import TranslateMove


class MainPlayerVsBot:
    def __init__(self, agent_type, depth):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.bot_board = chess.Board()
        self.botPlayer = BotPlayer(agent_type=agent_type, depth=depth)
        print("nciciicnc")

    def display_game_state(self):
        self.game.show_bg(self.screen)
        self.game.show_last_move(self.screen)
        self.game.show_moves(self.screen)
        self.game.show_pieces(self.screen)
        self.game.show_hover(self.screen)
        if self.game.dragger.dragging:
            self.game.dragger.update_blit(self.screen)

    def process_mouse_motion(self, event):
        motion_row, motion_col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
        if 0 <= motion_row <= 7 and 0 <= motion_col <= 7:
            self.game.set_hover(motion_row, motion_col)
            if self.game.dragger.dragging:
                self.game.dragger.update_mouse(event.pos)
                self.display_game_state()

    def process_mouse_button_down(self, event):
        self.game.dragger.update_mouse(event.pos)
        clicked_row, clicked_col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
        if 0 <= clicked_row <= 7 and 0 <= clicked_col <= 7 and self.game.board.squares[clicked_row][
            clicked_col].has_piece():
            piece = self.game.board.squares[clicked_row][clicked_col].piece
            if piece.color == self.game.next_player:
                self.game.board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                self.game.dragger.save_initial(event.pos)
                self.game.dragger.drag_piece(piece)
                self.display_game_state()

    def process_mouse_button_up(self, event):
        if self.game.dragger.dragging:
            self.game.dragger.update_mouse(event.pos)
            released_row, released_col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
            if 0 <= released_row <= 7 and 0 <= released_col <= 7:
                initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                final = Square(released_row, released_col)
                move = Move(initial, final)
                if self.game.board.valid_move(self.game.dragger.piece, move):
                    self.execute_move(move, released_row, released_col)
                    origin_location = TranslateMove.translate_to_chesslib(self.game.dragger.initial_col,
                                                                          self.game.dragger.initial_row)
                    destine_location = TranslateMove.translate_to_chesslib(released_col, released_row)
                    move = f'{origin_location}{destine_location}'
                    is_game_over = self.bot_board.outcome()
                    if is_game_over:
                        print('Game over')
                        return
                    else:
                        move = chess.Move.from_uci(str(move))
                        self.bot_board.push(move)
                        print('----------------')
                        print('Person move: ', str(move))
                        print(self.bot_board)
                        print('----------------')
            self.game.dragger.undrag_piece()
            self.display_game_state()

            if self.bot_board is None:
                pygame.quit()
                sys.exit()

    def execute_move(self, move, released_row, released_col):
        captured = self.game.board.squares[released_row][released_col].has_piece()
        self.game.board.move(self.game.dragger.piece, move)
        self.game.board.set_true_en_passant(self.game.dragger.piece)
        self.game.play_sound(captured)
        self.display_game_state()
        self.game.next_turn()

    def process_key_down(self, event):
        if event.key == pygame.K_t:
            self.game.change_theme()
        elif event.key == pygame.K_r:
            self.game.reset()

    def check_game_over(self):
        if self.bot_board.is_game_over():
            print('Game over')
            pygame.quit()
            sys.exit()

    def play_bot_turn(self):
        if self.game.next_player == 'black':
            self.bot_board = self.botPlayer.play_bot_turn(self.screen, self.game, self.game.board, self.game.dragger,
                                                          self.bot_board)
            self.check_game_over()

    def mainloop(self):
        bot_started = self.game.next_player == 'black'
        while not self.bot_board.is_game_over():
            self.display_game_state()
            if not bot_started:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        self.process_mouse_motion(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.process_mouse_button_down(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.process_mouse_button_up(event)
                        bot_started = self.game.next_player == 'black'
                    elif event.type == pygame.KEYDOWN:
                        self.process_key_down(event)
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                self.play_bot_turn()
                bot_started = self.game.next_player == 'black'
            pygame.display.update()


class MainBotVsBot:
    def __init__(self, main_agent_type, main_agent_depth, second_agent_type, second_agent_depth):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.bot_board = chess.Board()
        self.botPlayer1 = BotPlayer(agent_type=main_agent_type,
                                    depth=main_agent_depth)  # Initialized with the first bot's strategy and depth
        self.botPlayer2 = BotPlayer(agent_type=second_agent_type,
                                    depth=second_agent_depth)  # # Initialized with the second bot's strategy and depth

    def display_game_state(self):
        self.game.show_bg(self.screen)
        self.game.show_last_move(self.screen)
        self.game.show_moves(self.screen)
        self.game.show_pieces(self.screen)
        self.game.show_hover(self.screen)
        if self.game.dragger.dragging:
            self.game.dragger.update_blit(self.screen)

    def play_bot_turn(self, bot_player):
        """Let the given bot player make a move."""
        if not self.bot_board.is_game_over():
            print(f'{self.game.next_player} Turn')
            self.bot_board = bot_player.play_bot_turn(self.screen, self.game, self.game.board, self.game.dragger,
                                                      self.bot_board)

            self.display_game_state()
            pygame.display.update()
            self.check_game_over()

    def check_game_over(self):
        """Check if the game has ended and handle the game over logic."""
        if self.bot_board is None:
            winner = 'white' if self.game.next_player == 'black' else 'black'
            print(f'Winner is {winner}')
            time.sleep(3)
            pygame.quit()
            sys.exit()

        if self.bot_board.is_game_over():
            print('Game over')
            result = self.bot_board.result()
            print(f'Result: {result}')
            time.sleep(3)
            pygame.quit()
            sys.exit()

    def mainloop(self):
        while not self.bot_board.is_game_over():
            self.display_game_state()
            if self.game.next_player == 'white':
                self.play_bot_turn(self.botPlayer1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                self.play_bot_turn(self.botPlayer2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            time.sleep(0.5)


parser = argparse.ArgumentParser(description='Chess AI configuration')
parser.add_argument('-af', '--main-agent', default='RandomAgent',
                    help='The main agent to use for the game.')
parser.add_argument('-as', '--second-agent', default='RandomAgent',
                    help='The second agent to use for the game.')
parser.add_argument('-df', '--main-agent-depth', type=int, default=2, help='Search depth for the main agent.')
parser.add_argument('-ds', '--second-agent-depth', type=int, default=2, help='Search depth for the second agent.')
parser.add_argument('-p', '--play-type', default="PlayerVsBot", help='Play type: PlayerVsBot or BotVsBot.')
args = parser.parse_args()

if __name__ == "__main__":
    print("Configuring game...")

    if args.play_type == 'PlayerVsBot':
        print("Starting Player vs Bot...")
        # Assuming MainPlayerVsBot is correctly defined elsewhere
        main = MainPlayerVsBot(agent_type=args.main_agent, depth=args.main_agent_depth)
        main.mainloop()

    elif args.play_type == 'BotVsBot':
        print("Starting Bot vs Bot...")
        # Assuming MainBotVsBot is correctly defined elsewhere
        main = MainBotVsBot(main_agent_type=args.main_agent, main_agent_depth=args.main_agent_depth,
                            second_agent_type=args.second_agent, second_agent_depth=args.second_agent_depth)
        main.mainloop()
