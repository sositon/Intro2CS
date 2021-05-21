#################################################################
# FILE : math_print.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex1 2021
# DESCRIPTION: A simple program that prints some mathematical values using math module
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: ...
#################################################################
import math


def golden_ratio():
    """this function prints the golden ratio - a mathematical const"""
    print(2 * (math.cos(math.pi / 5)))


def six_squared():
    """this function prints 6 to the power of 2"""
    print(math.pow(6, 2))


def hypotenuse():
    """this function prints the hypotenuse length in a right triangle with sides of 5, 12"""
    print(math.sqrt(math.pow(5, 2) + math.pow(12, 2)))


def pi():
    """this function prints the pi number value"""
    print(math.pi)


def e():
    """this function prints the e number value"""
    print(math.e)


def squares_area():
    """this function prints the squares area of 10 squares with sides length between 1 to 10 """
    print(math.pow(1, 2), math.pow(2, 2), math.pow(3, 2), math.pow(4, 2), math.pow(5, 2), math.pow(6, 2),
                                                    math.pow(7, 2), math.pow(8, 2), math.pow(9, 2), math.pow(10, 2))


if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
