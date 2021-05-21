#################################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Omer Siton , omer_siton , 316123819
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that contains two mathematical functions
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https://en.wikipedia.org/wiki/Binary_operation,
#                                       https://en.wikipedia.org/wiki/Operand
# NOTES: None
#################################################################


def calculate_mathematical_expression(operand_1, operand_2, binary_operation):
    """this function gets 3 parameters, the first two are numbers(int or float)
    and the third one is a character that represent the desired operation.
    return the mathematical result."""

    if binary_operation == '+':
        return operand_1 + operand_2
    elif binary_operation == '-':
        return operand_1 - operand_2
    elif binary_operation == '*':
        return operand_1 * operand_2
    elif binary_operation == ':' and operand_2 != 0:
        return operand_1 / operand_2
    else:
        return None


def calculate_from_string(string):
    """this function gets a string with two operands and an operation separated
     by spaces. return the mathematical result."""

    string = string.split(" ")
    return calculate_mathematical_expression(float(string[0]),
                                             float(string[2]), string[1])
