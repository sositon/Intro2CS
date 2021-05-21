import sys

# Constants
UP = "u"
DOWN = "d"
RIGHT = "r"
LEFT = "l"
RIGHT_UP_DIAGONAL = "w"
LEFT_UP_DIAGONAL = "x"
RIGHT_DOWN_DIAGONAL = "y"
LEFT_DOWN_DIAGONAL = "z"
DIRECTIONS_STRING = "udrlwxyz"

WORD_FILE = 1
MATRIX_FILE = 2
OUTPUT_FILE = 3
DIRECTIONS = 4


def read_wordlist(filename):
    """
    :param filename: a file that is given as a parameter with words to search
    :return: a list with all the words in the file by order
    """
    try:
        with open(filename, 'r') as wordlist_file:
            words_list = wordlist_file.read().splitlines()
        return words_list
    except FileNotFoundError:
        return None


def test_read_wordlist():
    print(read_wordlist("ex5_example_files/word_list.txt"))


def read_matrix(filename):
    """
    :param filename: a file that is given as a parameter as a matrix of
    letters to search words from
    :return: creates a list of lists from the file
    """
    try:
        matrix = []
        with open(filename, 'r') as matrix_file:
            tmp_lst = matrix_file.read().splitlines()
        for line in tmp_lst:
            matrix.append(line.split(","))
        return matrix
    except FileNotFoundError:
        return None


def test_read_matrix():
    print(read_matrix("ex5_example_files/mat.txt"))


def search(word, matrix):
    """
    :param word: a string of letters that is searched in the matrix
    :param matrix: list of lists from which the word is searched
    :return: tuple that shows the word and how many times it appeared in the matrix
    """
    counter = 0
    n = len(word)
    if n and matrix:
        for line in matrix:
            for i in range(len(line)-n+1):
                if list(word) == line[i:i+n]:
                    counter += 1
    return word, counter


def test_search():
    print(search("CAT", read_matrix("ex5_example_files/mat.txt")))


def matrix_transpose(matrix):
    """
    :param matrix: list of lists
    :return: the transposed matrix
    """
    new_matrix = []
    if matrix:
        for i in range(len(matrix[0])):
            column = []
            for j in range(len(matrix)):
                column.append(matrix[j][i])
            new_matrix.append(column)
    return new_matrix


def test_matrix_transpose():
    print(matrix_transpose(read_matrix("ex5_example_files/mat.txt")))


def get_rows(matrix):
    return [[c for c in r] for r in matrix]


def get_backward_diagonals(matrix):
    """ this function adds an empty buffer to the matrix, and then takes the
    columns without the buffer cells.
    this function shift the matrix for RIGHT_DOWN and LEFT_UP diagonals
    :param matrix: a list of lists
    :return: a new list of lists with the backward diagonals in the matrix
    """
    buffer = [None] * (len(matrix) - 1)
    matrix = [buffer[i:] + row + buffer[:i] for i, row in
              enumerate(get_rows(matrix))]
    return [[column for column in row if column is not None] for row in
            zip(*matrix)]


def get_forward_diagonals(matrix):
    """ this function adds an empty buffer to the matrix, and then takes the
        columns without the buffer cells.
        this function shift the matrix for RIGHT_UP and LEFT_DOWN diagonals
        :param matrix: a list of lists
        :return: a new list of lists with the forward diagonals in the matrix
        """
    buffer = [None] * (len(matrix) - 1)
    matrix = [buffer[:i] + row + buffer[i:] for i, row in
              enumerate(get_rows(matrix))]
    return [[column for column in row if column is not None] for row in
            zip(*matrix)]


def test_diagonals():
    matrix_path = "ex5_example_files/mat.txt"
    matrix = read_matrix(matrix_path)
    print("\n")

    print(get_forward_diagonals(matrix))
    print(get_backward_diagonals(matrix))


def reverse_rows(matrix):
    """
    :param matrix: list of lists
    :return: matrix in reverse
    """
    new_matrix = []
    for row in matrix:
        row = row[::-1]
        new_matrix.append(row)
    return new_matrix


def matrix_switch(matrix, direction):
    """
    :param matrix: list of lists
    :param direction: a letter that represents the direction of searching
    words in the matrix
    :return: the new matrix that matches the direction of search
    """
    if direction is RIGHT:
        return matrix
    if direction is LEFT:
        return reverse_rows(matrix)
    if direction is DOWN:
        return matrix_transpose(matrix)
    if direction is UP:
        return reverse_rows(matrix_transpose(matrix))
    if direction is LEFT_DOWN_DIAGONAL:
        return get_forward_diagonals(matrix)
    if direction is RIGHT_UP_DIAGONAL:
        return reverse_rows(get_forward_diagonals(matrix))
    if direction is RIGHT_DOWN_DIAGONAL:
        return get_backward_diagonals(matrix)
    if direction is LEFT_UP_DIAGONAL:
        return reverse_rows(get_backward_diagonals(matrix))


def test_matrix_switch():
    matrix = read_matrix("ex5_example_files/mat.txt")
    print(matrix_switch([], "z"))


def find_words(word_list, matrix, directions):
    """
    :param word_list: list of words to search
    :param matrix: a list of lists
    :param directions: string of letters that indicates the search direction in
    the matrix
    :return: list of tuples (word(str), count(int)) for each one of the words
    from the word_list
    """
    return_list = []
    directions_set = set(directions)
    for direction in directions_set:
        matrix_tmp = matrix_switch(matrix, direction)
        for word in word_list:
            result = search(word, matrix_tmp)
            if result[1] != 0:
                return_list.append(result)
    return list_of_tuples_merged(return_list)


def test_find_words():
    directions = "udlrwxyz"
    word_list = read_wordlist("ex5_example_files/word_list.txt")
    matrix = read_matrix("ex5_example_files/mat.txt")
    print()
    return find_words(word_list, matrix, directions)


def list_of_tuples_merged(results):
    """
    :param results: a list of tuples that holds (word, counter).
    :return: a new list that merged identical words and sum up the counter.
    """
    dic = dict()
    new_results = []
    for i, j in results:
        dic.setdefault(i, []).append(j)
    for k, v in dic.items():
        tup = k, sum(v)
        new_results.append(tup)
    return new_results


def write_output(results, filename):
    """
    :param results: list of tuples (word(str), count(int)) for each one of
    the words from the word_list
    :param filename: the outfile name, to write the results
    :return: creates a file and writes the results in the file
    """
    with open(filename, 'w') as output_file:
        for tup in results:
            output_file.write(tup[0]+","+str(tup[1])+"\n")


def test_write_output():
    results = test_find_words()
    print(results)
    write_output(results, "output.txt")
    with open("output.txt") as output_file:
        print(output_file.read())


def main(parameter_list):
    """
    :param parameter_list:
    :return:
    """
    words_list = read_wordlist(parameter_list[WORD_FILE])
    matrix = read_matrix(parameter_list[MATRIX_FILE])
    if len(parameter_list) != 5:
        return print("Should be given 4 parameters.")
    elif words_list is None or matrix is None:
        return print("word_file doesn't exist.")
    for direction in parameter_list[DIRECTIONS]:
        if direction not in DIRECTIONS_STRING:
            return print("directions parameter is invalid.")
    result_list = find_words(words_list, matrix, parameter_list[DIRECTIONS])
    write_output(result_list, parameter_list[OUTPUT_FILE])


if __name__ == '__main__':
    main(sys.argv)
