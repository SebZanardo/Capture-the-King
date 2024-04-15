from components.chess import Colour, Piece


# NOTE: King must be first in array and only one king registered (If checking is enabled)
levels = [
    {
        "name": "Tut",
        "board": (30, 5, 5),
        "opponents": {
            Colour.RED: [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Introducing Knights",
        "board": (44, 7, 7),
        "opponents": {
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.PAWN] * 1,
            Colour.RED: [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Bishop Time",
        "board": (112, 8, 8),
        "opponents": {
            Colour.BLUE: [Piece.BISHOP] * 3 + [Piece.PAWN] * 6,
        },
    },
    {
        "name": "Close Quarters Rooks",
        "board": (50, 10, 4),
        "opponents": {
            Colour.GREEN: [Piece.ROOK] * 2,
            Colour.RED: [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Queen Intro",
        "board": (150, 13, 13),
        "opponents": {
            Colour.PURPLE: [Piece.QUEEN] * 1 + [Piece.ROOK] * 2 + [Piece.KNIGHT] * 3 + [Piece.PAWN] * 5,
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.PAWN] * 3,
        },
    },
    {
        "name": "Bishops, Knights and Rooks",
        "board": (200, 15, 15),
        "opponents": {
            Colour.BLUE: [Piece.BISHOP] * 4,
            Colour.YELLOW: [Piece.KNIGHT] * 3 + [Piece.PAWN] * 4,
            Colour.GREEN: [Piece.PAWN] * 5 + [Piece.KNIGHT] * 2 + [Piece.ROOK] * 2
        },
    },
    {
        "name": "Black",
        "board": (320, 16, 16),
        "opponents": {
            Colour.BLACK: [Piece.BISHOP] * 6 + [Piece.KNIGHT] * 6 + [Piece.ROOK] * 6 + [Piece.PAWN] * 15 +
                          [Piece.QUEEN] * 6,
        },
    },
    {
        "name": "Party",
        "board": (144, 12, 12),
        "opponents": {
            Colour.BLUE: [Piece.BISHOP] * 5,
            Colour.PURPLE: [Piece.QUEEN] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 6,
            Colour.GREEN: [Piece.PAWN] * 5 + [Piece.BISHOP] * 2 + [Piece.ROOK] * 3
        },
    },
    {
        "name": "Classic Chess",
        "board": (210, 16, 16),
        "opponents": {
            Colour.BLUE: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                         [Piece.QUEEN],
            Colour.RED: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                        [Piece.QUEEN],
        },
    },
    {
        "name": "Classic Chess Mayhem",
        "board": (400, 20, 20),
        "opponents": {
            Colour.BLUE: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                         [Piece.QUEEN],
            Colour.RED: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                        [Piece.QUEEN],
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [
                Piece.ROOK] * 2 +
                           [Piece.QUEEN],
            Colour.GREEN: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [Piece.ROOK] * 2 +
                          [Piece.QUEEN],
            Colour.PURPLE: [Piece.KNIGHT] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 8 + [
                Piece.ROOK] * 2 +
                           [Piece.QUEEN],
        },
    },

]
