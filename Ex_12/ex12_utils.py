# Constants
X = 0
Y = 1


def _adjacent_coordinates(cord_1, cord_2):
    """
    :param cord_1: a tuple of coordinates
    :param cord_2: a tuple of coordinates
    :return: True if they are adjoin
    """
    return abs(cord_2[X] - cord_1[X]) <= 1 and abs(cord_2[Y] - cord_1[Y]) <= 1


def is_valid_path(board, path, words):
    """
    :param board: list of lists represent the game board
    :param path: a list of coordinates in tuples
    :param words: a container that hold the game words data
    :return: a word if the path is valid and creates a word in words. else None
    """
    # check no repetition
    word = ""
    if len(set(path)) != len(path):
        return None
    for i, cord in enumerate(path):
        # check if in board limits
        x, y = cord
        if x not in range(len(board)) or y not in range(len(board)):
            return None
        # check if adjacent
        if i > 0:
            if not _adjacent_coordinates(path[i - 1], path[i]):
                return None
        word += board[x][y]
    # check if word in words
    if word not in words:
        return None

    return word


def find_length_n_paths(n, board, words):
    """
    :param n: length of paths to find
    :param board: list of lists represent the game board
    :param words: a container that hold the game words data
    :return: list of all paths from length n that are valid and creates a word in words.
    """
    return find_length_n_helper(n, board, words, path_filter=True)


def find_length_n_words(n, board, words):
    """
    :param n: length of paths to find
    :param board: list of lists represent the game board
    :param words: a container that hold the game words data
    :return: list of all legal words from length n.
    """
    return find_length_n_helper(n, board, words)


def still_in_board(board, cord):
    """:return True if cord in board"""
    return 0 <= cord[X] < len(board) and 0 <= cord[Y] < len(board[X])


def max_score_paths(board, words):
    """
    :param board:  list of lists represents the game board
    :param words: a container that hold the game words data
    :return: list of the longest path for each word in board.
    """
    word_to_paths = {word: [] for word in words}

    def fill_found_paths(left_from_word, current_path):
        """:return a path for every word in board"""
        if not left_from_word:
            word_to_paths[path_to_word(board, current_path)].append(
                current_path)
            return
        for next_cord in generate_neighbors(current_path[-1]):
            if next_cord not in current_path:
                if still_in_board(board, next_cord):
                    if board[next_cord[X]][next_cord[Y]] == left_from_word[0]:
                        fill_found_paths(left_from_word[1:],
                                         current_path + [next_cord])

    def max_len_path(paths):
        """:return the longest path for each word"""
        max_len_path, max_len = None, 0
        for path in paths:
            if len(path) > max_len:
                max_len = len(path)
                max_len_path = path
        return max_len_path

    # function call
    for i in range(len(board)):
        for j in range(len(board[i])):
            for word in words:
                if board[i][j] == word[0]:
                    fill_found_paths(word[1:], [(i, j)])

    return [max_len_path(paths) for paths in word_to_paths.values() if paths]


def find_length_n_helper(n, board, words, path_filter=False):
    """ help function to save double code of functions find_words/paths"""
    res = []
    if not 0 < n <= len(board)**2:
        return res
    if path_filter:
        words = [word for word in words if n <= len(word)]
    else:
        words = [word for word in words if n == len(word)]
    board_cords = [(i, j) for i in range(len(board)) for j in range(len(board))]
    for cord in board_cords:
        res.extend(path_permutations(n, board, words, cord, [], path_filter))
    return res


def path_permutations(n, board, words, cord, path, path_filter=False):
    """
    :param n: an integer
    :param board: list of lists represents the game board
    :param words: a container that hold the game words data
    :param cord: a tuple of coordinates
    :param path: list of cords
    :param path_filter: distinguish between functions find_words/paths
    :return: all valid path permutations in board
    """
    path.append(cord)
    if path_filter:
        if len(path) >= n:
            if is_valid_path(board, path, words):
                yield path
            return
    else:
        if len(path) == n:
            if is_valid_path(board, path, words):
                yield path
            return

    for new_cord in generate_neighbors(cord):
        path_copy = path.copy()
        if still_in_board(board, cord):
            yield from path_permutations(n, board, words, new_cord, path_copy,
                                         path_filter)


def generate_neighbors(cur):
    """
    gets a tuple and generate 8 new tuples represent neighbors of the
    current cord in a 2D matrix
    """
    cur = list(cur)
    for i in range(2):
        cur[i] -= 1
        yield tuple(cur)
        cur[i] += 2
        yield tuple(cur)
        cur[i] -= 1
    yield cur[X] - 1, cur[Y] - 1
    yield cur[X] - 1, cur[Y] + 1
    yield cur[X] + 1, cur[Y] + 1
    yield cur[X] + 1, cur[Y] - 1


def path_to_word(board, path):
    word = ''
    for cord in path:
        x, y = cord
        word += board[x][y]
    return word
