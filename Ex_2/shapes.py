#################################################################
# FILE : shapes.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that contains four functions
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https: None
# NOTES: None
#################################################################
import math


def circle_area(radius):
    """returns the area of a circle."""
    return math.pi * math.pow(radius, 2)


def rectangle_area(side_1, side_2):
    """returns the area of a rectangle."""
    return side_1 * side_2


def equilateral_triangle(side):
    """returns the area of a equilateral triangle."""
    return (math.sqrt(3)/4) * math.pow(side, 2)


def shape_area():
    """
    the user chooses a shape circle, rectangle or triangle. and insert the data
    needed for the calculation.
    :return: the specific shape area the user picked.
    """
    s1 = float(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))
    if s1 not in (1, 2, 3):
        return None
    if s1 == 1:
        return circle_area(float(input()))
    elif s1 == 2:
        return rectangle_area(float(input()), float(input()))
    else:
        return equilateral_triangle(float(input()))
