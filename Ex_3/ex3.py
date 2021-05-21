def input_list():
    """ this function gets varied number inputs from the user, breaks when
    the input is empty string.
    :return: a list with all the numbers the user
    inputted and their total at the end of the list.
    """
    total = 0
    user_list = []
    while True:
        i = input()
        if not i:
            break
        user_list.append(float(i))
        total += float(i)
    user_list.append(total)
    return user_list


def inner_product(vec_1, vec_2):
    """ this function gets two vector lists, checks if they are in the same
    length and non empty.
    :return: the standard inner product of the vectors.
    """
    total = 0
    # empty lists
    if vec_1 is [] and vec_2 is []:
        return total
    # different length
    elif len(vec_1) != len(vec_2):
        return None
    else:
        for i in range(len(vec_1)):
            total += vec_1[i] * vec_2[i]
        return total


def sequence_monotonicity(sequence):
    """ the function gets a sequence and check monotonicity of the sequence.
    :param sequence: list of numbers, int or float.
    :return: a list of 4 booleans represent the type of monotonicity.
    """
    result = [True, True, True, True]
    for i in range(len(sequence) - 1):
        if sequence[i] < sequence[i+1]:
            result[2], result[3] = False, False
        if sequence[i] > sequence[i+1]:
            result[0], result[1] = False, False
        if sequence[i] == sequence[i+1]:
            result[1], result[3] = False, False
    return result


def monotonicity_inverse(def_bool):
    """ the inverse function for 'sequence_monotonicity()'
    :param def_bool: list of 4 booleans.
    :return: a sequence that represent an example for the type of monotonicity.
    """
    if def_bool == [True, True, False, False]:
        return [1, 2, 3, 4]
    elif def_bool == [True, False, False, False]:
        return [1, 1, 2, 3]
    elif def_bool == [True, False, True, False]:
        return [1, 1, 1, 1]
    elif def_bool == [False, False, True, True]:
        return [4, 3, 2, 1]
    elif def_bool == [False, False, True, False]:
        return [4, 4, 3, 2]
    elif def_bool == [False, False, False, False]:
        return [1, 0, -1, 1]
    else:
        return None


def gather_divisors(num):
    """creates a list of all the positive numbers that evenly divide a
    specified number (not including the divisor 1).
    we saw an almost identical function on class 2.5
    """
    divisors = []
    for d in range(2, num // 2 + 1):
        if num % d == 0:
            divisors.append(d)
    return divisors


def primes_for_asafi(n):
    """
    :param n: an int >= 0.
    :return: a list with n prime numbers.
    """
    primes = []
    i = 2
    while n > len(primes):
        if not gather_divisors(i):
            primes.append(i)
        i += 1
    return primes


def sum_of_vectors(vec_lst):
    """:param vec_lst: a list of vectors, filled with numbers int or float,
    all lists are on the same length.
    :return: a list that represent a sum vector of all the vectors in vec_lst.
    """
    if not vec_lst:
        return None
    sum_vec = []
    for i in range(len(vec_lst[0])):
        total = 0
        for j in range(len(vec_lst)):
            total += vec_lst[j][i]
        sum_vec.append(total)
    return sum_vec


def num_of_orthogonal(vectors):
    """:param vectors: list of vectors on the same length, filled with numbers
    int or float.
    :return: the number of orthogonal vector pairs.
    """
    result = 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            if not inner_product(vectors[i], vectors[j]):
                result += 1
    return result
