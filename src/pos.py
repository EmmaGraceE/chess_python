class Pos:
    """Handler class for positions.
    FILE = x
    RANK = y
    """

    def __init__(self, file: int = 0, rank: int = 0) -> None:
        self.file = file
        self.rank = rank

    def translate_notation(self, notation: str) -> tuple:
        """Translates notation into a position, returns an error
        if position doesn't exist."""
        if len(notation) != 2:
            # Temp
            raise ValueError

        file = ord(notation[0].lower()) - 96
        rank = int(notation[1])
        if (file >= 1 and file <= 8) and (rank >= 1 and rank <= 8):
            return (file + 1, rank + 1)

        else:
            # Temp
            raise ValueError

    def __hash__(self) -> int:
        return hash((self.file, self.rank))

    def __eq__(self, other: object) -> bool:
        return (self.file, self.rank) == (other.file, other.rank)


def translate_notation(notation: str) -> Pos:
    if len(notation) == 2:
        return Pos(ord(notation[0].lower()) - ord("a"), int(notation[1]) - 1)
    raise Exception
