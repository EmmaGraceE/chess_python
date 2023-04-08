from pos import *
from constants import *
import logging
from copy import deepcopy


class Board:
    def __init__(self):
        self.white_pieces = {}
        self.black_pieces = {}
        self.turn = Turn.WHITE

    def mover_pieces(self) -> dict:
        """Get the current turn players pieces."""
        return self.white_pieces if self.turn == Turn.WHITE else self.black_pieces

    def opponent_pieces(self) -> dict:
        """Get the current turn opponent's pieces."""
        return self.black_pieces if self.turn == Turn.WHITE else self.white_pieces

    def set_up_board(self):
        """Set up the default positions for all pieces at turn 1."""
        # Set up pawns.
        for file in range(0, 8):
            self.white_pieces[Pos(file, 1)] = Piece.W_PAWN
            self.black_pieces[Pos(file, 6)] = Piece.B_PAWN
        # Set up rooks, bishops, knight.
        counter = 0
        for piece in [Piece.ROOK, Piece.BISHOP, Piece.KNIGHT]:
            self.white_pieces[Pos(counter, 0)] = self.white_pieces[
                Pos(7 - counter, 0)
            ] = self.black_pieces[Pos(counter, 7)] = self.black_pieces[
                Pos(7 - counter, 7)
            ] = piece
            counter += 1

        self.white_pieces[Pos(3, 0)] = self.black_pieces[Pos(4, 7)] = Piece.QUEEN
        self.white_pieces[Pos(4, 0)] = self.black_pieces[Pos(3, 7)] = Piece.KING

    def is_own(self, pos: Pos, df=0, dr=0) -> bool:
        """Checking if a place has a piece owned by current player.
        @param pos: Position object.
        @param df: file offset for pos.
        @param dr: rank offset for pos.
        :return: True if position is free.
        """
        logging.info(f"Checking if f{pos.file+1} r{pos.rank+1} has player piece.")
        pos = Pos(pos.file + df, pos.rank + dr)
        return True if pos in self.mover_pieces().keys() else False

    def is_enemy(self, pos: Pos, df=0, dr=0) -> bool:
        """Check if a place has a piece owned by opponent.
        @param pos: Position object.
        @param df: file offset for pos.
        @param dr: rank offset for pos.
        :return: True if position is free.
        """
        logging.info(f"Checking if f{pos.file+1} r{pos.rank+1} has opponent piece.")
        pos = Pos(pos.file + df, pos.rank + dr)
        return True if pos in self.opponent_pieces().keys() else False

    def is_inside_board(self, pos: Pos, df=0, dr=0) -> bool:
        """Check if a position to move to is inside the board.
        @param pos: Position object.
        @param df: file offset for pos.
        @param dr: rank offset for pos.
        :return: True if position is free.
        """
        logging.info(f"Checking if f{pos.file+1} r{pos.rank+1} is inside board.")
        pos = Pos(pos.file + df, pos.rank + dr)
        return True if (0 <= pos.file <= 7 and 0 <= pos.rank <= 7) else False

    def is_free(self, pos: Pos, df=0, dr=0) -> bool:
        """Check if a position is free.
        @param pos: Position object.
        @param df: file offset for pos.
        @param dr: rank offset for pos.
        :return: True if position is free.
        """
        logging.info(f"Checking if f{pos.file+1} r{pos.rank+1} is free.")
        if (
            self.is_own(pos, df, dr) == False
            and self.is_enemy(pos, df, dr) == False
            and self.is_inside_board(pos, df, dr) == True
        ):
            logging.info(f"f{pos.file+1} r{pos.rank+1} is free.")
            return True
        else:
            return False

    def is_check(self, check_mover: bool = True) -> bool:
        """Check if board is currently in a state of check.
        @param check_mover: By default check if the mover is in check.
        @param from_pos: optional position to try and move a piece form.
        @param new_pos:
        :return: True if in check.
        """
        
        # if we want to check whether the mover is in check then flip turns.
        if check_mover == True:
            self.switch_player()
            
        # Get the position of king for the player being tested to see if in check.
        king_pos = next(key for key, value in self.opponent_pieces().items() if value == Piece.KING)
        
        # Get all possible moves for the player who is attacking the player being tested.
        all_moves = [
            move for position in self.mover_pieces() for move in self.possible_moves(position)
        ]
        # Revert the flipping of turns.
        if check_mover == True:
            self.switch_player()
        
        # If the king's position is one of the positions that can be moved into, then 
        # it's in a state of check.
        return True if king_pos in all_moves else False

    def possible_moves(self, from_pos: Pos) -> list:
        """Get all possible moves for a given piece.
        from_pos: position of piece to get moves for.
        :return: List of all possible Pos the piece can move to.
        """
        print(from_pos.file, from_pos.rank)
        piece = self.mover_pieces()[from_pos]
        move_list = []

        def add_to(pos, df, dr) -> bool:
            pos = Pos(pos.file + df, pos.rank + dr)
            if self.is_free(pos) or self.is_enemy(pos):
                move_list.append(pos)
                return True
            return False

        if piece == Piece.W_PAWN:
            add_to(from_pos, 0, 1) if self.is_free(from_pos, 0, 1) else None
            add_to(from_pos, 0, 2) if (
                self.is_free(from_pos, 0, 1)
                and self.is_free(from_pos, 0, 2)
                and from_pos.rank == 1
            ) else None
            add_to(from_pos, 1, 1) if self.is_enemy(from_pos, 1, 1) else None
            add_to(from_pos, 1, 1) if self.is_enemy(from_pos, -1, 1) else None

        if piece == Piece.B_PAWN:
            add_to(from_pos, 0, -1) if self.is_free(from_pos, 0, -1) else None
            add_to(from_pos, 0, -2) if (
                self.is_free(from_pos, 0, -1)
                and self.is_free(from_pos, 0, -2)
                and from_pos.rank == 6
            ) else None
            add_to(from_pos, -1, -1) if self.is_enemy(from_pos, -1, -1) else None
            add_to(from_pos, 1, -1) if self.is_enemy(from_pos, 1, -1) else None

        if piece in [Piece.ROOK, Piece.QUEEN]:
            for df, dr in [(0, 1), (0, 1), (-1, 0), (0, -1)]:
                for multiplier in range(1, 8):
                    if not add_to(
                        from_pos, df * multiplier, dr * multiplier
                    ) and not self.is_enemy(from_pos, df * multiplier, dr * multiplier):
                        break

        if piece in [Piece.BISHOP, Piece.QUEEN]:
            for df, dr in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                for multiplier in range(1, 8):
                    if not add_to(
                        from_pos, df * multiplier, dr * multiplier
                    ) and not self.is_enemy(from_pos, df * multiplier, dr * multiplier):
                        break

        if piece == Piece.KNIGHT:
            for df, dr in [
                (1, 2),
                (-1, 2),
                (1, -2),
                (-1, -2),
                (2, 1),
                (-2, 1),
                (2, -1),
                (-2, -1),
            ]:
                add_to(from_pos, df, dr)

        if piece == Piece.KING:
            for df, dr in [(i, j) for i in range(-1, 2) for j in range(-1, 2)]:
                add_to(from_pos, df, dr)

        logging.info(
            f"Possible moves for {piece} are:\n"
            + "\n".join([f"f{i.file+1}, r{i.rank+1}" for i in move_list])
        )
        return move_list

    def make_move(self, move_from: Pos, move_to: Pos) -> bool:
        """
        @param move_from: position to try and move a piece from.
        @param move_to: position to try and move a piece to.
        :return: Return true if move made successfully.
        """

        if not self.is_own(move_from):
            return False

        if move_to in self.possible_moves(move_from):
            # Save current positions in case they need to be reverted to if the is_check
            # test fails. Use deepcopy as children are changed/deleted.
            old_mover_pieces = deepcopy(self.mover_pieces())
            old_opponent_pieces = deepcopy(self.opponent_pieces())

            if self.is_enemy(move_to):
                logging.info(f"Removing enemy piece at {move_to}.")
                self.opponent_pieces().pop(move_to)

            logging.info(f"Moving {move_from} to {move_to}.")
            self.mover_pieces()[move_to] = self.mover_pieces()[move_from]
            self.mover_pieces().pop(move_from)

            # If move would result in a state of check, then don't allow move and revert
            # to previous state.
            if self.is_check(check_mover=True):
                if self.turn == Turn.WHITE:
                    self.white_pieces, self.black_pieces = (
                        old_mover_pieces,
                        old_opponent_pieces,
                    )
                else:
                    self.white_pieces, self.black_pieces = (
                        old_opponent_pieces,
                        old_mover_pieces,
                    )
                return False

            return True
        return False

    def switch_player(self) -> None:
        """
        Switches currently active player.
        """
        self.turn = Turn.WHITE if self.turn == Turn.BLACK else Turn.BLACK
