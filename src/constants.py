from enum import Enum


class Piece(Enum):
    W_PAWN = 0
    # black and white pawns have different movesets so seperate pieces.
    B_PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Turn(Enum):
    WHITE = 0
    BLACK = 1


PIECE_SCORE_MAP = {
    Piece.W_PAWN: 1,
    Piece.B_PAWN: 1,
    Piece.KNIGHT: 3,
    Piece.BISHOP: 3,
    Piece.ROOK: 4,
    Piece.QUEEN: 5,
    # King should be considered INF.
    Piece.KING: 10000,
}

PIECE_SPRITE_MAP = {
    Piece.W_PAWN: "p",
    Piece.B_PAWN: "p",
    Piece.KNIGHT: "n",
    Piece.BISHOP: "b",
    Piece.ROOK: "r",
    Piece.QUEEN: "q",
    Piece.KING: "k",
}
