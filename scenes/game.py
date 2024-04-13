import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from config.constants import BACKGROUND, LIGHT_SQUARE, DARK_SQUARE
from components.chess import (
    Colour,
    Piece,
    generate_empty_board,
    generate_empty_player_pieces,
    place_pieces_randomly,
    play_random_move,
)
from config.assets import PIECES

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.squares = 40
        self.board_size = (25, 8)
        self.square_size = min(
            WINDOW_WIDTH // self.board_size[0], WINDOW_HEIGHT // self.board_size[1]
        )
        self.square_size_tuple = (self.square_size, self.square_size)

        self.scaled_pieces = [
            pygame.transform.scale(sprite, self.square_size_tuple) for sprite in PIECES
        ]

        self.active_players = [Colour.RED, Colour.BLUE]

        self.player_piece_sprites = {}
        for colour in self.active_players:
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
        self.move_speed = 0.2
        self.move_speed_timer = 0

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if action_buffer[Action.START][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

        self.clicked = mouse_buffer[MouseButton.LEFT][InputState.PRESSED]

    def update(self, dt: float) -> None:
        self.move_speed_timer -= dt
        if self.move_speed_timer < 0:
            player = self.active_players[self.turn]

            # HACK: Move a piece if a player still has pieces on the board
            if self.player_pieces[player]:
                play_random_move(self.board, self.player_pieces, player)

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

                    surface.blit(
                        self.player_piece_sprites[player_colour][piece.value],
                        position,
                    )
                    break
