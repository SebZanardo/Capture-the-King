from components.chess import Colour, Piece


# NOTE: King must be first in array and only one king registered (If checking is enabled)
levels = [
    {
        "name": "Level One",
        "board": (20, 5, 5),
        "opponents": {
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 4,
        },
    },
    {
        "name": "Level Two",
        "board": (20, 7, 5),
        "opponents": {
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.PAWN] * 2,
        },
    },
    {
        "name": "Level Three",
        "board": (65, 10, 8),
        "opponents": {
            Colour.RED: [Piece.KING] + [Piece.PAWN] * 4,
            Colour.YELLOW: [Piece.KING] + [Piece.KNIGHT] * 2 + [Piece.PAWN] * 2,
        },
    },
]
