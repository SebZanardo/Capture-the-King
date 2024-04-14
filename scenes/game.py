import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from config.constants import BACKGROUND, LIGHT_SQUARE, DARK_SQUARE
from components.chess import (
    Colour,
    Piece,
    Move,
    generate_empty_board,
    generate_empty_player_pieces,
    place_pieces_randomly,
    pick_random_move,
    remove_piece,
    place_piece,
    perform_capture,
)
from config.assets import CHESS_PIECES
from utilities.math import lerp

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.squares = 100
        self.board_size = (15, 15)
        self.square_size = min(
            WINDOW_WIDTH // self.board_size[0], WINDOW_HEIGHT // self.board_size[1]
        )
        self.square_size_tuple = (self.square_size, self.square_size)

        self.scaled_pieces = [
            pygame.transform.scale(sprite, self.square_size_tuple)
            for sprite in CHESS_PIECES
        ]

        self.active_players = [Colour.RED, Colour.BLUE]
        self.alive_players = {player: True for player in self.active_players}

        self.player_piece_sprites = {}
        for colour in list(Colour):
            coloured_pieces = [
                self.scaled_pieces[colour.value * len(Piece) + i]
                for i in range(len(Piece))
            ]
            self.player_piece_sprites[colour] = coloured_pieces

        self.board_offset = (
            (WINDOW_WIDTH - self.square_size * self.board_size[0]) // 2,
            (WINDOW_HEIGHT - self.square_size * self.board_size[1]) // 2,
        )

        self.board = generate_empty_board(self.squares, *self.board_size)
        self.player_pieces = generate_empty_player_pieces(self.active_players)
        place_pieces_randomly(
            self.board,
            self.player_pieces,
            Colour.RED,
            [Piece.KING, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.KNIGHT],
        )
        place_pieces_randomly(
            self.board,
            self.player_pieces,
            Colour.BLUE,
            [Piece.KING, Piece.QUEEN, Piece.PAWN, Piece.ROOK, Piece.BISHOP],
        )

        self.turn = 0  # Index in self.active_players array
        self.active_player = self.active_players[self.turn]
        self.moves = 0
        self.moves_since_death = 0

        self.starting_move_speed = 0.2
        self.move_speed = self.starting_move_speed
        self.move_speed_timer = self.starting_move_speed

        self.active_move: Move = None
        self.active_piece: Piece = None
        self.active_piece_x = 0
        self.active_piece_y = 0

        self.gameover = False

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if action_buffer[Action.START][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

        self.clicked = mouse_buffer[MouseButton.LEFT][InputState.PRESSED]

    def update(self, dt: float) -> None:
        if self.gameover:
            return

        self.move_speed_timer -= dt
        if self.move_speed_timer > 0 and self.active_move:
            # Lerp piece position
            percent = (self.move_speed - self.move_speed_timer) / self.move_speed

            self.active_piece_x = lerp(
                self.active_move.piece_x,
                self.active_move.target_x,
                percent,
            )
            self.active_piece_y = lerp(
                self.active_move.piece_y,
                self.active_move.target_y,
                percent,
            )

        else:
            if self.active_move:
                # Place piece that was moving
                place_piece(
                    self.board,
                    self.player_pieces,
                    self.active_player,
                    self.active_move,
                    self.active_piece,
                )

                # Perform capture if needed
                captured = perform_capture(self.player_pieces, self.active_move)

                # TODO: Play sound effect for move and capture
                if captured:
                    pass
                else:
                    pass

                self.active_move = None

                # HACK: Until I implement check, checkmate and stalemate
                if not self.alive_players[self.active_players[0]]:
                    self.gameover = True

            # Update turn
            self.active_player = self.active_players[self.turn]

            if self.alive_players[self.active_player]:
                selected_move = pick_random_move(
                    self.board, self.player_pieces, self.active_player
                )
                if selected_move:
                    # Set piece to move
                    self.active_move = selected_move

                    # Remove from board
                    self.active_piece = remove_piece(
                        self.board,
                        self.player_pieces,
                        self.active_player,
                        self.active_move,
                    )

                    self.active_piece_x = self.active_move.piece_x
                    self.active_piece_y = self.active_move.piece_y

                    self.moves += 1
                    self.moves_since_death += 1
                    self.move_speed = max(
                        0, self.starting_move_speed * (1 - self.moves_since_death / 50)
                    )
                else:
                    # TODO: Play sound effect player death

                    # Slow down game
                    self.moves_since_death = 0
                    self.move_speed = self.starting_move_speed
                    self.move_speed_timer = self.move_speed

                    self.alive_players[self.active_player] = False

            self.turn += 1
            self.turn %= len(self.active_players)
            self.move_speed_timer = self.move_speed

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND)
        for square, piece in self.board.items():
            colour = LIGHT_SQUARE if (square[0] + square[1]) % 2 == 0 else DARK_SQUARE
            position = (
                square[0] * self.square_size + self.board_offset[0],
                square[1] * self.square_size + self.board_offset[1],
            )
            pygame.draw.rect(surface, colour, (position, self.square_size_tuple))

            # There is a piece on the square
            if piece is not None:
                for player_colour, piece_squares in self.player_pieces.items():
                    # Skip if piece doesn't belong to this player
                    if square not in piece_squares:
                        continue

                    if self.alive_players[player_colour]:
                        surface.blit(
                            self.player_piece_sprites[player_colour][piece.value],
                            position,
                        )
                    else:
                        surface.blit(
                            self.player_piece_sprites[Colour.DEAD][piece.value],
                            position,
                        )
                    break

        # Render piece moving
        if self.active_move:
            screen_pos = (
                self.active_piece_x * self.square_size + self.board_offset[0],
                self.active_piece_y * self.square_size + self.board_offset[1],
            )
            surface.blit(
                self.player_piece_sprites[self.active_player][self.active_piece.value],
                screen_pos,
            )
