from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
import random


class Colour(Enum):
    WHITE = 0
    BLACK = auto()
    RED = auto()
    BLUE = auto()
    DEAD = auto()  # Keep at end for grey pieces


class Outcome(Enum):
    WIN = auto()
    DRAW = auto()
    LOSE = auto()


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


KNIGHT_MOVES = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1))
BISHOP_DIRECTIONS = ((1, 1), (1, -1), (-1, -1), (-1, 1))
ROOK_DIRECTIONS = ((0, 1), (0, -1), (-1, 0), (1, 0))
QUEEN_DIRECTIONS = (
    (0, 1),
    (0, -1),
    (-1, 0),
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
)
KING_MOVES = ((0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def generate_pseudo_moves(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour
) -> list[Move]:
    moves = []

    for piece_square in player_pieces[player_colour]:
        piece = board[piece_square]
        moves += generate_piece_moves(
            board, player_pieces, player_colour, piece, *piece_square
        )

    return moves


def generate_piece_moves(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    piece: Piece,
    x: int,
    y: int,
) -> list[Move]:
    match (piece):
        case Piece.PAWN:
            d = -1 if player_colour == list(player_pieces.keys())[0] else 1
            return get_pawn_moves(board, player_pieces, player_colour, x, y, d)

        case Piece.KNIGHT:
            return get_set_moves(
                board, player_pieces, player_colour, x, y, KNIGHT_MOVES
            )

        case Piece.BISHOP:
            return get_sliding_moves(
                board, player_pieces, player_colour, x, y, BISHOP_DIRECTIONS
            )

        case Piece.ROOK:
            return get_sliding_moves(
                board, player_pieces, player_colour, x, y, ROOK_DIRECTIONS
            )

        case Piece.QUEEN:
            return get_sliding_moves(
                board, player_pieces, player_colour, x, y, QUEEN_DIRECTIONS
            )

        case Piece.KING:
            return get_set_moves(board, player_pieces, player_colour, x, y, KING_MOVES)


def find_piece_colour(player_pieces: PlayerPieces, x: int, y: int) -> Optional[Colour]:
    for colour, squares in player_pieces.items():
        # Skip if player piece doesn't belong to them
        if (x, y) not in squares:
            continue

        # Found which player the piece belongs to
        return colour

    return None


def get_pawn_moves(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    x: int,
    y: int,
    direction: int,
) -> list[Move]:
    moves = []

    new_x = x
    new_y = y + direction
    # If square inside board and empty
    if (new_x, new_y) in board and board[(new_x, new_y)] is None:
        moves.append(Move(x, y, new_x, new_y, None))
    # Captures
    new_x = x + 1
    if (new_x, new_y) in board:
        piece_colour = find_piece_colour(player_pieces, new_x, new_y)
        if piece_colour is not None and piece_colour != player_colour:
            moves.append(Move(x, y, new_x, new_y, piece_colour))

    new_x = x - 1
    if (new_x, new_y) in board:
        piece_colour = find_piece_colour(player_pieces, new_x, new_y)
        if piece_colour is not None and piece_colour != player_colour:
            moves.append(Move(x, y, new_x, new_y, piece_colour))

    return moves


def get_set_moves(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    x: int,
    y: int,
    set_moves: tuple[tuple[int, int]],
) -> list[Move]:
    moves = []

    for set_move in set_moves:
        new_x = x + set_move[0]
        new_y = y + set_move[1]

        # Skip if square is not on board
        if (new_x, new_y) not in board:
            continue

        piece = board[(new_x, new_y)]

        # Add as move
        if piece is None:
            moves.append(Move(x, y, new_x, new_y, None))

        # Find if valid capture (i.e not one of your team's pieces)
        else:
            piece_colour = find_piece_colour(player_pieces, new_x, new_y)
            if piece_colour != player_colour:
                moves.append(Move(x, y, new_x, new_y, piece_colour))

    return moves


def get_sliding_moves(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    x: int,
    y: int,
    directions: tuple[tuple[int, int]],
) -> list[Move]:
    moves = []

    for direction in directions:
        new_x = x + direction[0]
        new_y = y + direction[1]

        # Keep moving in direction until not on board or ontop of piece
        while (new_x, new_y) in board and board[(new_x, new_y)] is None:
            moves.append(Move(x, y, new_x, new_y, None))
            new_x += direction[0]
            new_y += direction[1]

        # Find if can capture piece
        if (new_x, new_y) in board:
            piece_colour = find_piece_colour(player_pieces, new_x, new_y)
            if piece_colour != player_colour:
                moves.append(Move(x, y, new_x, new_y, piece_colour))

    return moves


def remove_piece(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour, move: Move
) -> Optional[Piece]:
    piece = board[(move.piece_x, move.piece_y)]

    board[(move.piece_x, move.piece_y)] = None
    player_pieces[player_colour].remove((move.piece_x, move.piece_y))

    return piece


def place_piece(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    move: Move,
    piece: Piece,
) -> None:
    board[(move.target_x, move.target_y)] = piece
    player_pieces[player_colour].add((move.target_x, move.target_y))


def perform_capture(player_pieces: PlayerPieces, move: Move) -> None:
    if move.capture is not None:
        player_pieces[move.capture].remove((move.target_x, move.target_y))


def pick_random_move(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour
) -> Optional[Move]:
    possible_moves = generate_pseudo_moves(board, player_pieces, player_colour)

    # Prioritise captures over regular moves
    captures = []
    for move in possible_moves:
        if move.capture:
            captures.append(move)

    if captures:
        return random.choice(captures)
    elif possible_moves:
        return random.choice(possible_moves)
    else:
        return None
