import sys
import platform
import pygame

from config.settings import WINDOW_SETUP, CAPTION
from config.constants import PIECE_WIDTH, PIECE_HEIGHT
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
IMPOSSIBLE_SPIN_FRAMES = slice_sheet("assets/impossible_spin.png", 64, 64)
PIECES = slice_sheet("assets/pieces.png", PIECE_WIDTH, PIECE_HEIGHT)
PIECE_MAP = {
    "P": PIECES[0],
    "N": PIECES[1],
    "B": PIECES[2],
    "R": PIECES[3],
    "Q": PIECES[4],
    "K": PIECES[5],
    "p": PIECES[6],
    "n": PIECES[7],
    "b": PIECES[8],
    "r": PIECES[9],
    "q": PIECES[10],
    "k": PIECES[11],
}


# Load all audio files (Must be .ogg file for browser compatibility)
pass

# Load all font files (Must be .ttf file for brower compatibility)
DEBUG_FONT = pygame.font.Font("assets/joystix.ttf", 10)
