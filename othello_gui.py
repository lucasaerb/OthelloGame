# Lucas Erb 86293617. ICS 32 Project 5.
#
# othello_gui.py
# This program controls Tkinter interfaces for the Graphical User Interface (GUI) version of the Othello Game.


import tkinter
from othello_logic import OthelloGame
import othello_logic

BACKGROUND_COLOR = '#dde2d5'
DEFAULT_FONT = ('Helvetica', 14)
BOARD_COLOR = '#0c5e1b'


class MainGameGui:
    """Last Class run in the game. Controls interfacing with the OthelloGame class and runs each player's turn.
    This is the primary game Gui which the user will use for playing the Othello Game."""
    def __init__(self):
        """Initializes the tkinter self._root_window and attributes (buttons, labels, etc)."""
        self._root_window = tkinter.Tk()
        self._width = 600
        self._height = 600
        self._boxes_coordinates_list = [[]]
        ###############
        self._piece_count_label = tkinter.Label(master=self._root_window, text='', font=("Helvetica", 17))

        self._piece_count_label.grid(row=0,column = 0, padx=10, pady=10, sticky=tkinter.S)
        ###############
        self._canvas = tkinter.Canvas(
            master=self._root_window, width=600, height=600,
            background=BACKGROUND_COLOR)
        self._canvas.grid(row=1, column=0, padx=10, pady=10,
                          sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        ################
        self._whose_turn_label = tkinter.Label(master=self._root_window,
                                               text='', font=("Helvetica", 17))
        self._whose_turn_label.grid(row=2, column=0, padx=10, pady=10, sticky=tkinter.N)
        ################
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def run(self) -> None:
        """Runs the mainloop on the root window for the tkinter interface."""
        self._root_window.mainloop()

    def _draw_board(self) -> None:
        """Prints the main background board with colors and updates sizes.
        Prints the OthelloGame board_state to the gui with corresponding blanks, blacks, and whites."""
        color_converter = {-1: 'White', 1: 'Black', None: 'TIE'}
        piece_counts = othello_game.get_piece_counts()
        if othello_game.is_game_over():
            winning_color = color_converter[othello_game.get_winner()]
            self._whose_turn_label.configure(text="GAME OVER\n{} Wins!".format(winning_color))
        else:
            self._whose_turn_label.configure(text= "{}'s turn".format(color_converter[othello_game.whose_turn]))

        self._piece_count_label.configure(text = 'FULL\nBlack: {}   White: {}'.format(piece_counts.black,
                                                                                    piece_counts.white))

        for row in range(len(othello_game.board_state)):
            for piece in range(len(othello_game.board_state[row])):
                box_coords = self._boxes_coordinates_list[row][piece]
                self._canvas.create_rectangle(box_coords, fill=BOARD_COLOR, outline='black')
                if othello_game.board_state[row][piece] != 0:
                    self._canvas.create_oval(box_coords, fill = color_converter[othello_game.board_state[row][piece]])
        return

    def _on_canvas_clicked(self, event: tkinter.Event):
        """When the canvas is clicked compares the coordinates with corresponding box coordinates to make a
               move of the piece at a certain row and column."""
        for row in range(len(self._boxes_coordinates_list)):
            for column in range(len(self._boxes_coordinates_list[row])):
                box = self._boxes_coordinates_list[row][column]
                if box[1][0] > event.x > box[0][0] and box[1][1] > event.y > box[0][1]:
                    self._make_move(row, column)
        return None

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        """When the canvas is resized, deletes the current canvas, updates the coordinates, and redraws the board."""
        self._canvas.delete(tkinter.ALL)
        self._update_boxes_coordinates_list()
        self._draw_board()

    def _make_move(self, row: int, column: int)-> None:
        """Try's  to make a move on the OthelloGame at the row and column given, redraws the board.
        If the move is not valid catches the  othello_logic InvalidMoveError, and Redraws the board."""
        try:
            othello_game.make_move((row,column))
        except othello_logic.InvalidMoveError:
            pass
        self._draw_board()
        return

    def _update_boxes_coordinates_list(self) -> None:
        """Takes the list of boxes coordinates and updates them to the current size of the window."""
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()

        BOARD_RATIO1 = (0.05, 0.05)
        BOARD_RATIO2 = (0.95, 0.95)
        board_corner1 = self._frac_to_pixel(BOARD_RATIO1)
        board_corner2 = self._frac_to_pixel(BOARD_RATIO2)

        rows = othello_game.BOARD_SIZE[0]
        columns = othello_game.BOARD_SIZE[1]

        rows_space = (board_corner2[1] - board_corner1[1]) / rows
        cols_space = (board_corner2[0] - board_corner1[0]) / columns

        list_of_boxes = []

        for row in range(rows):
            sublist = []
            coordinate = [(board_corner1[0], board_corner1[1] + rows_space * row),
                          (board_corner1[0] + cols_space, board_corner1[1] + rows_space * row + rows_space)]
            for column in range(columns):
                sublist.append(((coordinate[0][0] + cols_space * column, coordinate[0][1]),
                                (coordinate[1][0] + cols_space * column, coordinate[1][1])))
            list_of_boxes.append(sublist)

        self._boxes_coordinates_list = list_of_boxes

    def _frac_to_pixel(self, coordinates: tuple) -> tuple:
        """Takes in a coordinate tuple in ratio (fraction) form and returns a tuple of their pixel values."""
        return (coordinates[0] * self._width, coordinates[1] * self._height)

    def _pixel_to_frac(self, pixel_coordinates: tuple) -> tuple:
        """Takes in a coordinate tuple  in pixels and returns a tuple of their ratio (fraction) values."""
        return (pixel_coordinates[0] / self._width, pixel_coordinates[1] / self._height)


class BoardSelection:
    """Controls the user's selection of an initial board. This initial board (the white and then black pieces)
    are then passed to the OthelloGame object for use in the board_state."""
    def __init__(self):
        """Initializes the tkinter self._root_window and attributes (buttons, labels, etc)."""
        self._width = 600
        self._height = 600
        self._root_window = tkinter.Tk()

        self._start_board = self._build_empty_board()
        self._currently_placing = 1
        self._boxes_coordinates_list = [[]]
        self._piece_list = []

        ###############
        self._canvas = tkinter.Canvas(
            master=self._root_window, width=600, height=600,
            background=BACKGROUND_COLOR)
        self._canvas.grid(row=2, column=0, padx=10, pady=10,
                          sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        ################
        self._label = tkinter.Label(master=self._root_window,
                                    text='Please Place Starting Black Discs.', font=("Helvetica", 17))
        self._label.grid(row=0,column=0, padx=20, pady=20, sticky=tkinter.N)
        ################
        self._next_button = tkinter.Button(
            master=self._root_window, text='Okay.', font=DEFAULT_FONT,
            command=self._on_okay_button)
        self._next_button.grid(row=3, column=0, padx=10, pady=10, sticky=tkinter.S + tkinter.E)
        ################

        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Configure>', self._on_canvas_resized)


        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def run(self) -> None:
        """Runs the mainloop on the root window for the tkinter interface."""
        self._root_window.mainloop()

    def _draw_board(self) -> None:
        """Draws the board, first boxes and then the pieces (from pieces_list) which overlay on top of the board."""
        color_converter = {-1: 'white', 1: 'black'}
        for row in self._boxes_coordinates_list:
            for box in row:
                self._canvas.create_rectangle(box, fill=BOARD_COLOR, outline='black')
        for piece in self._piece_list:
            self._canvas.create_oval(self._boxes_coordinates_list[piece[0]][piece[1]], fill = color_converter[piece[2]])

    def _update_boxes_coordinates_list(self) -> None:
        """Takes the list of boxes coordinates and updates them to the current size of the window."""
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()

        BOARD_RATIO1 = (0.05, 0.05)
        BOARD_RATIO2 = (0.95, 0.95)
        board_corner1 = self._frac_to_pixel(BOARD_RATIO1)
        board_corner2 = self._frac_to_pixel(BOARD_RATIO2)

        rows = othello_game.BOARD_SIZE[0]
        columns = othello_game.BOARD_SIZE[1]

        rows_space = (board_corner2[1] - board_corner1[1]) / rows
        cols_space = (board_corner2[0] - board_corner1[0]) / columns

        list_of_boxes = []

        for row in range(rows):
            sublist = []
            coordinate = [(board_corner1[0], board_corner1[1] + rows_space * row),
                          (board_corner1[0] + cols_space, board_corner1[1] + rows_space * row + rows_space)]
            for column in range(columns):
                sublist.append(((coordinate[0][0] + cols_space * column, coordinate[0][1]),
                                (coordinate[1][0] + cols_space * column, coordinate[1][1])))
            list_of_boxes.append(sublist)

        self._boxes_coordinates_list = list_of_boxes

    def _on_canvas_clicked(self, event: tkinter.Event):
        """When the canvas is clicked compares the coordinates with corresponding box coordinates to call a placement
        of the piece at a certain row and column. redraws the board."""
        for row in range(len(self._boxes_coordinates_list)):
            for column in range(len(self._boxes_coordinates_list[row])):
                box = self._boxes_coordinates_list[row][column]
                if box[1][0] > event.x > box[0][0] and box[1][1] > event.y > box[0][1]:
                    self._place(row, column)
                    self._draw_board()
        return None

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        """When the canvas is resized, deletes the current canvas, updates the coordinates, and redraws the board."""
        self._canvas.delete(tkinter.ALL)
        self._update_boxes_coordinates_list()
        self._draw_board()

    def _frac_to_pixel(self, coordinates: tuple) -> tuple:
        """Takes in a coordinate tuple in ratio (fraction) form and returns a tuple of their pixel values."""
        return (coordinates[0] * self._width, coordinates[1] * self._height)

    def _pixel_to_frac(self, pixel_coordinates: tuple) -> tuple:
        """Takes in a coordinate tuple  in pixels and returns a tuple of their ratio (fraction) values."""
        return (pixel_coordinates[0] / self._width, pixel_coordinates[1] / self._height)

    def _build_empty_board(self) -> list:
        """Builds an initial empty board based on the number of rows and columns that the user passed to
        the OthelloGame object."""
        board = []
        for row in range(othello_game.BOARD_SIZE[0]):
            templist = []
            for column in range(othello_game.BOARD_SIZE[1]):
                templist.append(0)
            board.append(templist)
        return board

    def _place(self, row: int, column: int) -> None:
        """Given row and column coordinates representing a placement. Assuming the placement
        is valid, it updates that placement in the piecelist as well as removing a piece if it was
        previously placed where clicked."""
        piece = ((row, column, self._currently_placing))
        if self._start_board[row][column] != self._currently_placing * -1:
            if piece in self._piece_list:
                self._remove_piece(row,column)
            else:
                self._piece_list.append((row, column, self._currently_placing))
                self._start_board[row][column] = self._currently_placing

        return

    def _on_okay_button(self) -> None:
        """When the okay button is pressed changes the currently placing to white if currently placing
        blacks, or passes the board to OthelloGame and destroys the window if the user is done placing whites."""
        if self._currently_placing == -1:
            othello_game.board_state = self._start_board
            self._root_window.destroy()
        else:
            self._currently_placing *= -1
            self._label.configure(text = 'Now Place Starting White Discs.' )
        return

    def _remove_piece(self, row:int, column: int)-> None:
        """Removes a piece that was previously placed and clicked again that way if a user
        mistakenly places a starting position they can correct that mistake."""
        for piece in self._piece_list:
            if piece[0] == row and piece[1] == column:
                self._piece_list.remove(piece)
        self._start_board[row][column] = 0


class StartGameInfo:
    """Runs right at the beginning of the game through PreGame()- controls getting the initial game info from the
    user and passing it to PreGame so that PreGame can assign those variables to the variables used in the
    othello_logic.py OthelloGame class."""
    def __init__(self):
        """Initializes the tkinter _game_info_window and attributes (buttons, labels, etc). for
        the StartGameInfo class."""
        self._game_info_window = tkinter.Toplevel()

        welcome_label = tkinter.Label(
            master=self._game_info_window, text='WELCOME TO OTHELLO\n\nBefore you play, '
                                                'give us some info about your game.', font=DEFAULT_FONT)

        welcome_label.grid(
            row=0, columnspan=2, padx=10, pady=10)

        #   ASK ROWS:
        rows_label = tkinter.Label(
            master=self._game_info_window, text='Number of Rows (Even Number Between 4 and 16):',
            font=DEFAULT_FONT)

        rows_label.grid(
            row=1, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self._rows_entry = tkinter.Entry(
            master=self._game_info_window, width=20, font=DEFAULT_FONT)

        self._rows_entry.grid(
            row=1, column=1, padx=10, pady=1,
            sticky=tkinter.W + tkinter.E)

        #   ASK COLUMNS:
        columns_label = tkinter.Label(
            master=self._game_info_window, text='Number of Columns (Even Number Between 4 and 16):',
            font=DEFAULT_FONT)

        columns_label.grid(
            row=2, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self._columns_entry = tkinter.Entry(
            master=self._game_info_window, width=20, font=DEFAULT_FONT)

        self._columns_entry.grid(
            row=2, column=1, padx=10, pady=1,
            sticky=tkinter.W + tkinter.E)

        #   ASK FIRST MOVE:
        first_move_label = tkinter.Label(
            master=self._game_info_window, text='Who moves first? ("Black" or "White"):',
            font=DEFAULT_FONT)

        first_move_label.grid(
            row=3, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self._first_move_entry = tkinter.Entry(
            master=self._game_info_window, width=20, font=DEFAULT_FONT)

        self._first_move_entry.grid(
            row=3, column=1, padx=10, pady=1,
            sticky=tkinter.W + tkinter.E)

        #   ASK WINNER CONDITION:
        winner_condition_label = tkinter.Label(
            master=self._game_info_window, text='Will the game be won by the player with ("Fewer" or "More") Pieces?:',
            font=DEFAULT_FONT)

        winner_condition_label.grid(
            row=4, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self._winner_condition_entry = tkinter.Entry(
            master=self._game_info_window, width=20, font=DEFAULT_FONT)

        self._winner_condition_entry.grid(
            row=4, column=1, padx=10, pady=1,
            sticky=tkinter.W + tkinter.E)

        #   BUTTONS:
        button_frame = tkinter.Frame(master=self._game_info_window)

        button_frame.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10,
            sticky=tkinter.E + tkinter.S)

        enter_button = tkinter.Button(
            master=button_frame, text='OK', font=DEFAULT_FONT,
            command=self._on_ok_button)

        enter_button.grid(row=0, column=0, padx=10, pady=10)

        cancel_button = tkinter.Button(
            master=button_frame, text='Cancel', font=DEFAULT_FONT,
            command=self._on_cancel_button)

        cancel_button.grid(row=0, column=1, padx=10, pady=10)

        self._game_info_window.rowconfigure(3, weight=1)
        self._game_info_window.columnconfigure(1, weight=1)

        self._ok_clicked = False
        self._rows = ''
        self._columns = ''
        self._first_move = ''
        self._winner_condition = ''

    def show(self) -> None:
        """Shows the _game_info_window to the user."""
        self._game_info_window.grab_set()
        self._game_info_window.wait_window()

    def was_ok_clicked(self) -> bool:
        """Returns a bool representing whether ok was clicked."""
        return self._ok_clicked

    def get_num_rows(self) -> str:
        """Returns the self._rows variable."""
        return self._rows

    def get_num_columns(self) -> str:
        """Returns the self._columns variable."""
        return self._columns

    def get_first_move(self) -> str:
        """Returns the self._first_move variable."""
        return self._first_move

    def get_winner_condition(self) -> str:
        """Returns the self._winner_conditon variable."""
        return self._winner_condition

    def _on_ok_button(self) -> None:
        """When the okay button is pressed gets all of the entries and sets them to the object variables.
        Finishes by destroying the window."""
        self._ok_clicked = True
        self._rows = self._rows_entry.get()
        self._columns = self._columns_entry.get()
        self._first_move = self._first_move_entry.get()
        self._winner_condition = self._winner_condition_entry.get()

        self._game_info_window.destroy()

    def _on_cancel_button(self) -> None:
        """Destroys the main window when the cancel button is pressed."""
        self._game_info_window.destroy()


class PreGame:
    """The intital welcome and play button for getting the Othello Game started."""
    def __init__(self):
        """Initializes the tkinter root window and attributes (buttons, labels, etc)."""
        self._root_window = tkinter.Tk()

        welcome_label = tkinter.Label(
            master=self._root_window, text='WELCOME TO OTHELLO\n', font=DEFAULT_FONT)
        welcome_label.grid(row=0, column=0, padx=10, pady=10)

        play_button = tkinter.Button(
            master=self._root_window, text='PLAY', font=('Helvetica', 20),
            command=self._on_play)

        play_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10,
            sticky=tkinter.S)

        self._row_col_text = tkinter.StringVar()
        self._row_col_text.set('')

        greeting_label = tkinter.Label(
            master=self._root_window, textvariable=self._row_col_text,
            font=DEFAULT_FONT)

        greeting_label.grid(
            row=2, column=0, padx=10, pady=10,
            sticky=tkinter.N)

    def start(self) -> None:
        """Runs mainloop on the tkinter self._root_window."""
        self._root_window.mainloop()

    def _on_play(self) -> None:
        """Controls what to do when the play button is pressed. Runs StartGameInfo() also. Checks whether inputs
        are valid against the _check_valid function. If not runs the InvalidInput() Class.
        """

        self.game_info = StartGameInfo()
        self.game_info.show()

        if self.game_info.was_ok_clicked():
            self._rows = self.game_info.get_num_rows()
            self._cols = self.game_info.get_num_columns()
            self._first_move = self.game_info.get_first_move()
            self._winner_condition = self.game_info.get_winner_condition()

            # self._row_col_text.set('Hello, {} {}!'.format(rows, cols))

            if not self._check_valid():
                invalid = InvalidInput()
                invalid.start()
                self._on_play()

            self._segue_to_game()

    def _segue_to_game(self):
        """Once values are determined for passing to the OthelloGame object, prepares for the next stage of
        game initialization by destroying the root window """

        WINNER_CONDITION_CONVERTER = {'more': '>', 'fewer': '<'}
        WHOSE_TURN_CONVERTER = {'black': 1, 'white': -1}

        othello_game.BOARD_SIZE = (self._rows, self._cols)
        othello_game.whose_turn = WHOSE_TURN_CONVERTER[self._first_move]
        othello_game.WINNER_CONDITION = WINNER_CONDITION_CONVERTER[self._winner_condition]
        try:
            self._root_window.destroy()
        except tkinter.TclError:
            pass

    def _check_valid(self) -> bool:
        """Checks that the inputs passed are valid - returns true if all of the inputs are Valid and False if not."""
        try:
            self._rows = int(self._rows.strip(' '))
            self._cols = int(self._cols.strip(' '))
            self._first_move = self._first_move.strip(' ').lower()
            self._winner_condition = self._winner_condition.strip(' ').lower()
        except (ValueError, AttributeError):
            return False

        if 4 > self._rows > 16 or self._rows % 2 != 0 or 4 > self._cols > 16 or self._cols % 2 != 0:
            return False
        if not (self._first_move == 'black' or self._first_move == 'white'):
            return False
        if not (self._winner_condition == 'more' or self._winner_condition == 'fewer'):
            return False
        return True


class InvalidInput:
    """Controls the popup window when an invalid input is passed for any of the initial Game variables"""
    def __init__(self):
        """Initializes the tkinter _invalid_window and attributes (buttons, labels, etc)."""
        self._invalid_window = tkinter.Toplevel()

        invalid_label = tkinter.Label(master=self._invalid_window, text='Invalid Input. Please Try Again.',
                                      font=DEFAULT_FONT)
        invalid_label.grid(row=0, padx=10, pady=10)

        close_button = tkinter.Button(master=self._invalid_window, text='Close', font=DEFAULT_FONT,
                                      command=self._on_close_button)
        close_button.grid(row=1, padx=10, pady=10)

    def start(self):
        """Runs the invalid window."""
        self._invalid_window.grab_set()
        self._invalid_window.wait_window()

    def _on_close_button(self) -> None:
        """Destroys the invalid window when close button is pressed."""
        self._invalid_window.destroy()


if __name__ == '__main__':
    othello_game = OthelloGame()    #   Create a new OthelloGame object for controlling game logic.
    PreGame().start()
    BoardSelection().run()
    MainGameGui().run()