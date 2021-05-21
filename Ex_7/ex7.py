def print_to_n(n):
    """
    param:n: non-negative int
    return: None. prints all numbers up to n
    """
    if n >= 1:
        print_to_n(n - 1)
        print(n)


def test_print_to_n():
    print_to_n(5)
    print_to_n(-1)


def digit_sum(n):
    """
    param:n: none-negative int
    return: the sum of the digits of n
    """
    if n > 0:
        return n % 10 + digit_sum(n // 10)
    else:
        return 0


def test_digit_sum():
    print(digit_sum(5555))


def gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)


def is_prime(n, i=2):
    """
    param:n: int
    return: true if n is prime, false if n is not prime
    """
    if n <= 2 or not isinstance(n, int):
        return True if n == 2 else False
    else:
        if i > int(n ** 0.5):
            return True
        elif n % i == 0:
            return False
        else:
            return is_prime(n, i + 1)


def test_is_prime():
    for i in range(1000):
        print(i, is_prime(i))
    print(is_prime(5.5))


def play_hanoi(hanoi, n, src, dst, temp):
    """
    function that solves the hanoi tower problem
    """
    if n > 0:
        play_hanoi(hanoi, n - 1, src, temp, dst)
        hanoi.move(src, dst)
        play_hanoi(hanoi, n - 1, temp, dst, src)


def to_string(lst):
    return "".join(lst)


def print_sequences(char_list, n, s=""):
    """
    param:char_list: a list of chars, differs from each other
    param:n: tha length of the combinations
    return: None. print all the combinations from length n with chars from
    the list
    """
    if n >= 0:
        if n == 0:
            print(s)

        for c in char_list:
            s += c
            print_sequences(char_list, n - 1, s)
            s = s[:-1]


def print_no_repetition_sequences(char_list, n, s=""):
    """
        param:char_list: a list of chars, differs from each other
        param:n: tha length of the combinations
        return: None. print all the combinations from length n with chars from
        the list, without repetition of same chars
        """
    if n >= 0:
        if n == 0 and len(set(s)) == len(s):
            print(s)

        for c in char_list:
            s += c
            print_no_repetition_sequences(char_list, n - 1, s)
            s = s[:-1]


def test_sequences():
    print_sequences(["a"], 2)
    print_no_repetition_sequences(["a", "b", "c", "d"], 4)


def parentheses(n, open=0, close=0, s="", res=None):
    """
    param:n: number of parentheses ()
    return: a list with all the combinations of n valid parentheses
    """
    res = [] if res is None else res
    if open == close == n:
        res.append(s)
    if open < n:
        s += "("
        parentheses(n, open + 1, close, s, res)
        s = s[:-1]
    if close < open:
        s += ")"
        parentheses(n, open, close + 1, s, res)
        s = s[:-1]
    return res


def test_parentheses():
    print(parentheses(0))
    print(parentheses(1))
    print(parentheses(4))


def generate_start_points(start):
    """
    gets a tuple and generate 4 new tuples
    """
    start = list(start)
    for i in range(2):
        start[i] -= 1
        yield tuple(start)
        start[i] += 2
        yield tuple(start)
        start[i] -= 1


def flood_fill(image, start):
    """
    param:image: a list of lists filled with "*" or ".", the frame of the
    image filled with "*"
    param:start: a tuple that holds the start point coordinate
    return: None. fill the image with "*" from the starting point to
    everywhere reachable by water.
    """
    if image[start[0]][start[1]] == "*":
        return
    image[start[0]][start[1]] = "*"
    for s in generate_start_points(start):
        flood_fill(image, s)
    return


def test_fill():
    image = [['*', '*', '*', '*', '*'],
             ['*', '.', '*', '.', '*'],
             ['*', '.', '*', '.', '*'],
             ['*', '*', '*', '*', '*']]
    start = (1, 3)
    flood_fill(image, start)
    # mat = flood_fill(image, start)
    # print()
    # for m in mat:
    #     print(m)
