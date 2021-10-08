# Python program to convert infix expression to postfix

# Class to convert the expression
from Calculator import *


class Stack:

    # Constructor to initialize the class variables
    def __init__(self):
        self.top = 0
        # This array is used a stack
        self.array = []

    # check if the stack is empty
    def isEmpty(self):
        if self.top == 0:
            return True
        else:
            return False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "Error: Can't pop an empty stack."

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)
