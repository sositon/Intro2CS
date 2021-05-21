import hangman_helper as helper
# message constants
INITIAL_MSG = "Good luck!\n"
INVALID_MSG = "Your input is invalid, please try again.\n"
REPETITIVE_MSG = "You tried this letter before, please try again.\n"
CORRECT_GUESS_MSG = "You guessed a letter in the word!\n"
WRONG_GUESS_MSG = "You guessed a letter that isn't part of the word.\n"
CORRECT_WORD_MSG = "You guessed the word correctly!\n"
WRONG_WORD_MSG = "Wrong word.\n"
HINT_MSG = "You asked for a hint.\n"
WIN_MSG = "You won!\n"
LOSE_MSG = "You lost the game, "


def list_to_string(lst):
    """unpack a list to a string"""
    try:
        return "".join(lst)
    except TypeError:
        print("list_to_string() - TypeError")


def check_order_word_pattern(word, pattern):
    """
    this function checks a word and a pattern for filter_words_list()
    :param word: a word from the words base, type string
    :param pattern: the pattern of the actual word, type string
    :return: False if the word doesn't match to the pattern by the order of
    the letters, else return True
    """
    let_in_pattern = []
    for i, let in enumerate(pattern):
        if let != "_":
            let_in_pattern.append(let)
            if let != word[i]:
                return False

    for i, let in enumerate(word):
        if let in let_in_pattern and pattern[i] == "_":
            return False

    return True


def check_if_in_wrong_list(word, wrong_guess_lst):
    """
    check if wrong letters the player guessed are in the word
    :param word: a word from the words base, type string
    :param wrong_guess_lst: a list of chars the isn't part of the actual word
    :return: False if in the word, else return True
    """
    for wrong in wrong_guess_lst:
        if wrong in word:
            return False
    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    :param words: a list of words
    :param pattern: a string of the word game with hidden letters shown as '_'
    :param wrong_guess_lst: a list contains letters that aren't in the pattern
    :return: a list of potentially words that could fit the pattern
    """
    hint_lst = []
    for word in words:
        # check if the length of the word and the pattern are matched
        if len(word) != len(pattern):
            continue

        # check if the order of the word and the letters are matched
        if not check_order_word_pattern(word, pattern):
            continue

        # check if wrong letters the player guessed are in the word
        if not check_if_in_wrong_list(word, wrong_guess_lst):
            continue

        # word passed all conditions
        hint_lst.append(word)
    return hint_lst


def update_word_pattern(word, pattern, letter):
    """
    :param word: a random word from Type str.
    :param pattern: the word pattern with missing letters replaced by "_",
    Type str with the same length as the word param.
    :param letter: a single letter, Type str.
    :return: updated pattern based on the letter and the word.
    """
    try:
        if letter not in word:
            return pattern
        p = list(pattern)
        for i in range(len(word)):
            if word[i] == letter:
                p[i] = letter
        return list_to_string(p)
    except TypeError:
        print("update_word_pattern() - TypeError")


def run_single_game(words_list, score):
    """
    This function initiates a new game
    :param words_list: A list containing a database of words used in the game
    :param score: The number of points the game starts with
    :return: The final score of the player
    """
    # initialize game
    game_word = helper.get_random_word(words_list)
    wrong_list = []
    pattern = "_" * len(game_word)
    msg = INITIAL_MSG
    # play game
    while "_" in pattern and score:
        helper.display_state(pattern, wrong_list, score, msg)
        choice = helper.get_input()
        # choice is a letter
        if choice[0] == helper.LETTER:
            if len(choice[1]) > 1 or choice[1].isupper() or not \
                    choice[1].isalpha():
                msg = INVALID_MSG
            elif choice[1] in wrong_list or choice[1] in pattern:
                msg = REPETITIVE_MSG
            else:
                score -= 1
                if choice[1] in game_word:
                    pattern = update_word_pattern(game_word, pattern,
                                                  choice[1])
                    n = pattern.count(choice[1])
                    score += (n * (n + 1)) // 2
                    msg = CORRECT_GUESS_MSG
                    continue
                else:
                    if choice[1] not in wrong_list:
                        wrong_list.append(choice[1])
                        msg = WRONG_GUESS_MSG
        # choice is a word
        if choice[0] == helper.WORD:
            score -= 1
            if choice[1] == game_word:
                n = pattern.count("_")
                score += (n * (n + 1)) // 2
                pattern = game_word
                msg = CORRECT_WORD_MSG
            else:
                msg = WRONG_WORD_MSG
        # choice is a hint
        if choice[0] == helper.HINT:
            score -= 1
            msg = HINT_MSG
            hint_lst = filter_words_list(words_list, pattern, wrong_list)
            if len(hint_lst) > helper.HINT_LENGTH:
                hint_lst_temp = []
                n = len(hint_lst)
                for i in range(helper.HINT_LENGTH):
                    hint_lst_temp.append(hint_lst[i * n // helper.HINT_LENGTH])
                helper.show_suggestions(hint_lst_temp)
            else:
                helper.show_suggestions(hint_lst)
    # end of the game
    if pattern == game_word:
        msg = WIN_MSG
    else:
        msg = LOSE_MSG + "the word was {}".format(game_word)
    helper.display_state(pattern, wrong_list, score, msg)
    return score


def main():
    """
    The flow of the game
    :return: None
    """
    words_list = helper.load_words()
    points = run_single_game(words_list, helper.POINTS_INITIAL)
    counter = 1
    flag = True
    while flag:
        # Player won
        if points > 0:
            flag = helper.play_again("You played {} games so far and your "
                                     "score is {}, do you want to play "
                                     "again?".format(counter, points))
            if flag:
                counter += 1
                points = run_single_game(words_list, points)
        # Player lost
        else:
            flag = helper.play_again("You survived {} games so far, do you "
                                     "want"
                                     " to play again?".format(counter))
            if flag:
                counter = 1
                points = run_single_game(words_list, helper.POINTS_INITIAL)


if __name__ == "__main__":
    main()
