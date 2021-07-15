from tkinter import *
from boggle_board_randomizer import *
from ex12_utils import *


class BoggleGame:
    """
    A class that contains all the elements of a boggle game
    """
    # Constants
    TIME = 180  # seconds
    STARTING_SCORE = 0
    DEFAULT_PATH_LEN = 0
    STARTING_LIFE = 3

    # words strength
    WORDS_STRENGTH = {1: 'lame ', 2: 'weak ', 3: '', 4: 'cool ',
                      5: 'fantastic ', 6: 'crazy ', 7: 'super ',
                      8: 'ludicrous ', 9: 'ludicrous ', 10: 'ludicrous ',
                      11: 'ludicrous ', 12: 'ludicrous ', 13: 'ludicrous ',
                      14: 'ludicrous ', 15: 'ludicrous ',
                      16: 'ludicrous '}

    # Messages
    START_MES = 'Start'
    SCORE_MES = "Score - "
    CHECK_WORD_MES = 'Check word'
    QUIT_MES = 'Quit game'
    HINT_MES = 'Hint'
    INITIAL_PHRASE = "Let's Rock!"
    HEART = '❤'
    GAME_OVER_MES = "Game over"
    YES_BUT = "Yes!"
    NO_BUT = "No, I want my mommy!"
    ALREADY_GUESSED = "You already guessed this word.\nTry again!"
    NO_SUCH_WORD = 'There is no such word! \nYou lose 1 life!'
    WON_MES = "You Won!!!!"

    def __init__(self, parent, board, words):
        """
        A function that sets the initial parameters in order to run the game.
        :param parent: Tk object, the main window where the
        programme will appear.
        :param board: list of lists that contains the letters of each cube,
        every list represent a row, and each value inside represent a cube.
        :param words: list, a list with all the valid words
        """
        self.__parent = parent
        self.__board = board
        self.__words = words

        # operational
        self.__word = ''
        self.__life_remaning = self.STARTING_LIFE
        self.__path_len = self.DEFAULT_PATH_LEN
        self.__correct_words = []
        self.__score = self.STARTING_SCORE
        self.show_start_button()
        self.stop_time = False
        self.max_paths = max_score_paths(self.__board, self.__words)
        self.all_words = self.all_words_on_board()

    def show_start_button(self):
        """
        Puts the start button on the screen, and prepares it to start the game
        """
        # creates the button
        self.__start_button = Button(self.__parent, text=self.START_MES,
                                     font=("Courier", 72), command=lambda:
            [self.__init_game(),
             self.start_time
             (self.TIME, self.timer_label),
             self.__start_button.destroy(),
             self.__timer.grid(row=2, column=0)])
        # puts the button on the screen
        self.__start_button.grid(row=0, column=0)

    def press_a_button(self, name, i, j):
        """
        The function that handel the operations after pressing on of the cubes.
        The function takes the letters on the cube, adds them to the screen
        and disable all the cubes that are now impossible to press on.
        :param name: string, the letters on the cube
        :param i: int, the row location of the cube
        :param j: int, the column location of the cube
        :return: an execution of the inner function
        """

        def sup_saver():
            self.add_path()  # adds one to the len of the path
            self.add_box(name)  # adds the name of the cube as an input
            self.__pressed_buttons.append((i, j))  # mark the button as pressed
            if '!' in self.chosen_letters_box.get('0.0', END):
                self.chosen_letters_box.delete('0.0', END)
                # clears the messages and letters display
            self.chosen_letters_box.insert(END, name)
            self.chosen_letters_box.insert(END, '  ')
            # adds the letters on the cube to the display
            self.__hint_button.config(state=DISABLED)
            self.__cells[i, j].config(state=DISABLED)
            self.__cells[i, j].grid(row=i, column=j)
            # disable the hint button and the cube ^

            # disable all the cubes that are not neighbours
            for cell in self.__cells.keys():
                if abs(cell[X] - i) > 1 or abs(cell[Y] - j) > 1:
                    # not neighbours
                    self.__cells[cell[X], cell[Y]].config(state=DISABLED)
                    self.__cells[cell[X], cell[Y]].grid \
                        (row=cell[X], column=cell[Y])
                elif i == cell[X] and j == cell[Y] or (cell[X], cell[Y]) \
                        in self.__pressed_buttons:
                    # same cell or already was pressed
                    pass
                else:  # neighbours
                    self.__cells[cell[X], cell[Y]].config(state=NORMAL)
                    self.__cells[cell[X], cell[Y]].grid \
                        (row=cell[X], column=cell[Y])

        return sup_saver

    def __init_game(self):
        """
        Starts the game after pressing the start button
        """
        # creates the board
        self.__cells = dict()
        self.__pressed_buttons = []
        self.__board_frame = Frame(self.__parent)
        # generates a frame for the board
        self.__board_frame.grid(row=3, column=0)  # locates the frame
        # creates each cube and puts it in it's spot
        for i, rw in enumerate(self.__board):
            for j, name in enumerate(self.__board[i]):
                self.__cells[i, j] = Button(self.__board_frame,
                                            text=name, width=4, height=2,
                                            font=("Courier", 30),
                                            command=self.press_a_button
                                            (name, i, j), state=NORMAL)
                self.__cells[i, j].grid(row=i, column=j)

        # score
        self.__score_frame = Frame(self.__parent, bg='lightgrey')
        # generates a frame for the board and locates it
        self.__score_frame.grid(row=0, column=0)
        # creates the first half of the score (the name "score")
        self._score_label_1 = Label(self.__score_frame, text=self.SCORE_MES,
                                    font=("Courier", 30), bg='lightgrey') \
            .grid(row=0, column=0)
        # creates the second half of the score (the actual point)
        self._score_label_2 = Label(self.__score_frame,
                                    text=self.__score, bg='lightgrey') \
            .grid(row=0, column=1)

        # check button
        self.__buttons_frame = Frame(self.__parent)
        # generates a frame for the check button and locates it
        self.__buttons_frame.grid(row=4, column=0)
        # creates the button itself and puts it on the display
        self.__check_button = Button(self.__parent,
                                     text=self.CHECK_WORD_MES,
                                     font=("Courier", 30),
                                     command=lambda:
                                     [self.word_checker
                                      (self.__word, self.__words),
                                      self.reset_word()])
        self.__check_button.grid(row=4, column=0)

        # quit button
        self.__quit_button = Button(self.__score_frame, text=self.QUIT_MES,
                                    font=("Courier", 15), width=10,
                                    command=lambda: [self.close()],
                                    bg='lightgrey')
        # generates a button for the quit button and locates it
        # generates a separator for visual needs
        self.__separator_1 = Label(self.__score_frame, width=5,
                                   bg='lightgrey').grid(row=0, column=2)
        self.__separator_2 = Label(self.__score_frame, width=5,
                                   bg='lightgrey').grid(row=0, column=4)
        self.__quit_button.grid(row=0, column=5)

        # hint button
        self.__hint_button = Button(self.__score_frame, text=self.HINT_MES,
                                    font=("Courier", 15),
                                    width=10, command=lambda: self.get_hint(),
                                    bg='lightgrey')
        # generates a button for the hint button and locates it
        self.__hint_button.grid(row=1, column=5)

        # correct words box
        self.correct_words_box = Text(self.__parent, width=25,
                                      height=15,
                                      wrap=WORD, background='white',
                                      font=("Courier", 25))
        # generates a textbox for the correct words and locates it
        self.correct_words_box.grid(row=5, column=0)

        # chosen letters + messages
        self.chosen_letters_box = Text(self.__parent, width=25,
                                       height=5, wrap=WORD,
                                       background='white',
                                       font=("Courier", 20))
        # generates a textbox for the letters an messages and locates it
        self.chosen_letters_box.insert(END, self.INITIAL_PHRASE)
        # the initial phrase
        self.chosen_letters_box.grid(row=1, column=0)

        # life
        self.life_frame = Frame(self.__score_frame)
        # generates a frame for the hearts (remaining life) and locates it
        for i in range(self.__life_remaning):
            heart = Label(self.life_frame, text=self.HEART,
                          bg='lightgrey', font=("Courier", 50),
                          width=1, height=1, fg='red')
            # adds hears according to the amount of life that remains
            heart.grid(row=0, column=i)  # locate each heart
        self.life_frame.grid(row=0, column=3)  # locate the life frame

        # timer
        self.timer_label = StringVar()
        self.timer_label.set(self.TIME)
        # generates a label for the timer and the timer itself,
        # not starting the timer yet
        self.__timer = Label(self.__parent,
                             textvariable=self.timer_label, font=("Courier",20)
                             , width=10)
        self.stop_time = False

    def start_time(self, time, label):
        """
        starting the time of the timer
        :param time: int the reamaining time in seconds
        :param label: string, the amount of time writen on the timer
        """
        if time > 0:
            # if time did not run out reduce 1 second and update the timer
            time -= 1
            label.set(time)
            if self.stop_time is False:
                # stops the timer when the game is not running
                self.__parent.after(1000, lambda: self.start_time(time, label))
        else:  # when the time run out - end the game
            self.game_over()

    def close(self):
        """
        closing the programme
        """
        self.__parent.destroy()

    def game_over(self):
        """
        Disable all the buttons and stops the timer
        """
        for cell in self.__cells.keys():
            # Disable all the buttons
            self.__cells[cell[X], cell[Y]].config(state=DISABLED)
            self.__cells[cell[X], cell[Y]].grid(row=cell[X], column=cell[Y])
        self.__check_button.config(state=DISABLED)
        self.__quit_button.config(state=DISABLED)
        self.__hint_button.config(state=DISABLED)
        # Stops the timer
        self.stop_time = True
        # open the play again popup
        self.play_again()

    def play_again(self):
        """
        Creates a popup that allows the user to play again or to close
        the programme. The popup also tells the player how many points
        he scored in the last round.
        """
        popup = Toplevel()
        popup.wm_title(self.GAME_OVER_MES)
        # creates the a popup and its message
        popup_label = Label(popup, text=f"You've scored {self.__score} "
                                        f"points! \nDo you want to play again?")
        popup_label.grid(row=0, column=1)

        # creates the yes - play again button and locates it on th popup
        play_again_button = Button(popup, text=self.YES_BUT,
                                   command=lambda: [popup.destroy(),
                                                    self.shuffle_board(),
                                                    self.restart_game(),
                                                    self.show_start_button()])
        play_again_button.grid(row=1, column=0)

        # creates the no - close programme button and locates it on the popup
        exit_button = Button(popup, text=self.NO_BUT, command=lambda:
        [popup.destroy(), self.close()])
        exit_button.grid(row=1, column=2)

    def word_checker(self, word, words_list):
        """
        Checks if the word that the user chose is valid, and if not
        reduces one life. If the user have found all the words on
        the table, opens a winner popup and if the user run out of life,
        opens the game over popup.
        :param word: string, the word that the user chose
        :param words_list: list, all the valid words
        """
        if word in words_list and word not in self.__correct_words:
            # if the word is valid
            # update the score
            self.__score += self.score_calc()
            self.__score_update()
            self.__correct_words.append(word)
            # puts the word on the board and announce about it
            self.correct_words_box.insert(END, word)
            self.correct_words_box.insert(END, '    ')
            self.chosen_letters_box.delete('0.0', END)
            self.chosen_letters_box.insert(END, f"You've found a"
                    f" {self.WORDS_STRENGTH [len(word)]}word! \nYou received"
                    f" {self.score_calc()} points!")
        elif word in self.__correct_words:
            # if the word already guessed by the user
            self.chosen_letters_box.delete('0.0', END)
            self.chosen_letters_box.insert(END, self.ALREADY_GUESSED)
        else:
            # if the word is not valid
            # takes down one life and give a message about it
            self.__life_remaning -= 1
            self.life_frame.winfo_children()[-1].destroy()
            self.chosen_letters_box.delete('0.0', END)
            self.chosen_letters_box.insert(END, self.NO_SUCH_WORD)

        # prepare for the next word
        self.__pressed_buttons.clear()
        self.__path_len = self.DEFAULT_PATH_LEN
        self.__hint_button.config(state=NORMAL)

        # Checks if the game is over
        if self.__life_remaning == 0:  # lose
            self.game_over()
        elif len(self.__correct_words) == len(self.all_words):  # won
            self.game_won()
        else:
            for cell in self.__cells.keys():  # no winner or loser this round
                # enable all the cubes
                self.__cells[cell[X], cell[Y]].config(state=NORMAL)
                self.__cells[cell[X], cell[Y]].grid(row=cell[X],
                                                    column=cell[Y])

    def add_box(self, box):
        """
        adds the letters on the chosen cube to the generated word
        :param box: string, the letters in the chosen cube
        """
        self.__word += box

    def shuffle_board(self):
        """
        Removes the existing board and gives a new one
        """
        self.__board_frame.destroy()
        self.__board = randomize_board()

    def score_calc(self):
        """
        Calculates the amount of point a word is worth
        :return: int, the amount of point to add to the score
        """
        return 2 ** self.__path_len

    def add_path(self):
        """
        Adds one to the existing path len
        """
        self.__path_len += 1

    def restart_game(self):
        """
        prepares the programme into another round of the game
        """
        # reset the parameters
        self.__word = ''
        self.__correct_words = []
        self.__score = self.STARTING_SCORE
        self.chosen_letters_box.delete('0.0', 'end')
        self.__score_update()
        self.correct_words_box.delete('0.0', 'end')
        self.__life_remaning = self.STARTING_LIFE

        # Destroys the existing texts, frames and buttons
        self.__check_button.destroy()
        self.__quit_button.destroy()
        self.__hint_button.destroy()
        self.chosen_letters_box.destroy()
        self.correct_words_box.destroy()
        self.__score_frame.destroy()
        self.__timer.destroy()
        self.life_frame.destroy()

        # Resets the timer
        self.timer_label = StringVar()
        self.timer_label.set(self.TIME)
        self.__timer = Label(self.__parent, textvariable=self.timer_label,
                             font=("Courier", 20), width=10)

        # Calculates what are the new words on the new board
        self.max_paths = max_score_paths(self.__board, self.__words)
        self.all_words = self.all_words_on_board()

    def reset_word(self):
        """
        Deletes all the letters in current attempt to find a word
        """
        self.__word = ''

    def __score_update(self):
        """
        Changes the scoreboard into the current score
        """
        self._score_label_2 = Label(self.__score_frame,
                                    text=self.__score).grid(row=0, column=1)

    def all_words_on_board(self):
        """
        Calculates all the valid words on the board.
        The function goal is to check when the user have found
        all the words on the board and won the game.
        :return: list, with all the valid words on the board
        """
        words = []
        for path in self.max_paths:
            temp_word = []
            for letter in path:
                temp_word.append(self.__board[letter[X]][letter[Y]])
                # generates every word from the paths and adds it to the list
            words.append(''.join(temp_word))
        return words

    def game_won(self):
        """
        Disable all the buttons and stops the timer
        """
        for cell in self.__cells.keys():
            # disable all the buttons
            self.__cells[cell[X], cell[Y]].config(state=DISABLED)
            self.__cells[cell[X], cell[Y]].grid(row=cell[X], column=cell[Y])
        self.__check_button.config(state=DISABLED)
        self.__quit_button.config(state=DISABLED)
        # stops the timer
        self.stop_time = True
        # opens the winner popup
        self.winner_play_again()

    def winner_play_again(self):
        """
        Creates a popup that allows the user to play again or to close
        the programme. The popup also tells the player how many points
        he scored in the last round.
        """
        popup = Toplevel()
        popup.wm_title(self.WON_MES)
        # creates the a popup and its message
        popup_label = Label(popup, text=f"You've found all the words"
                                        f" on the board and received"
                                        f" {self.__score} points! Well done! "
                                        f"\nDo you want to play again?")
        popup_label.grid(row=0, column=1)

        # creates the yes - play again button and locates it on th popup
        play_again_button = Button(popup, text=self.YES_BUT,
                                   command=lambda: [popup.destroy(),
                                                    self.shuffle_board(),
                                                    self.restart_game(),
                                                    self.show_start_button()])
        play_again_button.grid(row=1, column=0)

        #  creates the no - close programme button and locates it on the popup
        exit_button = Button(popup, text=self.NO_BUT, command=lambda:
        [popup.destroy(), self.close()])
        exit_button.grid(row=1, column=2)

    def get_hint(self):
        """
        Changes the first letter of a word into green and back to black
        """
        for i, word in enumerate(self.all_words):
            if word not in self.__correct_words:
                break
        # find a word that the user have'nt found yet
        hint_loc = self.max_paths[i][X]
        # Changes the color of the first letter of the word into green
        self.__cells[hint_loc[X], hint_loc[Y]].config(fg='green')
        # Changes back the color of the letter to black
        self.__parent.after(1500, lambda:
        self.__cells[hint_loc[X], hint_loc[Y]].config(fg='black'))


if __name__ == '__main__':
    root = Tk()
    root.wm_title("Boggle Game")

    board = randomize_board()
    with open("boggle_dict.txt") as words_file:
        words = set(words_file.read().splitlines())

    BoggleGame(root, board, words)
    root.mainloop()
