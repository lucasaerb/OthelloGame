# Lucas Erb 86293617. ICS 32 Project 4.
#
# othello_logic.py
# This program handles the underlying game logic of the Othello Game utlilizing one main class: Othello.

from collections import namedtuple


class InvalidBoardError(Exception):
    """Error for an invalid board_state."""
    pass


class InvalidMoveError(Exception):
    """Error for invalid moves."""
    pass


class InvalidFlipError(Exception):
    """Error for invalid piece flips."""
    pass


class OthelloGame:
    """Main class for the Othello Game. Multiple functions for manipulating the internal game logic and
    variables and running a game of Othello."""

    def __init__(self):
        """Inititalizes all of the variables used in the Othello object."""

        self._EMPTY = 0
        self._BLACK = 1
        self._WHITE = -1
        self.BOARD_SIZE = (0, 0)
        self.WINNER_CONDITION = ''

        self.board_state = [[]]
        self.whose_turn = 0

    def make_move(self, coordinates: tuple):
            """Takes in a set of coordinates (row, column) as a tuple. Attempts to make a move on that spot
            and raises an InvalidMoveError if the move attempt is unsuccessful. Creates a list of pieces
            which must be flipped using the _get_flipped_pieces() function based on the coordinates given.
            Flips those pieces one at a time using the _flip_piece() function.
            Switches to the next player's turn at the end of the move. """

            try:
                if self.board_state[coordinates[0]][coordinates[1]] != self._EMPTY:
                    raise InvalidMoveError
            except IndexError:
                raise InvalidMoveError

            to_be_flipped = self._get_flipped_pieces(coordinates)
            if len(to_be_flipped) <= 0:
                raise InvalidMoveError

            else:
                self.board_state[coordinates[0]][coordinates[1]] = self.whose_turn
                for piece in to_be_flipped:
                    self._flip_piece(piece)
            self._switch_turns()

    def is_game_over(self) -> bool:
        """Checks the game board and other othello game-states to find out if the game is over or not
        If there are no empty spaces left on the board, the game is over.
        Also checks if there are any valid moves for the current player and if not it will switch to the next player's
        turn. (If this happens twice in a row ie. there are no valid moves for either player, the game is over).
        If the game is over - returns True. If the game is not over - returns False.
        """

        if self.get_piece_counts().empty == 0:
            return True
        if not self._is_any_valid_moves():
            self._switch_turns()
            if not self._is_any_valid_moves():
                return True
        return False

    def get_winner(self)-> int or None:
        """Checks the winner condition against a dictionary to call upon the _get_winner_most and
        _get_winner_least functions in order to return the winner of the othello game or None if
        the players are tied."""

        winner_condition_converter = {'>': self._get_winner_most(), '<': self._get_winner_least()}
        return winner_condition_converter[self.WINNER_CONDITION]

    def get_piece_counts(self) -> namedtuple:
        """Counts through the board_state of the game to add up the number of each piece that is in play,
        including empty spaces. Returns a namedtuple containing a .empty .black and .white instances which contain
        the number of empty black and white pieces currently on the board."""

        piece_counts = namedtuple('piece_counts', 'empty black white')
        empty = 0
        black = 0
        white = 0

        for row in self.board_state:
            for piece in row:
                if piece == self._EMPTY:
                    empty += 1
                elif piece == self._BLACK:
                    black += 1
                elif piece == self._WHITE:
                    white += 1
                else:
                    raise InvalidBoardError("The game_board is invalid. All pieces must be '.' 'B' or 'W'")

        return piece_counts(empty, black, white)

    # PRIVATE FUNCTIONS #

    def _get_flipped_pieces(self, coordinates: tuple):
        """Takes in a tuple set of coordinates (row, column) and returns a list of tuples: coordinates of Pieces which
        should be flipped if a player's piece was placed on the coordinates passed. This function is not
        only used to make a move, but also to check whether there are any valid moves for a player."""

        directions_list = [(1, -1), (1, 0), (1, 1),
                           (-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1)]
        to_be_flipped = []
        for direction in directions_list:

            row = coordinates[0] + direction[0]
            column = coordinates[1] + direction[1]

            potential_flips = []

            while self.BOARD_SIZE[0] > row >= 0 and self.BOARD_SIZE[1] > column >= 0:
                if self.board_state[row][column] == self._EMPTY:
                    break
                elif self.board_state[row][column] != self.whose_turn and self.board_state[row][column] != self._EMPTY:
                    potential_flips.append((row, column))

                elif self.board_state[row][column] == self.whose_turn:
                    if len(potential_flips) > 0:
                        to_be_flipped += potential_flips
                    break

                row += direction[0]
                column += direction[1]

        return to_be_flipped

    def _is_any_valid_moves(self) -> bool:
        """Utilizes the _get_flipped_pieces function primarily to check whether a player has any
        valid moves available on the board_state. Goes through every available empty space on the board
        and verifies there is at least one valid move which would flip a piece. If no moves are valid for
        the player: returns False. Otherwise: Returns True."""

        for row in range(len(self.board_state)):
            for item in range(len(self.board_state[row])):
                if self.board_state[row][item] == self._EMPTY:
                    if len(self._get_flipped_pieces((row, item))) > 0:
                        return True
        return False

    def _switch_turns(self):
        """Switches to the next player's turn by multiplying self.whose_turn by -1 """
        self.whose_turn *= -1

    def _flip_piece(self, coordinates: tuple):
        """Takes in a coordinates tuple (row, column) and flips the piece of the coordinate
        passed by multiplying it by -1. Performs one last check beforehand that the coordinates passed
        are to a valid non-empty space - raises an InvalidFlipError if not."""

        if self.board_state[coordinates[0]][coordinates[1]] == self._EMPTY:
            raise InvalidFlipError
        else:
            self.board_state[coordinates[0]][coordinates[1]] *= -1

    def _get_winner_most(self)-> int or None:
        """Returns the winner based on who has the most pieces on the board.
        Returns None if the Black and White pieces are tied."""

        piece_counts = self.get_piece_counts()
        if piece_counts.black > piece_counts.white:
            return self._BLACK
        elif piece_counts.white > piece_counts.black:
            return self._WHITE
        else:
            return None

    def _get_winner_least(self)-> int or None:
        """Returns the winner based on who has the least pieces on the board.
        Returns None if the Black and White pieces are tied."""

        piece_counts = self.get_piece_counts()
        if piece_counts.black < piece_counts.white:
            return self._BLACK
        elif piece_counts.white < piece_counts.black:
            return self._WHITE
        else:
            return None
