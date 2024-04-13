"""
Colour: Enum
Piece: Enum
Move: from: tuple[int, int], to: tuple[int, int], capture: Optional[Colour]
Board: dict[tuple[int, int], Optional[Piece]]
Pieces: dict[colour, set[tuple[int, int]]]
"""

from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
import random


class Colour(Enum):
    WHITE = auto()
    BLACK = auto()


class Piece(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


@dataclass(frozen=True)
class Move:
    piece_x: int
    piece_y: int
    target_x: int
    target_y: int
    capture: Optional[Colour]


Board = dict[tuple[int, int], Optional[Piece]]
Pieces = dict[Colour, set[tuple[int, int]]]


def generate_board(squares: int, width: int, height: int) -> Board:
    start = (width // 2, height // 2)

    board = {}
    open_squares = [start]
    seen = set()
    seen.add(start)

    for i in range(squares):
        # Pick random open square
        square = open_squares.pop(random.randint(0, len(open_squares) - 1))
        board[square] = None

        # Check neighbouring cells
        for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            adjacent = (square[0] + direction[0], square[1] + direction[1])

            # Outside of board bounds
            if (
                adjacent[0] < 0
                or adjacent[0] >= width
                or adjacent[1] < 0
                or adjacent[1] >= height
            ):
                continue

            # If an unvisited square
            if adjacent not in seen:
                open_squares.append(adjacent)

            seen.add(adjacent)

    return board
