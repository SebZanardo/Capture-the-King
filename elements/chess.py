from typing import Optional
import chess
from stockfish import Stockfish


class Board:
    def __init__(self, fen_string: str) -> None:
        self.starting_fen = fen_string
        self.setup_board()
        self.setup_stockfish(5)

    def setup_board(self) -> None:
        self.board = chess.Board(self.starting_fen)

    def setup_stockfish(self, depth: int = 15, rating: int = 1600) -> None:
        self.stockfish = Stockfish()
        self.stockfish.set_depth(depth)
        self.stockfish.set_elo_rating(rating)
        self.stockfish.set_fen_position(self.starting_fen)

    def get_piece(self, x: int, y: int) -> Optional[str]:
        piece = self.board.piece_at(position_to_square(x, y))
        if not piece:
            return None
        return piece.symbol()


def position_to_square(x: int, y: int) -> int:
    return (7-y) * 8 + x
