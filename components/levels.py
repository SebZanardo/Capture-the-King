from components.chess import Colour, Piece


# NOTE: King must be first in array and only one king registered (If checking is enabled)
levels = [
    {
        "name": "Tut",
        "board": (30, 5, 5),
        "opponents": {
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Introducing Knights",
        "board": (34, 7, 7),
        "opponents": {
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.PAWN] * 1,
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Bishops on Fractal Board",
        "board": (32, 9, 8),
        "opponents": {
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 3,
            Colour.BLUE: [Piece.KING] + [Piece.BISHOP] * 2 + [Piece.PAWN] * 2,
        },
    },
    {
        "name": "Close Quarters Rooks",
        "board": (50, 10, 4),
        "opponents": {
            Colour.GREEN: [Piece.KING] + [Piece.ROOK] * 2,
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Queen Intro",
        "board": (150, 15, 15),
        "opponents": {
            Colour.PURPLE: [Piece.KING] + [Piece.QUEEN] * 1 + [Piece.ROOK] * 2 + [Piece.KNIGHT] * 3 + [Piece.PAWN] * 5,
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Bishops, Knights and Rooks",
        "board": (175, 15, 15),
        "opponents": {
            Colour.BLUE: [Piece.KING] + [Piece.BISHOP] * 4,
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 3 + [Piece.PAWN] * 4,
            Colour.GREEN: [Piece.KING] + [Piece.PAWN] * 5 + [Piece.KNIGHT] * 2 + [Piece.ROOK] * 2
        },
    },
    {
        "name": "Large Fractal",
        "board": (75, 16, 16),
        "opponents": {
            Colour.BLUE: [Piece.KING] + [Piece.BISHOP] * 5,
            Colour.PURPLE: [Piece.KING] + [Piece.QUEEN] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 6,
            Colour.GREEN: [Piece.KING] + [Piece.PAWN] * 5 + [Piece.BISHOP] * 2 + [Piece.ROOK] * 3
        },
    },
    {
        "name": "Classic Chess",
        "board": (210, 16, 16),
        "opponents": {
            Colour.BLUE: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                         [Piece.QUEEN],
            Colour.RED: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                        [Piece.QUEEN],
        },
    },
    {
        "name": "Classic Chess Mayhem",
        "board": (1024, 32, 32),
        "opponents": {
            Colour.BLUE: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                         [Piece.QUEEN],
            Colour.RED: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                        [Piece.QUEEN],
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [
                Piece.ROOK] * 2 +
                           [Piece.QUEEN],
            Colour.GREEN: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                          [Piece.QUEEN],
            Colour.PURPLE: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [
                Piece.ROOK] * 2 +
                           [Piece.QUEEN],
        },
    },
    {
        "name": "Black",
        "board": (640, 32, 32),
        "opponents": {
            Colour.BLACK: [Piece.KING] + [Piece.BISHOP] * 6 + [Piece.KNIGHT] * 6 + [Piece.ROOK] * 6 + [Piece.PAWN] * 6 +
                          [Piece.QUEEN] * 6,
        },
    },
]
