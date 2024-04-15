import sys
import platform
import pygame

from config.settings import WINDOW_SETUP, CAPTION
from utilities.spriteloading import slice_sheet

# -------------------------------- DO NOT MOVE! --------------------------------
# NOTE: Only /config/core.py should be importing window and clock
pygame.init()

if sys.platform == "emscripten":  # If running in browser
    platform.window.canvas.style.imageRendering = "pixelated"
    window = pygame.display.set_mode(WINDOW_SETUP["size"])
else:
    window = pygame.display.set_mode(**WINDOW_SETUP)

clock = pygame.time.Clock()
icon = pygame.image.load("assets/icon.png")

pygame.display.set_icon(icon)
pygame.display.set_caption(CAPTION)
# ------------------------------------------------------------------------------

# Load all sprite files (Ideally .png/.webp or .jpg for browser compatibility)
CHESS_PIECES = slice_sheet("assets/chess_pieces.png", 64, 96)
CHESS_SILHOUETTES = slice_sheet("assets/piece_silhouettes.png", 64, 96)
SOUL_FLAMES = slice_sheet("assets/soul_flames.png", 64, 64)
SOUL_FLAMES = [pygame.transform.scale(sprite, (128, 128)) for sprite in SOUL_FLAMES]

# Load all audio files (Must be .ogg file for browser compatibility)
pass

# Load all font files (Must be .ttf file for brower compatibility)
DEBUG_FONT = pygame.font.Font("assets/joystix.ttf", 10)
GAME_FONT_SMALL = pygame.font.Font("assets/joystix.ttf", 16)
GAME_FONT = pygame.font.Font("assets/joystix.ttf", 32)
GAME_FONT_BIG = pygame.font.Font("assets/joystix.ttf", 100)
