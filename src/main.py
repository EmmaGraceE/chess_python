from constants import Turn
from pos import translate_notation
from board import Board
from utils import render_board
from minimax import negamax, is_checkmate
import logging

logging.basicConfig(level=logging.ERROR)


def game_loop():
    """Loop from which game is played."""
    check_flag = False
    board = Board()
    board.set_up_board()

    while True:
        render_board(board.white_pieces, board.black_pieces)
        turn_text = "White" if board.turn == Turn.WHITE else "Black"
        print(
            f"{turn_text}'s turn."
            # Report if the current user is in check.
            + (" They're in check." if check_flag else "")
            + "\nEnter position to move from and to:"
        )
        user_response = input("> ")
        origin, dest = translate_notation(user_response[:2]), translate_notation(
            user_response[2:]
        )
        if board.make_move(origin, dest) == False:
            print("This move isn't possible, try again.")
            continue

        if is_checkmate(board, check_mover=False):
            break
        check_flag = True if board.is_check(check_mover=False) else False

        board.switch_player()

    print(f"{turn_text} wins.")
    exit()


def main():
    game_loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame ended without a winner.")
