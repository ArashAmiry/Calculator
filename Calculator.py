# package calculator
from math import nan
from enum import Enum
from Calculator_Stack import Stack
from decimal import *

# A calculator for rather simple arithmetic expressions.
# Your task is to implement the missing functions so the
# expressions evaluate correctly. Your program should be
# able to correctly handle precedence (including parentheses)
# and associativity - see helper functions.
# The easiest way to evaluate infix expressions is to transform
# them into postfix expressions, using a stack structure.
# For example, the expression 2*(3+4)^5 is first transformed
# to [ 3 -> 4 -> + -> 5 -> ^ -> 2 -> * ] and then evaluated
# left to right. This is known as Reverse Polish Notation,
# see: https://en.wikipedia.org/wiki/Reverse_Polish_notation
#
# NOTE:
# - You do not need to implement negative numbers
#
# To run the program, run either CalculatorREPL or CalculatorGUI

MISSING_OPERAND: str = "Missing or bad operand"
DIV_BY_ZERO: str = "Division with 0"
MISSING_OPERATOR: str = "Missing operator or parenthesis"
OP_NOT_FOUND: str = "Operator not found"
OPERATORS: str = "+-*/^"


def infix_to_postfix(tokens):  # Tokens --> ["69+420+666"]
    operators_stack = Stack()
    postfix_list = []
    infix_string = tokens[0]
    infix_list = []
    num_str = ""

    # Raise error if insufficient parentheses or no operators
    if infix_string.count("(") != infix_string.count(")"):
        raise ValueError(MISSING_OPERATOR)

    # Iterate over the expression for conversion
    create_list_of_infix_string(infix_list, infix_string, num_str)

    # Convert to a postfix_list
    convert_infix_list_to_postfix_list(infix_list, operators_stack, postfix_list)

    return postfix_list  # TODO


def convert_infix_list_to_postfix_list(infix_list, operators_stack, postfix_list):
    for i in infix_list:

        # If the character is an operand, add it to output
        if i not in OPERATORS and i != "(" and i != ")":
            postfix_list.append(i)

        # If the character is an '(', push it to stack
        elif i == "(":
            operators_stack.push(i)

        # If the scanned character is an ')', pop and output from the stack until and '(' is found
        elif i == ')':
            parentheses_prioritisation(operators_stack, postfix_list)

        # An operator is encountered
        else:
            while not operators_stack.isEmpty() and i_not_greater(i, operators_stack):
                postfix_list.append(operators_stack.pop())
            operators_stack.push(i)

    # pop all the operator from the stack
    while not operators_stack.isEmpty():
        postfix_list.append(operators_stack.pop())


def parentheses_prioritisation(operators_stack, postfix_list):
    while (not operators_stack.isEmpty()) and operators_stack.peek() != '(':
        postfix_list.append(operators_stack.pop())
    operators_stack.pop()


def create_list_of_infix_string(infix_list, infix_string, num_str):
    for i in range(len(infix_string)):

        # Not an operator and not parenthesis
        if infix_string[i] not in OPERATORS and infix_string[i] != "(" and infix_string[i] != ")":
            num_str = add_to_num_string(i, infix_string, num_str)
            append_last_operand(i, infix_list, infix_string, num_str)

        # If i is an operator
        else:
            add_num_before_operator(infix_list, num_str)

            # Add multiplication operator "*" if an operand is next to a parenthesis
            add_mult_before_left_bracket(i, infix_list, infix_string)

            error_handler(i, infix_string, num_str)

            # Append operator to the list
            infix_list.append(infix_string[i])

            # Add multiplication operator "*"ultiply if an operand is next to a parenthesis
            # Code snippet needs to be after the ")" has been appended
            append_mult_right_bracket(i, infix_list, infix_string)

            # Add multiplication operator "*" if left and right parenthesis are next to each other
            mult_two_expr(i, infix_list, infix_string)

            num_str = reset_num_str(num_str)


def error_handler(i, infix_string, num_str):
    # Raise error if a number contains more than one decimal point
    handle_multiple_decimal_error(num_str)
    # Raise error if two operators are next to each other
    handle_operators_error(i, infix_string)
    # Raise error if last character is an operator
    handle_lonely_operator_error(i, infix_string)
    # Raise error if an operator and a parentheses are next to each other
    handle_operator_after_left_bracket_error(i, infix_string)
    # Raise error if an operator and a parentheses are next to each other
    handle_operator_before_right_bracket_error(i, infix_string)


def reset_num_str(num_str):
    num_str = ""
    return num_str


def mult_two_expr(i, infix_list, infix_string):
    if infix_string[i] == ")" and i != len(infix_string) - 1:
        if infix_string[i + 1] == "(":
            infix_list.append("*")


def append_mult_right_bracket(i, infix_list, infix_string):
    if infix_string[i] == ")" and i != len(infix_string) - 1:
        if infix_string[i + 1].isnumeric():
            infix_list.append("*")


def handle_operator_before_right_bracket_error(i, infix_string):
    if infix_string[i] in OPERATORS and i != len(infix_string) - 1:
        if infix_string[i + 1] == ")":
            raise ValueError(MISSING_OPERAND)


def handle_operator_after_left_bracket_error(i, infix_string):
    if infix_string[i] in OPERATORS and i != 0:
        if infix_string[i - 1] == "(":
            raise ValueError(MISSING_OPERAND)


def handle_lonely_operator_error(i, infix_string):
    if infix_string[i] in OPERATORS and i == len(infix_string) - 1:
        raise ValueError(MISSING_OPERAND)


def handle_operators_error(i, infix_string):
    if infix_string[i] in OPERATORS and i != 0:
        if infix_string[i - 1] in OPERATORS:
            raise ValueError(MISSING_OPERAND)


def handle_multiple_decimal_error(num_str):
    if num_str.count(".") > 1:
        raise ValueError("Using more than one decimal point")


def add_mult_before_left_bracket(i, infix_list, infix_string):
    if infix_string[i] == "(" and i != 0:
        if infix_string[i - 1].isnumeric():
            infix_list.append("*")


def add_num_before_operator(infix_list, num_str):
    if num_str != "":  # Append number string to list if not empty
        infix_list.append(num_str)  # "534"


def add_to_num_string(i, infix_string, num_str):
    num_str += str(infix_string[i])
    return num_str


def append_last_operand(i, infix_list, infix_string, num_str):
    if i == len(infix_string) - 1:
        infix_list.append(num_str)


# -----  Evaluate RPN expression -------------------
def eval_postfix(postfix_tokens):
    operand_stack = Stack()
    for i in postfix_tokens:
        if i not in OPERATORS:
            operand_stack.push(i)
        elif i in OPERATORS:
            math_operation_on_operands(i, operand_stack)
    return operand_stack.pop()


def math_operation_on_operands(i, operand_stack):
    operand_one = Decimal(operand_stack.pop())
    operand_two = Decimal(operand_stack.pop())
    result = apply_operator(i, operand_one, operand_two)  # (5,5,+) > (10)
    operand_stack.push(result)


# Method used in REPL
def eval_expr(expr: str):
    if len(expr) == 0:
        return nan
    tokens = expr.split()
    postfix_tokens = infix_to_postfix(tokens)
    return eval_postfix(postfix_tokens)


def apply_operator(op: str, d1: float, d2: float):
    op_switcher = {
        "+": d1 + d2,
        "-": d2 - d1,
        "*": d1 * d2,
        "/": DIV_BY_ZERO if d1 == 0 else d2 / d1,
        "^": d2 ** d1
    }
    return op_switcher.get(op, ValueError(OP_NOT_FOUND))


def get_precedence(op: str):
    op_switcher = {
        "+": 2,
        "-": 2,
        "*": 3,
        "/": 3,
        "^": 4
    }
    return op_switcher.get(op, ValueError(OP_NOT_FOUND))


# class Assoc(Enum):
#     LEFT = 1
#     RIGHT = 2


# def get_associativity(op: str):
#     if op in "+-*/":
#         return Assoc.LEFT
#     elif op in "^":
#         return Assoc.RIGHT
#     else:
#         return ValueError(OP_NOT_FOUND)
#

# ---------- Tokenize -----------------------
def tokenize(expr: str):
    return None  # TODO


# TODO Possibly more methods
def i_not_greater(i, operator_stack):
    if operator_stack.peek() in OPERATORS:
        a = get_precedence(i)
        b = get_precedence(operator_stack.peek())
        return True if a <= b else False
    else:
        return False


#   Check whether sequence str contains ANY of the items in set. """
def containsAny(str, set):
    return 1 in [c in str for c in set]
