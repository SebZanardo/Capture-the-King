from components.chess import Colour, Piece


levels = [
    {
        "name": "HUMBLE BEGINNINGS",
        "board": (25, 5, 5),
        "opponents": {
            Colour.RED: [Piece.PAWN] * 3,
        },
        "mana_awarded": 15,
    },
    {
        "name": "JUMPING KNIGHTS",
        "board": (36, 6, 6),
        "opponents": {
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.PAWN] * 2,
        },
        "mana_awarded": 20,
    },
    {
        "name": "BEGINNER DUO",
        "board": (44, 7, 7),
        "opponents": {
            Colour.RED: [Piece.PAWN] * 3,
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.PAWN] * 2,
        },
        "mana_awarded": 20,
    },
    {
        "name": "DIAGONAL DANGER",
        "board": (36, 6, 6),
        "opponents": {
            Colour.GREEN: [Piece.BISHOP] * 3 + [Piece.PAWN] * 5,
        },
        "mana_awarded": 20,
    },
    {
        "name": "DYNAMIC DUO",
        "board": (70, 9, 9),
        "opponents": {
            Colour.YELLOW: [Piece.KNIGHT] * 3 + [Piece.PAWN] * 4,
            Colour.GREEN: [Piece.BISHOP] * 3 + [Piece.PAWN] * 2,
        },
        "mana_awarded": 20,
    },
    {
        "name": "RELENTLESS ROOKS",
        "board": (36, 6, 6),
        "opponents": {
            Colour.BLUE: [Piece.ROOK] * 3 + [Piece.PAWN] * 6,
        },
        "mana_awarded": 20,
    },
    {
        "name": "SLIDING PIECE SAGA",
        "board": (80, 10, 10),
        "opponents": {
            Colour.GREEN: [Piece.BISHOP] * 2 + [Piece.PAWN]*3,
            Colour.BLUE: [Piece.ROOK] * 2 + [Piece.PAWN]*3,
        },
        "mana_awarded": 20,
    },
    {
        "name": "MINOR PIECE TRIO",
        "board": (84, 12, 8),
        "opponents": {
            Colour.YELLOW: [Piece.KNIGHT] * 2 + [Piece.PAWN]*3,
            Colour.GREEN: [Piece.BISHOP] * 2 + [Piece.PAWN]*3,
            Colour.BLUE: [Piece.ROOK] * 2 + [Piece.PAWN]*4,
        },
        "mana_awarded": 30,
    },
    {
        "name": "THE ALMIGHTY QUEEN",
        "board": (64, 8, 8),
        "opponents": {
            Colour.PURPLE: [Piece.QUEEN] * 3 + [Piece.PAWN] * 9,
        },
        "mana_awarded": 30,
    },
    {
        "name": "THE FINAL CHALLENGE",
        "board": (150, 20, 10),
        "opponents": {
            Colour.YELLOW: [Piece.KNIGHT] * 3 + [Piece.PAWN]*3,
            Colour.GREEN: [Piece.BISHOP] * 3 + [Piece.PAWN]*3,
            Colour.BLUE: [Piece.ROOK] * 2 + [Piece.PAWN] * 3,
            Colour.PURPLE: [Piece.QUEEN] * 2 + [Piece.PAWN] * 3,
            Colour.BLACK: [Piece.KING] * 4 + [Piece.QUEEN] + [Piece.PAWN] * 8,
        },
        "mana_awarded": 40,
    },
    # {
    #     "name": "Black",
    #     "board": (320, 16, 16),
    #     "opponents": {
    #         Colour.BLACK: [Piece.BISHOP] * 6
    #         + [Piece.KNIGHT] * 6
    #         + [Piece.ROOK] * 6
    #         + [Piece.PAWN] * 15
    #         + [Piece.QUEEN] * 6,
    #     },
    #     "mana_awarded": 20,
    # },
    # {
    #     "name": "Party",
    #     "board": (144, 12, 12),
    #     "opponents": {
    #         Colour.BLUE: [Piece.BISHOP] * 5,
    #         Colour.PURPLE: [Piece.QUEEN] * 2 + [Piece.BISHOP] * 2 + [Piece.PAWN] * 6,
    #         Colour.GREEN: [Piece.PAWN] * 5 + [Piece.BISHOP] * 2 + [Piece.ROOK] * 3,
    #     },
    #     "mana_awarded": 20,
    # },
    # {
    #     "name": "Classic Chess",
    #     "board": (210, 16, 16),
    #     "opponents": {
    #         Colour.BLUE: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #         Colour.RED: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #     },
    #     "mana_awarded": 20,
    # },
    # {
    #     "name": "Classic Chess Mayhem",
    #     "board": (400, 20, 20),
    #     "opponents": {
    #         Colour.BLUE: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #         Colour.RED: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #         Colour.YELLOW: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #         Colour.GREEN: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #         Colour.PURPLE: [Piece.KNIGHT] * 2
    #         + [Piece.BISHOP] * 2
    #         + [Piece.PAWN] * 8
    #         + [Piece.ROOK] * 2
    #         + [Piece.QUEEN],
    #     },
    #     "mana_awarded": 20,
    # },
]
