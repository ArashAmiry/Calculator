# package calculator
from math import nan
from enum import Enum
from Calculator_Stack import Stack

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
    # Iterate over the expression for conversion
    for i in range(len(infix_string)):
        if infix_string[i] not in OPERATORS and infix_string[i] != "(" and infix_string[i] != ")":
            num_str += str(infix_string[i])
            if i == len(infix_string) - 1:
                infix_list.append(num_str)
        else:
            if num_str != "":
                infix_list.append(num_str)  # "534"
            infix_list.append(infix_string[i])  # "+"
            num_str = ""

    for i in infix_list:

        # If the character is an operand,
        # add it to output
        if i not in OPERATORS and i != "(" and i != ")":
            postfix_list.append(i)

        # If the character is an '(', push it to stack
        elif i == "(":
            operators_stack.push(i)

        # If the scanned character is an ')', pop and
        # output from the stack until and '(' is found
        elif i == ')':
            while (not operators_stack.isEmpty()) and operators_stack.peek() != '(':
                postfix_list.append(operators_stack.pop())
            operators_stack.pop()

        # An operator is encountered
        else:
            while not operators_stack.isEmpty() and i_not_greater(i, operators_stack):
                postfix_list.append(operators_stack.pop())
            operators_stack.push(i)

    # pop all the operator from the stack
    while not operators_stack.isEmpty():
        postfix_list.append(operators_stack.pop())

    return postfix_list  # TODO


# -----  Evaluate RPN expression -------------------
def eval_postfix(postfix_tokens):
    operand_stack = Stack()
    for i in postfix_tokens:
        if i not in OPERATORS:
            operand_stack.push(i)
        elif i in OPERATORS:
            operand_one = float(operand_stack.pop())
            operand_two = float(operand_stack.pop())
            result = apply_operator(i, operand_one, operand_two)  # (5,5,+) > (10)
            operand_stack.push(result)
    return operand_stack.pop()


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
        "/": nan if d1 == 0 else d2 / d1,
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


class Assoc(Enum):
    LEFT = 1
    RIGHT = 2


def get_associativity(op: str):
    if op in "+-*/":
        return Assoc.LEFT
    elif op in "^":
        return Assoc.RIGHT
    else:
        return ValueError(OP_NOT_FOUND)


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
