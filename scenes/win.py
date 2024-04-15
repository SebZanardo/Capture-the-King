import random
import pygame

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton
from baseclasses.scenemanager import Scene, SceneManager
from config.settings import WINDOW_CENTRE, WINDOW_HEIGHT, WINDOW_WIDTH
from config.constants import WHITE, BACKGROUND
from config.assets import GAME_FONT_BIG, GAME_FONT, CHESS_PIECES
from components.button import blit_centered_text
from components.fallingpieces import FallingSprite
# Import the whole module of all scenes you want to switch to
import scenes.mainmenu


class Win(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)

        self.square_size = 100
        self.piece_size = (self.square_size, self.square_size / 2 * 3)
        self.scaled_pieces = [
            pygame.transform.scale(sprite, self.piece_size) for sprite in CHESS_PIECES
        ]
        self.piece_offset = (0, -self.piece_size[1] // 2)
        falling_pieces = self.scaled_pieces
        self.pieces = []
        for i, image in enumerate(falling_pieces):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            speed = random.randint(1, 4) * 50
            # trust
            rotate_speed = random.randint(25, 50) * random.choice((1, -1))
            self.pieces.append(
                FallingSprite(
                    image=image,
                    pos_x=x,
                    pos_y=y,
                    speed=speed,
                    rotate_speed=rotate_speed,
                )
            )

        self.win_text = GAME_FONT_BIG.render("THE END!", False, WHITE)
        self.thanks_text = GAME_FONT.render(
            "thanks for playing our Ludum Dare entry", False, WHITE
        )
        self.enjoy_text = GAME_FONT.render(
            "we hope you enjoyed Capture the King", False, WHITE
        )

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if mouse_buffer[MouseButton.LEFT][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.mainmenu.MainMenu)

    def update(self, dt: float) -> None:
        for piece in self.pieces:
            piece.update(dt)
            if piece.rect.top > WINDOW_HEIGHT:
                piece.rect.bottom = 0

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND)

        for piece in self.pieces:
            surface.blit(piece.image, piece.rect.topleft)

        blit_centered_text(surface, self.win_text, *WINDOW_CENTRE)
        blit_centered_text(
            surface, self.thanks_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] + 70
        )
        blit_centered_text(
            surface, self.enjoy_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] + 100
        )
