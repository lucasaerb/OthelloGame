# Lucas Erb 86293617. ICS 32 Project 4.
#
# othello_ui.py
# This program handles the user-interface (inputs and printing) and game order of the Othello game.
# the game is started using an if __name__ == "__main__" statement at the bottom which creates an Othello object
# and calls upon the run_game() function.


from othello_logic import OthelloGame
import othello_logic


def run_game():
    """Main class of the othello user interface module. Controls the flow of the other user-interface functions and sets the values
    of various othello object properties. """


    print("FULL")

    othello_game.BOARD_SIZE = read_board_line_nums()
    othello_game.whose_turn = read_first_player()
    othello_game.WINNER_CONDITION = read_winner_condition()
    othello_game.board_state = read_board_initial_contents(othello_game.BOARD_SIZE)

    while True:

        if othello_game.is_game_over():
            print_pieces()
            print_board()
            print_winner()
            break

        print_pieces()
        print_board()
        print_turn()

        while True:

            move_coordinates = read_move()
            try:
                othello_game.make_move(move_coordinates)
                print('VALID')
                break

            except othello_logic.InvalidMoveError:
                print('INVALID')


def print_winner():
    """Takes information from the othello_logic get_winner() class. Converts the Othello object
    values into string representations with the converter dictionary. Prints the Winner. """

    winner = othello_game.get_winner()
    converter = {1: 'B', -1: 'W', None: 'NONE'}
    print('WINNER: {}'.format(converter[winner]))


def print_pieces():
    """Converts the othello_logic class get_piece_counts information into string readable format.
    Prints the number of black and white pieces on the board. """

    piece_counts = othello_game.get_piece_counts()
    print('B: {}  W: {}'.format(piece_counts.black, piece_counts.white))


def print_turn():
    """Prints whose turn it is (Black or White) to the user interface."""

    converter = {1: 'B', -1: 'W', }
    print('TURN: {}'.format(converter[othello_game.whose_turn]))


def read_move() -> tuple:
    """Reads the players imput move "(row: int) (column: int)" and returns it as a tuple coordinate (row, column)
        for use in making a move in the Othello game."""

    move = input().split(' ')
    try:
        return int(move[0]) - 1, int(move[1]) - 1
    except ValueError:
        raise othello_logic.InvalidMoveError


def print_board():
    """Calls upon the Othello object board_state converting its values into readable strings using
    the converter dictionary. Prints a nicely formatted board with each row representing one printed line."""

    board_state = othello_game.board_state
    converter = {0: '. ', 1: 'B ', -1: 'W '}
    for row in board_state:
        line = ''
        for piece in row:
            line += converter[piece]
        print(line[:-1])


def read_board_line_nums() -> tuple:
    """Reads two lines of integer input from the console. The first line specifies the numver of rows,
    the second the number of columns. Raise a ValueError if the rows/columns values are not between 4 and 16 and even
    numbers. Returns a 2 item tuple containing first the rows integer and then the columns integer"""

    num_of_rows = int(input())
    num_of_columns = int(input())
    if 16 >= num_of_rows >= 4 and num_of_rows % 2 == 0 and 16 >= num_of_columns >= 4 and num_of_columns % 2 == 0:
        return num_of_rows - 1, num_of_columns - 1
    else:
        raise othello_logic.InvalidBoardError('Invalid Board Size: Must be even and between 4x4 and 16x16 in size')


def read_first_player() -> int:
    """Reads a character of input either 'B' or 'W' declaring the first player to move in the game. Verifies that the
    value is one of those two and returns the first_player as a string."""

    converter = {'B': 1, 'W': -1}
    first_player = input().strip(' ')
    if first_player == 'B' or first_player == 'W':
        return converter[first_player]
    else:
        raise ValueError


def read_winner_condition() -> str:
    """Reads the winner condition, verifies it is either '<' or '>'. Raises a value error if not.
    Returns the winner condition as a string.

    Winner conditions:
    > means that the player with the most discs on the board at the end of the game wins
    < means the player with the fewest
    """

    winner_condition = input().strip(' ')
    if winner_condition == '<' or winner_condition == '>':
        return winner_condition
    else:
        raise ValueError


def read_board_initial_contents(board_line_nums: tuple) -> [[int]]:
    """Reads the player input of initial board contents - one line representing one row of the board.
    Reads line inputs equivalent to the number of rows in the board. Uses the converter dictionary to convert
    piece values to those needed by the Othello object class.
    Returns a list of lists representing the starting othello board."""

    initial_contents = []
    num_of_rows = board_line_nums[0]
    converter = {'.': 0, 'B': 1, 'W': -1}

    for row in range(num_of_rows + 1):
        sublist = []
        try:
            for piece in input().split(' '):
                sublist.append(converter[piece])
        except (ValueError, KeyError):
            raise othello_logic.InvalidBoardError('Invalid Initial Board Piece given.')

        initial_contents.append(sublist)
    return initial_contents


if __name__ == "__main__":
    othello_game = OthelloGame()   # Creates a new OthelloGame object titled "othello_game"
    run_game()
