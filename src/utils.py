from constants import PIECE_SPRITE_MAP


def render_board(white_pieces: dict, black_pieces: dict) -> None:
    """Pretty print the board to the terminal."""

    print("    A   B   C   D   E   F   G   H\n")
    for rank in reversed(range(0, 8)):
        line = str(rank + 1) + "  "

        for file in range(0, 8):

            sprite = " "

            for piece in white_pieces:
                if (piece.file == file) and (piece.rank == rank):
                    sprite = (
                        "\u001b[32m" + (PIECE_SPRITE_MAP[white_pieces[piece]]).upper()
                    )
                    break
            for piece in black_pieces:
                if (piece.file == file) and (piece.rank == rank):
                    sprite = "\u001b[31m" + PIECE_SPRITE_MAP[black_pieces[piece]]
                    break

            if (file % 2 == 0 and rank % 2 == 1) or (file % 2 == 1 and rank % 2 == 0):
                sprite = "\u001b[40m " + sprite
            else:
                sprite = "\u001b[47m " + sprite

            line += sprite + " \u001b[0m "

        print(line + " " + str(rank + 1) + "\n")

    print("    A   B   C   D   E   F   G   H")
