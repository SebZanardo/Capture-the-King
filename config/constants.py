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
LIGHT_SQUARE = pygame.Color(230, 232, 196)
DARK_SQUARE = pygame.Color(146, 99, 65)

FACTION_COLOUR_MAP = {
    Colour.WHITE: WHITE,
    Colour.BLACK: BLACK,
    Colour.RED: pygame.Color(255, 74, 74),
    Colour.BLUE: pygame.Color(96, 182, 255),
    Colour.DEAD: pygame.Color(100, 100, 100),
}
