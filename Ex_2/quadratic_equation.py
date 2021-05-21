#################################################################
# FILE : quadratic_equation.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that contains two functions
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https: https://en.wikipedia.org/wiki/Quadratic_equation
# NOTES: None
#################################################################
import math


def quadratic_equation(a, b, c):
    """this function gets 3 coefficients stands for ax^2 + bx + c = 0 and
    returns the solutions for the equation."""

    discriminant = math.pow(b, 2) - 4 * a * c
    if discriminant < 0:
        return None, None
    elif discriminant == 0:
        return -b / (2 * a), None
    else:
        discriminant = math.sqrt(discriminant)
        return (-b + discriminant) / (2 * a), (-b - discriminant) / (2 * a)


def quadratic_equation_user_input():
    """this function collects input from the user of 3 coefficients stands for
    ax^2 + bx + c = 0 and print, the number of solutions and the solutions of
    the equation. if a = 0 it will print an error massage."""

    s = input("Insert coefficients a, b, and c: ")
    s = s.split(" ")
    if float(s[0]) == 0:
        print("The parameter 'a' may not equal 0")
        return
    result = quadratic_equation(float(s[0]), float(s[1]), float(s[2]))
    if (None, None) == result:
        print("The equation has no solutions")
    elif None in result:
        print("The equation has 1 solution: {}".format(result[0]))
    else:
        print("The equation has 2 solutions: {} and {}".format(result[0],
                                                               result[1]))
