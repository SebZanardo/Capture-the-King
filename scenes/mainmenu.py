import pygame
import random

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton
from baseclasses.scenemanager import Scene, SceneManager
from config.constants import WHITE, BACKGROUND
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CENTRE
from config.assets import CHESS_PIECES, GAME_FONT_BIG, GAME_FONT, GAME_FONT_SMALL
from components.button import blit_centered_text
from components.fallingpieces import FallingSprite

# Import the whole module of all scenes you want to switch to
import scenes.game


class MainMenu(Scene):
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
            speed = random.randint(1, 4)
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

        self.title_text = GAME_FONT_BIG.render("CAPTURE", False, WHITE)
        self.title2_text = GAME_FONT.render("THE", False, WHITE)
        self.title3_text = GAME_FONT_BIG.render("KING", False, WHITE)
        self.ludum_text = GAME_FONT_SMALL.render(
            "Made in 72hrs for Ludum Dare 55", False, WHITE
        )
        self.credits_text = GAME_FONT_SMALL.render(
            "Created by Alex, Benjamin and Seb", False, WHITE
        )
        self.play_text = GAME_FONT.render("Click anywhere to play!", False, WHITE)

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if mouse_buffer[MouseButton.LEFT][InputState.PRESSED]:
            self.scene_manager.switch_scene(scenes.game.Game)

    def update(self, dt: float) -> None:
        for piece in self.pieces:
            piece.update(dt)
            if piece.rect.top > WINDOW_HEIGHT:
                piece.rect.bottom = 0

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND)

        for piece in self.pieces:
            surface.blit(piece.image, piece.rect.topleft)

        blit_centered_text(
            surface, self.title_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] - 150
        )
        blit_centered_text(
            surface, self.title2_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] - 80
        )
        blit_centered_text(
            surface, self.title3_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1]
        )
        blit_centered_text(
            surface, self.ludum_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] + 100
        )
        blit_centered_text(
            surface, self.play_text, WINDOW_CENTRE[0], WINDOW_CENTRE[1] + 200
        )

        surface.blit(self.credits_text, (0, 0))
