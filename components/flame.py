from components.chess import Piece
from components.animationplayer import AnimationPlayer
from components.button import Button
from config.assets import GAME_FONT
from config.constants import WHITE

SUMMON_COST_MAP = {
    Piece.PAWN: 1,
    Piece.KNIGHT: 3,
    Piece.BISHOP: 3,
    Piece.ROOK: 5,
    Piece.QUEEN: 9,
    Piece.KING: 2,
}


class Flame:
    def __init__(
        self,
        button: Button,
        piece_type: Piece,
        animation: AnimationPlayer,
    ) -> None:
        self.hitbox = button
        self.animation = animation
        self.piece_type = piece_type
        self.summon_cost = SUMMON_COST_MAP[piece_type]
        self.summon_text = GAME_FONT.render(f"{self.summon_cost}", False, WHITE)
