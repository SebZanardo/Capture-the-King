from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass
import random


class Colour(Enum):
    WHITE = 0
    BLACK = auto()
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    PURPLE = auto()
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
PlayerPieces = dict[Colour, list[tuple[int, int]]]


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


def find_legal_moves(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    pseudo_moves: list[Move],
) -> list[Move]:
    legal_moves = []

    for move in pseudo_moves:
        if is_legal(board, player_pieces, player_colour, move):
            legal_moves.append(move)

    return legal_moves


def is_legal(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    move: Move,
) -> bool:
    legal = True

    # Play move on board
    target_piece = play_move(board, player_pieces, player_colour, move)
    capture_index = perform_capture(player_pieces, move)

    king_x, king_y = player_pieces[player_colour][0]

    # Go through each piece belonging to opponents
    for colour, piece_positions in player_pieces.items():
        if colour == player_colour:
            continue

        for piece_position in piece_positions:
            # Find if any of that piece's possible captures is our king
            piece = board[piece_position]
            moves = generate_piece_moves(
                board, player_pieces, colour, piece, *piece_position
            )
            captures = find_captures(moves)

            # If piece can capture king, player is in check and move is illegal
            for capture in captures:
                if capture.target_x == king_x and capture.target_y == king_y:
                    legal = False
                    break

            if not legal:
                break

        if not legal:
            break

    # Unplay move on board
    undo_move(board, player_pieces, player_colour, move, target_piece)
    undo_capture(player_pieces, move, capture_index)

    return legal


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
            return []
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


def play_move(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour, move: Move
) -> Optional[Piece]:
    target_piece = board[(move.target_x, move.target_y)]
    board[(move.target_x, move.target_y)] = board[(move.piece_x, move.piece_y)]
    board[(move.piece_x, move.piece_y)] = None

    i = player_pieces[player_colour].index((move.piece_x, move.piece_y))
    player_pieces[player_colour][i] = (move.target_x, move.target_y)

    return target_piece


def undo_move(
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    move: Move,
    target_piece: Optional[Piece],
) -> None:
    board[(move.piece_x, move.piece_y)] = board[(move.target_x, move.target_y)]
    board[(move.target_x, move.target_y)] = target_piece

    i = player_pieces[player_colour].index((move.target_x, move.target_y))
    player_pieces[player_colour][i] = (move.piece_x, move.piece_y)


def perform_capture(player_pieces: PlayerPieces, move: Move) -> Optional[int]:
    if move.capture is not None:
        index = player_pieces[move.capture].index((move.target_x, move.target_y))
        player_pieces[move.capture].pop(index)
        return index


def undo_capture(player_pieces: PlayerPieces, move: Move, index: Optional[int]) -> None:
    # King will never be captured when player is alive so don't need to worry about order messing up then
    if move.capture is not None:
        player_pieces[move.capture].insert(index, (move.target_x, move.target_y))


def find_captures(moves: list[Move]) -> list[Move]:
    captures = []
    for move in moves:
        if move.capture:
            captures.append(move)
    return captures


def is_attack(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour, move: Move
) -> Optional[list[Move]]:
    """Returns: The capturing move(s) the attack threatens."""

    target_piece = play_move(board, player_pieces, player_colour, move)
    pseudo_moves = generate_pseudo_moves(board, player_pieces, player_colour)
    threatening_captures = None
    for pseudo_move in pseudo_moves:
        # If there is a valid capture on the next move, then this move is an attack.
        if pseudo_move.capture:
            threatening_captures = pseudo_move
            break
    undo_move(board, player_pieces, player_colour, move, target_piece)

    return threatening_captures


def find_attacks(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour, moves: list[Move]
) -> list[Move]:
    attacks = []
    for move in moves:
        if is_attack(board, player_pieces, player_colour, move):
            attacks.append(move)
    return attacks


def pick_random_move(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour
) -> Optional[Move]:
    pseudo_moves = generate_pseudo_moves(board, player_pieces, player_colour)
    possible_moves = pseudo_moves
    # possible_moves = find_legal_moves(board, player_pieces, player_colour, pseudo_moves)

    captures = find_captures(possible_moves)

    # Prioritise captures, then attacks, then regular moves
    if captures:
        # Todo: Prioritise capturing higher value pieces.
        return random.choice(captures)
    elif attacks := find_attacks(board, player_pieces, player_colour, possible_moves):
        return random.choice(attacks)
    elif possible_moves:
        return random.choice(possible_moves)
    else:
        return None
