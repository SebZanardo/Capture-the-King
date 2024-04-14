import pygame
from components.chess import Colour


# Colour constants
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)
CYAN = pygame.Color(0, 255, 255)
BLUE = pygame.Color(0, 0, 255)
MAGENTA = pygame.Color(255, 0, 255)

BACKGROUND = pygame.Color(50, 50, 50)
LIGHT_SQUARE = pygame.Color(200, 200, 200)
DARK_SQUARE = pygame.Color(150, 150, 150)

FACTION_COLOUR_MAP = {
    Colour.WHITE: WHITE,
    Colour.BLACK: BLACK,
    Colour.DEAD: pygame.Color(100, 100, 100),
    Colour.RED: pygame.Color(216, 72, 72),
    Colour.YELLOW: pygame.Color(215, 171, 68),
    Colour.GREEN: pygame.Color(137, 217, 78),
    Colour.BLUE: pygame.Color(75, 158, 217),
    Colour.PURPLE: pygame.Color(184, 73, 216),
}
