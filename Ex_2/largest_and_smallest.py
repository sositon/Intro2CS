#################################################################
# FILE : largest_and_smallest.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that contains two functions
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: None
#################################################################


def largest_and_smallest(num_1, num_2, num_3):
    """this function gets 3 numbers and return the largest and the smallest,
     by this order."""

    large, small = num_1, num_1
    if large <= num_2:
        large = num_2
    if large <= num_3:
        large = num_3
    if small >= num_2:
        small = num_2
    if small >= num_3:
        small = num_3
    return large, small


def check_largest_and_smallest():
    """
    this function checks largest_and_smallest() with 5 different scenarios.
    I chose to check the same number scenario (b4) and a float scenario (b5).
    :return: True if passes all 5 scenarios, and False if not.
    """
    b1 = (17, 1) == largest_and_smallest(17, 1, 6)
    b2 = (17, 1) == largest_and_smallest(1, 17, 6)
    b3 = (2, 1) == largest_and_smallest(1, 1, 2)
    b4 = (0, 0) == largest_and_smallest(0, 0.0, 0.0)
    b5 = (7.5, 7.3) == largest_and_smallest(7.5, 7.3, 7.4)
    if b1 and b2 and b3 and b4 and b5:
        return True
    else:
        return False
