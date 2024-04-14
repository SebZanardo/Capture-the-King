from typing import Optional
import math
import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SIZE
from config.constants import BACKGROUND, LIGHT_SQUARE, DARK_SQUARE, FACTION_COLOUR_MAP
from components.chess import (
    Colour,
    Piece,
    Move,
    Outcome,
    pick_random_move,
    play_move,
    perform_capture,
)
from components.board_generation import (
    generate_empty_board,
    generate_empty_player_pieces,
    place_pieces_randomly,
)

from config.assets import CHESS_PIECES
from utilities.math import lerp, clamp

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.transparent_colorkey = (255, 0, 255)
        self.transparent_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        self.transparent_surface.set_colorkey(self.transparent_colorkey)

        self.squares = 64
        self.board_size = (8, 8)
        self.square_size = min(
            WINDOW_WIDTH // self.board_size[0], WINDOW_HEIGHT // self.board_size[1]
        )
        self.square_size_tuple = (self.square_size, self.square_size)

        self.scaled_pieces = [
            pygame.transform.scale(sprite, self.square_size_tuple)
            for sprite in CHESS_PIECES
        ]

        self.active_players = [Colour.WHITE, Colour.RED, Colour.BLUE]
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

        # First player (YOU) gets bottom half of board. Opponents get top half divided equally
        self.player_regions: dict[Colour, tuple[int, int, int, int]] = {}
        self.player_regions[self.active_players[0]] = (
            0,
            math.floor(self.board_size[1] / 2),
            self.board_size[0],
            math.ceil(self.board_size[1] / 2),
        )
        divided_width = math.floor(self.board_size[0] / (len(self.active_players) - 1))
        for i in range(1, len(self.active_players)):
            colour = self.active_players[i]
            self.player_regions[colour] = (
                divided_width * (i - 1),
                0,
                divided_width,
                math.floor(self.board_size[1] / 2),
            )

        # NOTE: King must be first in array and only one king allowed (If checking is enabled)
        place_pieces_randomly(
            self.board,
            self.player_pieces,
            Colour.WHITE,
            self.player_regions,
            [Piece.KING, Piece.QUEEN, Piece.QUEEN, Piece.ROOK, Piece.BISHOP],
        )
        place_pieces_randomly(
            self.board,
            self.player_pieces,
            Colour.RED,
            self.player_regions,
            [Piece.KING, Piece.QUEEN, Piece.QUEEN, Piece.ROOK, Piece.BISHOP],
        )
        place_pieces_randomly(
            self.board,
            self.player_pieces,
            Colour.BLUE,
            self.player_regions,
            [Piece.KING, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.KNIGHT],
        )

        self.turn = 0  # Index in self.active_players array
        self.active_player = self.active_players[self.turn]
        self.moves = 0
        self.moves_since_death = 0
        self.max_moves_since_death = 200

        self.starting_speed = 0.2
        self.move_speed = self.starting_speed
        self.move_speed_timer = self.starting_speed

        self.active_move: Move = None
        self.active_piece: Piece = None
        self.active_captured_piece: Optional[Piece] = None
        self.active_piece_x = 0
        self.active_piece_y = 0

        self.gameover = False
        self.outcome = Outcome.DRAW
        self.finished = False

        self.run_simulation = False

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if action_buffer[Action.START][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

        self.clicked = mouse_buffer[MouseButton.LEFT][InputState.PRESSED]

    def update(self, dt: float) -> None:
        if self.clicked:
            self.run_simulation = True

        if self.run_simulation:
            if self.gameover or self.moves_since_death == self.max_moves_since_death:
                if not self.finished:
                    print(self.outcome)
                self.finished = True
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
                    # TODO: Play sound effect for move and capture
                    if self.active_move.capture:
                        pass
                    else:
                        pass

                    self.active_move = None

                    still_alive = []
                    for player, alive in self.alive_players.items():
                        if alive:
                            still_alive.append(player)

                    if self.active_players[0] not in still_alive:
                        self.gameover = True
                        self.outcome = Outcome.LOSE
                        return

                    elif len(still_alive) == 1:
                        self.gameover = True
                        self.outcome = Outcome.WIN
                        return

                # Update turn
                self.active_player = self.active_players[self.turn]

                if self.alive_players[self.active_player]:
                    selected_move = pick_random_move(
                        self.board, self.player_pieces, self.active_player
                    )
                    if selected_move:
                        # Set piece to move
                        self.active_move = selected_move
                        self.active_piece = self.board[
                            (self.active_move.piece_x, self.active_move.piece_y)
                        ]

                        self.active_captured_piece = play_move(
                            self.board,
                            self.player_pieces,
                            self.active_player,
                            self.active_move,
                        )
                        perform_capture(self.player_pieces, self.active_move)

                        self.active_piece_x = self.active_move.piece_x
                        self.active_piece_y = self.active_move.piece_y

                        self.moves += 1
                        self.moves_since_death += 1
                        self.move_speed = self.starting_speed * (
                            1
                            - self.moves_since_death / (self.max_moves_since_death / 4)
                        )
                        self.move_speed = clamp(self.move_speed, 0, self.starting_speed)
                    else:
                        # TODO: Play sound effect player death

                        # Slow down game
                        self.moves_since_death = 0
                        self.move_speed = self.starting_speed
                        self.move_speed_timer = self.move_speed

                        self.alive_players[self.active_player] = False

                self.turn += 1
                self.turn %= len(self.active_players)
                self.move_speed_timer = self.move_speed

    def render(self, surface: pygame.Surface) -> None:
        self.transparent_surface.fill(self.transparent_colorkey)
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

                    # Don't render piece that is moving or piece that is captured
                    if self.active_move and square == (
                        self.active_move.target_x,
                        self.active_move.target_y,
                    ):
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

        # Render captured piece
        if self.active_move and self.active_captured_piece:
            screen_pos = (
                self.active_move.target_x * self.square_size + self.board_offset[0],
                self.active_move.target_y * self.square_size + self.board_offset[1],
            )
            surface.blit(
                self.player_piece_sprites[self.active_move.capture][
                    self.active_captured_piece.value
                ],
                screen_pos,
            )

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

        if not self.run_simulation:
            for colour, region in self.player_regions.items():
                screen_rect = (
                    region[0] * self.square_size + self.board_offset[0],
                    region[1] * self.square_size + self.board_offset[1],
                    region[2] * self.square_size,
                    region[3] * self.square_size,
                )
                colour = FACTION_COLOUR_MAP[colour]
                colour.a = 100
                pygame.draw.rect(self.transparent_surface, colour, screen_rect)

        surface.blit(self.transparent_surface, (0, 0))
