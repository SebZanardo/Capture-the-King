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
    board: Board,
    player_pieces: PlayerPieces,
    player_colour: Colour,
    pieces: list[Piece],
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
        player_pieces[player_colour].add(square)


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
            return get_pawn_moves(board, player_pieces, player_colour, x, y, 1)

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


def perform_move(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour, move: Move
) -> None:
    # Move the piece on the board
    board[(move.target_x, move.target_y)] = board[(move.piece_x, move.piece_y)]
    board[(move.piece_x, move.piece_y)] = None

    # Update player_pieces for player that moved
    player_pieces[player_colour].remove((move.piece_x, move.piece_y))
    player_pieces[player_colour].add((move.target_x, move.target_y))

    # Update remove opponents piece if there was a capture
    if move.capture is not None:
        player_pieces[move.capture].remove((move.target_x, move.target_y))


def play_random_move(
    board: Board, player_pieces: PlayerPieces, player_colour: Colour
) -> None:
    possible_moves = generate_pseudo_moves(board, player_pieces, player_colour)
    if possible_moves:
        selected_move = random.choice(possible_moves)
        perform_move(board, player_pieces, player_colour, selected_move)
