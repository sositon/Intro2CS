#################################################################
# FILE : temperature.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that contains one function
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https: None
# NOTES: None
#################################################################


def is_it_summer_yet(temp_limit, temp1, temp2, temp3):
    """
    checks if at least 2 out of the 3 temp_i are higher than the temp_limit
    :return: a boolean True or False
    """
    result = bool(temp1 > temp_limit)\
        + bool(temp2 > temp_limit) + bool(temp3 > temp_limit)
    if result < 2:
        return False
    else:
        return True
