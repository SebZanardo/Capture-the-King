import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_CENTRE
from config.constants import BACKGROUND, WHITE
from config.assets import GAME_FONT_BIG
from components.button import blit_centered_text

# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Win(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.win_text = GAME_FONT_BIG.render("THE END!", False, WHITE)

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if mouse_buffer[MouseButton.LEFT][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND)

        blit_centered_text(surface, self.win_text, *WINDOW_CENTRE)


