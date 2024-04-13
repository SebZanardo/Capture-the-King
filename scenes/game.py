import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from config.constants import BACKGROUND, LIGHT_SQUARE, DARK_SQUARE
from components.chess import generate_board
# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Game(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.tiles = 65
        self.board_size = (8, 8)

        self.square_size = min(
            WINDOW_WIDTH // self.board_size[0], WINDOW_HEIGHT // self.board_size[1]
        )
        self.board_offset = (
            (WINDOW_WIDTH - self.square_size * self.board_size[0]) // 2,
            (WINDOW_HEIGHT - self.square_size * self.board_size[1]) // 2,
        )

        self.board = generate_board(self.tiles, *self.board_size)

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if action_buffer[Action.START][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

        self.clicked = mouse_buffer[MouseButton.LEFT][InputState.PRESSED]

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND)
        for square in self.board:
            colour = LIGHT_SQUARE if (square[0] + square[1]) % 2 == 0 else DARK_SQUARE
            rect = (
                square[0] * self.square_size + self.board_offset[0],
                square[1] * self.square_size + self.board_offset[1],
                self.square_size,
                self.square_size,
            )
            pygame.draw.rect(surface, colour, rect)
