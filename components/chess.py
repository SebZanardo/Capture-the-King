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
    WHITE = 0
    BLACK = auto()
    RED = auto()
    BLUE = auto()


class Piece(Enum):
    PAWN = 0
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
PlayerPieces = dict[Colour, set[tuple[int, int]]]


def generate_empty_board(squares: int, width: int, height: int) -> Board:
    start = (width // 2, height // 2)

    board = {}
    open_squares = [start]
    seen = set()
    seen.add(start)

    iterations = 0
    while open_squares:
        if iterations == squares:
            break
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

        iterations += 1

    if iterations != squares:
        print("Too many squares to fit within bounds!")

    return board


def generate_empty_player_pieces(players: list[Colour]) -> PlayerPieces:
    return {colour: set() for colour in players}


def place_pieces_randomly(
    board: Board, playerpieces: PlayerPieces, colour: Colour, pieces: list[Piece]
) -> None:
    open_squares = []
    for square, piece in board.items():
        if piece is None:
            open_squares.append(square)

    random.shuffle(open_squares)

    for piece in pieces:
        if not open_squares:
            print("Not enough open squares to place pieces!")
            break
        square = open_squares.pop()
        board[square] = piece
        playerpieces[colour].add(square)
