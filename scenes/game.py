import pygame
import pygame.macosx

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from config.constants import (
    WHITE,
    MAGENTA,
    LIGHT_SQUARE,
    DARK_SQUARE,
    SQUARE_WIDTH,
    SQUARE_HEIGHT,
)
from config.assets import PIECE_MAP
from elements.chess import Board, position_to_square

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)
        self.open_cells = [[True for x in range(8)] for y in range(8)]
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.board_offset_x = (WINDOW_WIDTH - SQUARE_WIDTH * 8) // 2
        self.board_offset_y = (WINDOW_HEIGHT - SQUARE_HEIGHT * 8) // 2

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if action_buffer[Action.START][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

    def update(self, dt: float) -> None:
        mouse_position = pygame.mouse.get_pos()
        self.hovered_square = (
            int((mouse_position[0] - self.board_offset_x) / SQUARE_WIDTH),
            int((mouse_position[1] - self.board_offset_y) / SQUARE_HEIGHT),
        )

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(WHITE)
        for y in range(8):
            for x in range(8):
                if not self.open_cells[y][x]:
                    continue

                # Draw square
                square_colour = LIGHT_SQUARE if (x + y) % 2 == 0 else DARK_SQUARE
                square_rect = (
                    x * SQUARE_WIDTH + self.board_offset_x,
                    y * SQUARE_HEIGHT + self.board_offset_y,
                    SQUARE_WIDTH,
                    SQUARE_HEIGHT,
                )
                pygame.draw.rect(surface, square_colour, square_rect)

                # Draw piece if a piece is on this square
                piece = self.board.get_piece(x, y)
                if piece:
                    surface.blit(PIECE_MAP[piece], square_rect)

        if self.hovered_square[0] in range(0, 8) and self.hovered_square[1] in range(0, 8):
            square_rect = (
                self.hovered_square[0] * SQUARE_WIDTH + self.board_offset_x,
                self.hovered_square[1] * SQUARE_HEIGHT + self.board_offset_y,
                SQUARE_WIDTH,
                SQUARE_HEIGHT,
            )
            pygame.draw.rect(surface, MAGENTA, square_rect, 5)
