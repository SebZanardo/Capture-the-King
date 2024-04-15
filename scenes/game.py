from typing import Optional
import math
import random
import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SIZE, WINDOW_CENTRE
from config.constants import (
    BACKGROUND,
    LIGHT_SQUARE,
    DARK_SQUARE,
    FACTION_COLOUR_MAP,
    WHITE,
    BLACK,
    EMPTY_SQUARE,
)
from components.chess import (
    Colour,
    Piece,
    Move,
    Outcome,
    pick_random_move,
    play_move,
    perform_capture,
)
from components.boardgeneration import (
    generate_empty_board,
    generate_empty_player_pieces,
    place_pieces_randomly,
    place_king_randomly,
)
from components.animationplayer import AnimationPlayer
from components.button import Button, blit_centered_text
from components.flame import Flame
from config.assets import (
    CHESS_PIECES,
    CHESS_SILHOUETTES,
    SOUL_FLAMES,
    GAME_FONT,
    GAME_FONT_BIG,
    GAME_FONT_SMALL,
)
from components.levels import levels
from utilities.math import lerp, clamp
import scenes.globals as globaldata

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu
import scenes.win


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.transparent_colorkey = (255, 0, 255)
        self.transparent_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        self.transparent_surface.set_colorkey(self.transparent_colorkey)

        # Load current level
        current_level = levels[globaldata.level]
        self.mana_reward = current_level["mana_awarded"]
        self.name = current_level["name"]
        board = current_level["board"]
        self.squares = board[0]
        self.board_size = (board[1], board[2])

        self.square_size = min(
            (WINDOW_WIDTH - 256) // self.board_size[0],
            (WINDOW_HEIGHT - 128) // self.board_size[1],
        )
        self.square_size_tuple = (self.square_size, self.square_size)

        self.piece_size = (self.square_size, self.square_size / 2 * 3)
        scaled_pieces = [
            pygame.transform.scale(sprite, self.piece_size) for sprite in CHESS_PIECES
        ]
        self.piece_offset = (0, -self.piece_size[1] // 2)

        self.active_players = [Colour.WHITE]
        opponents = current_level["opponents"]
        for colour in opponents.keys():
            self.active_players.append(colour)

        self.alive_players = {player: True for player in self.active_players}

        self.player_piece_sprites = {}
        piece_colours = [
            Colour.DEAD,
            Colour.WHITE,
            Colour.BLACK,
            Colour.RED,
            Colour.YELLOW,
            Colour.GREEN,
            Colour.BLUE,
            Colour.PURPLE,
        ]
        for i, colour in enumerate(piece_colours):
            coloured_pieces = [
                scaled_pieces[i * len(Piece) + j] for j in range(len(Piece))
            ]
            self.player_piece_sprites[colour] = coloured_pieces

        self.flames = []
        flame_colours = [
            Colour.BLACK,
            Colour.RED,
            Colour.YELLOW,
            Colour.GREEN,
            Colour.BLUE,
            Colour.PURPLE,
        ]
        flame_colour_to_piece = {
            Colour.BLACK: Piece.KING,
            Colour.RED: Piece.PAWN,
            Colour.YELLOW: Piece.KNIGHT,
            Colour.GREEN: Piece.BISHOP,
            Colour.BLUE: Piece.ROOK,
            Colour.PURPLE: Piece.QUEEN,
        }
        for i, colour in enumerate(flame_colours):
            anim = AnimationPlayer("idle", SOUL_FLAMES[i * 12 : i * 12 + 6], 0.2)
            anim.add_animation("cast", SOUL_FLAMES[i * 12 + 7 : i * 12 + 12], 0.1)
            anim.frame_index = random.randint(0, 4)
            hitbox = Button(
                0, 100 * i + 40, 128, 80
            )  # Offset for removal of king summon
            flame = Flame(hitbox, flame_colour_to_piece[colour], anim)
            self.flames.append(flame)
        self.flames.pop(0)  # Remove king summon

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
            extra = 0
            if i == len(self.active_players) - 1:
                extra = self.board_size[0] - self.board_size[0] // (
                    len(self.active_players) - 1
                ) * (len(self.active_players) - 1)

            colour = self.active_players[i]
            self.player_regions[colour] = (
                divided_width * (i - 1),
                -0.8,
                divided_width + extra,
                math.floor(self.board_size[1] / 2) + 0.8,
            )

        self.piece_silhouette = {}
        silhouette_order = [
            Piece.PAWN,
            Piece.KNIGHT,
            Piece.BISHOP,
            Piece.ROOK,
            Piece.QUEEN,
            Piece.KING,
        ]
        for piece, sprite in zip(silhouette_order, CHESS_SILHOUETTES):
            sprite = pygame.transform.scale(sprite, (32, 48))
            self.piece_silhouette[piece] = sprite

        place_king_randomly(
            self.board,
            self.player_pieces,
            self.active_players[0],
            self.player_regions,
            True,
        )

        for colour, pieces in opponents.items():
            place_king_randomly(
                self.board,
                self.player_pieces,
                colour,
                self.player_regions,
                False,
            )
            place_pieces_randomly(
                self.board,
                self.player_pieces,
                colour,
                self.player_regions,
                pieces,
            )

        self.start_button = Button(
            WINDOW_WIDTH - 128, WINDOW_HEIGHT // 2 - 50, 128, 100
        )

        self.turn = 0  # Index in self.active_players array
        self.active_player = self.active_players[self.turn]
        self.moves = 0
        self.moves_since_death = 0
        self.max_moves_since_death = 200

        self.starting_speed = 0.5
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

        self.player_made_move = True

        self.hovered_flame = None
        self.hovered_square = None

        self.level_text = GAME_FONT.render(f"{self.name}", False, WHITE)
        self.mana_text = GAME_FONT.render(f"{globaldata.mana}", False, WHITE)
        self.fight_complete_text = GAME_FONT.render(
            "FIGHT CONCLUDED", False, WHITE, BLACK
        )
        self.win_text = GAME_FONT_BIG.render("YOU WIN!", False, WHITE, BLACK)
        self.draw_text = GAME_FONT_BIG.render("STALEMATE!", False, WHITE, BLACK)
        self.lose_text = GAME_FONT_BIG.render("YOU LOST!", False, WHITE, BLACK)
        self.restart_text = GAME_FONT.render(
            "CLICK ANYWHERE TO RESTART", False, WHITE, BLACK
        )
        self.continue_text = GAME_FONT.render(
            "CLICK ANYWHERE TO CONTINUE", False, WHITE, BLACK
        )
        self.start_text = GAME_FONT.render("START", False, WHITE)

        self.drag_me_text = GAME_FONT_SMALL.render("DRAG SOULS", False, WHITE)
        self.to_board_text = GAME_FONT_SMALL.render("TO BOARD", False, WHITE)
        self.mana_word_text = GAME_FONT_SMALL.render("MANA", False, WHITE)
        self.remaining_text = GAME_FONT_SMALL.render("REMAINING", False, WHITE)
        self.summon_text = GAME_FONT_SMALL.render("TO SUMMON", False, WHITE)

        self.summon_flames_vfx: dict[Piece, tuple[tuple[int, int], AnimationPlayer]] = (
            {}
        )
        for i, colour in enumerate(flame_colours):
            frames = SOUL_FLAMES[i * 12 : i * 12 + 6]
            final_frames = [
                pygame.transform.scale(f, self.square_size_tuple) for f in frames
            ]
            for i in range(len(frames)):
                final_frames[i].set_alpha(clamp(i * (255 / (len(frames) - 1)), 0, 255))

            final_frames.reverse()
            animation = AnimationPlayer("cast", final_frames, 0.1, False)
            self.summon_flames_vfx[flame_colour_to_piece[colour]] = (
                (-1000, -1000),
                animation,
            )

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        self.clicked = mouse_buffer[MouseButton.LEFT][InputState.PRESSED]
        self.dragging = mouse_buffer[MouseButton.LEFT][InputState.HELD]
        self.released = mouse_buffer[MouseButton.LEFT][InputState.RELEASED]

    def update(self, dt: float) -> None:
        mouse_position = pygame.mouse.get_pos()

        if self.moves_since_death == self.max_moves_since_death:
            self.gameover = True

        if self.gameover:
            if not self.finished:
                print(self.outcome)
            self.finished = True

            if self.clicked:
                if self.outcome == Outcome.WIN:
                    globaldata.level += 1
                    globaldata.mana += self.mana_reward
                    if globaldata.level >= len(levels):
                        globaldata.level = 0
                        globaldata.mana = globaldata.starting_mana
                        self.scene_manager.switch_scene(scenes.win.Win)
                        return
                    else:
                        self.scene_manager.switch_scene(Game)
                elif self.outcome == Outcome.DRAW or self.outcome == Outcome.LOSE:
                    globaldata.level = 0
                    globaldata.mana = globaldata.starting_mana
                    self.scene_manager.switch_scene(Game)
            return

        if self.run_simulation:
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

                    # A player just lost... lol
                    if self.active_captured_piece == Piece.KING:
                        # TODO: Play sound effect player death
                        self.alive_players[self.active_move.capture] = False
                        self.moves_since_death = 0
                        self.move_speed = self.starting_speed
                        self.move_speed_timer = self.move_speed

                    self.active_move = None

                # Update turn
                self.active_player = self.active_players[self.turn]

                # Stalemate (No piece made a move for any player for a turn)
                if (
                    self.active_player == self.active_players[0]
                    and not self.player_made_move
                ):
                    self.gameover = True

                if self.active_player == self.active_players[0]:
                    self.player_made_move = False

                if self.alive_players[self.active_player]:
                    selected_move = pick_random_move(
                        self.board, self.player_pieces, self.active_player
                    )
                    if selected_move:
                        self.player_made_move = True

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
                        # Can't make move
                        # self.alive_players[self.active_player] = False
                        pass

                self.turn += 1
                self.turn %= len(self.active_players)
                self.move_speed_timer = self.move_speed

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
        else:
            inside = False

            for pair in self.summon_flames_vfx.values():
                pair[1].update(dt)

            for flame in self.flames:
                flame.animation.update(dt)
                if globaldata.mana < flame.summon_cost:
                    continue

                if flame.hitbox.inside(*mouse_position):
                    if self.hovered_flame != flame:
                        if self.hovered_flame is not None:
                            self.hovered_flame.animation.switch_animation("idle")
                        self.hovered_flame = flame
                        self.hovered_flame.animation.switch_animation("cast")
                    inside = True

            self.hovered_square = None

            # Attempt summon of piece
            if self.hovered_flame is not None:
                # Find square we are over
                square = (
                    (mouse_position[0] - self.board_offset[0]) // self.square_size,
                    (mouse_position[1] - self.board_offset[1]) // self.square_size,
                )
                # If square inside player's region
                region = self.player_regions[self.active_players[0]]
                if (
                    square[0] >= region[0]
                    and square[0] < region[0] + region[2]
                    and square[1] >= region[1]
                    and square[1] < region[1] + region[3]
                ):
                    # If square not occupied or non-existant
                    if square in self.board and self.board[square] is None:
                        self.hovered_square = square
                        # If mouse released
                        if self.released:
                            piece_type = self.hovered_flame.piece_type
                            self.board[square] = piece_type
                            self.player_pieces[self.active_players[0]].append(square)
                            globaldata.mana -= self.hovered_flame.summon_cost
                            self.mana_text = GAME_FONT.render(
                                f"{globaldata.mana}", False, WHITE
                            )

                            pos, anim = self.summon_flames_vfx[piece_type]

                            position = (
                                square[0] * self.square_size + self.board_offset[0],
                                square[1] * self.square_size + self.board_offset[1],
                            )
                            anim.reset()
                            self.summon_flames_vfx[piece_type] = (position, anim)

            if not self.dragging and not inside and self.hovered_flame is not None:
                self.hovered_flame.animation.switch_animation("idle")
                self.hovered_flame = None

            if self.clicked and self.start_button.inside(*mouse_position):
                self.run_simulation = True

    def render(self, surface: pygame.Surface) -> None:
        self.transparent_surface.fill(self.transparent_colorkey)
        surface.fill(BACKGROUND)

        background_rect = (
            self.board_offset[0],
            self.board_offset[1],
            self.board_size[0] * self.square_size,
            self.board_size[1] * self.square_size,
        )
        pygame.draw.rect(surface, EMPTY_SQUARE, background_rect)

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

                    piece_screen_pos = (
                        square[0] * self.square_size
                        + self.board_offset[0]
                        + self.piece_offset[0],
                        square[1] * self.square_size
                        + self.board_offset[1]
                        + self.piece_offset[1],
                    )
                    if self.alive_players[player_colour]:
                        surface.blit(
                            self.player_piece_sprites[player_colour][piece.value],
                            piece_screen_pos,
                        )
                    else:
                        surface.blit(
                            self.player_piece_sprites[Colour.DEAD][piece.value],
                            piece_screen_pos,
                        )
                    break

        # Render captured piece
        if self.active_move and self.active_captured_piece:
            screen_pos = (
                self.active_move.target_x * self.square_size
                + self.board_offset[0]
                + self.piece_offset[0],
                self.active_move.target_y * self.square_size
                + self.board_offset[1]
                + self.piece_offset[1],
            )
            if self.alive_players[self.active_move.capture]:
                surface.blit(
                    self.player_piece_sprites[self.active_move.capture][
                        self.active_captured_piece.value
                    ],
                    screen_pos,
                )
            else:
                surface.blit(
                    self.player_piece_sprites[Colour.DEAD][
                        self.active_captured_piece.value
                    ],
                    screen_pos,
                )

        # Render piece moving
        if self.active_move:
            screen_pos = (
                self.active_piece_x * self.square_size
                + self.board_offset[0]
                + self.piece_offset[0],
                self.active_piece_y * self.square_size
                + self.board_offset[1]
                + self.piece_offset[1],
            )
            surface.blit(
                self.player_piece_sprites[self.active_player][self.active_piece.value],
                screen_pos,
            )

        if not self.run_simulation:
            if self.hovered_square and self.hovered_flame:
                square_pos = (
                    self.hovered_square[0] * self.square_size + self.board_offset[0],
                    self.hovered_square[1] * self.square_size + self.board_offset[1],
                )
                pygame.draw.rect(surface, WHITE, (square_pos, self.square_size_tuple))

                piece_screen_pos = (
                    self.hovered_square[0] * self.square_size
                    + self.board_offset[0]
                    + self.piece_offset[0],
                    self.hovered_square[1] * self.square_size
                    + self.board_offset[1]
                    + self.piece_offset[1],
                )
                piece_sprite = self.player_piece_sprites[self.active_players[0]][
                    self.hovered_flame.piece_type.value
                ]
                surface.blit(piece_sprite, piece_screen_pos)

            for piece, pair in self.summon_flames_vfx.items():
                position, anim = pair
                surface.blit(anim.get_frame(), position)

            for colour, region in self.player_regions.items():
                if colour == self.active_players[0]:
                    continue
                screen_rect = (
                    region[0] * self.square_size + self.board_offset[0],
                    region[1] * self.square_size + self.board_offset[1],
                    region[2] * self.square_size,
                    region[3] * self.square_size,
                )
                colour = FACTION_COLOUR_MAP[colour]
                colour.a = 100
                pygame.draw.rect(
                    self.transparent_surface,
                    colour,
                    screen_rect,
                )

            self.start_button.render(surface, DARK_SQUARE, None)
            blit_centered_text(surface, self.start_text, *self.start_button.center)

            for i, flame in enumerate(self.flames):
                i = i + 1
                surface.blit(flame.animation.get_frame(), (0, 100 * i))
                surface.blit(
                    self.piece_silhouette[flame.piece_type], (40, 100 * i + 40)
                )
                blit_centered_text(surface, flame.summon_text, 80, 100 * i + 70)

            blit_centered_text(surface, self.mana_text, 64, 50)
            blit_centered_text(surface, self.mana_word_text, 64, 75)
            blit_centered_text(surface, self.remaining_text, 64, 90)

            # Only show if first level
            if globaldata.level == 0:
                blit_centered_text(surface, self.drag_me_text, 68, 650)
                blit_centered_text(surface, self.to_board_text, 68, 665)
                blit_centered_text(surface, self.summon_text, 68, 680)

        surface.blit(self.transparent_surface, (0, 0))

        if self.gameover:
            blit_centered_text(
                surface,
                self.fight_complete_text,
                WINDOW_CENTRE[0],
                WINDOW_CENTRE[1] - 80,
            )
            if self.outcome == Outcome.WIN:
                blit_centered_text(
                    surface,
                    self.win_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1],
                )
                blit_centered_text(
                    surface,
                    self.continue_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1] + 70,
                )
            elif self.outcome == Outcome.DRAW:
                blit_centered_text(
                    surface,
                    self.draw_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1],
                )
                blit_centered_text(
                    surface,
                    self.restart_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1] + 70,
                )
            elif self.outcome == Outcome.LOSE:
                blit_centered_text(
                    surface,
                    self.lose_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1],
                )
                blit_centered_text(
                    surface,
                    self.restart_text,
                    WINDOW_CENTRE[0],
                    WINDOW_CENTRE[1] + 70,
                )
        blit_centered_text(
            surface,
            self.level_text,
            WINDOW_CENTRE[0],
            WINDOW_HEIGHT - 34,
        )
