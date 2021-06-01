import sys
import helper
import car
import board

# Constants
LEGAL_NAMES = ["Y", "B", "O", "G", "W", "R"]
LEGAL_LENGTHS = [2, 3, 4]
LEGAL_ORIENTATIONS = [0, 1]
LEGAL_DIRECTIONS = ["u", "d", "r", "l"]

INPUT_MSG = "please input your choice in the following format - name(" \
            "capital first letter), " \
            "direction(lower case letter from d, u, r, l)\n" \
            "or '!' to quit the game\n"
SUCCESS_MSG = "car moved successfully"
INVALID_MSG = "your input is invalid make sure you're following the specific " \
              "input format"
TRY_AGAIN_MSG = "can't move the car that way"
WIN_MSG = "you won!"


def create_cars_from_data(b, data_dic):
    """
    :param b: A Board object
    :param data_dic: A dictionary full with cars data to add to the board
    :return: b Board with the added cars following the game rules
    """
    for key, val in data_dic.items():
        name = key
        length, location, orientation = val
        if length not in LEGAL_LENGTHS:
            continue
        elif tuple(location) not in b.cell_list():
            continue
        elif name not in LEGAL_NAMES:
            continue
        elif orientation not in LEGAL_ORIENTATIONS:
            continue
        b.add_car(car.Car(name, length, tuple(location), orientation))
    return b


class Game:
    """
    This class define a Game object.
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume __board follows the API
        self.__board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        choice = input(INPUT_MSG)
        if choice == "!":
            return False
        if self.__check_input(choice):
            choice = choice.split(",")
            name, movekey = choice
            if self.__board.move_car(name, movekey):
                print(SUCCESS_MSG)
            else:
                print(TRY_AGAIN_MSG)
        else:
            print(INVALID_MSG)
        return True

    @staticmethod
    def __check_input(s):
        """
        :param s: A str represent the user input
        :return: True if valid, False otherwise
        """
        if len(s) != 3:
            return False
        if s[1] != ",":
            return False
        input_lst = s.split(",")
        name, movekey = input_lst
        if name not in LEGAL_NAMES:
            return False
        if movekey not in LEGAL_DIRECTIONS:
            return False
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        flag = True
        g_board = self.__board
        while flag:
            print(g_board)
            flag = self.__single_turn()
            win_cond = g_board.cell_content(g_board.target_location())
            if win_cond is not None:
                print(WIN_MSG)
                break


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.

    # Create the board for the game
    game_board = board.Board()
    # Read the json file, create cars and add them to the board
    json_file_path = sys.argv[1]
    json_file_data = helper.load_json(json_file_path)
    game_board = create_cars_from_data(game_board, json_file_data)
    # Create a game with the board we made
    game = Game(game_board)
    # Game play
    game.play()
