import math
from typing import List, Union, Optional
import re

# To define an ordering on operations, this represents PEMDAS, can be changed to represent other orderings.
# Lower number represents higher precedence.
PRECEDENCE={'^': 0, '*': 1, '/': 2, '+': 3, '-': 4}


def create_toplevel_tokens(input_str: str) -> List[str]:
    """Takes a string and returns a list of top level tokens.
    Top level tokens include '+', '-', '*', '/', numbers and bracketed expressions.

    >>> create_toplevel_tokens("1 + 2 - 35 / (7 * 5)")
    ['1', '+', '2', '-', '35', '/', '(7 * 5)']
    """
    tokens = []
    while input_str:
        if input_str[0] == " ":
            input_str = input_str[1:]
        elif match := re.match('[0-9]+(\\.[0-9]+)?', input_str):
            number = match.group(0)
            tokens.append(number)
            input_str = input_str[len(number):]
        elif input_str[0] == '+':
            tokens.append('+')
            input_str = input_str[1:]
        elif input_str[0] == '-':
            tokens.append('-')
            input_str = input_str[1:]
        elif input_str[0] == '*':
            tokens.append('*')
            input_str = input_str[1:]
        elif input_str[0] == '/':
            tokens.append('/')
            input_str = input_str[1:]
        elif input_str[0] == '^':
            tokens.append('^')
            input_str = input_str[1:]
        else:
            bracket_expr = get_bracket_token(input_str)
            tokens.append(bracket_expr)
            input_str = input_str[len(bracket_expr):]

    return tokens


def get_bracket_token(string: str) -> str:
    """Takes a string and returns the first bracket expression.

    >>> get_bracket_token("((1 + 2) + 3) + 4")
    '((1 + 2) + 3)'

    >>> get_bracket_token("1 + (2 + 3)")
    Traceback (most recent call last):
        ...
    ValueError: String "1 + (2 + 3)" doesn't begin with a bracket expression.

    >>> get_bracket_token("((1 + 2) +")
    Traceback (most recent call last):
        ...
    ValueError: String "((1 + 2) +" doesn't begin with a well bracketed expression, missing closing bracket.
    """
    if string[0] != '(':
        raise ValueError(f"String \"{string}\" doesn't begin with a bracket expression.")
    counter = 1
    for j in range(1, len(string)):
        if string[j] == '(':
            counter += 1
        elif string[j] == ')':
            counter -= 1

        if counter == 0:
            return string[:j+1]

    raise ValueError(f"String \"{string}\" doesn't begin with a well bracketed expression, missing closing bracket.")


class BSTNode:
    """A class representing a binary syntax tree node.
    Tree nodes are operations and leaf nodes are numbers (floats).
    """
    def __init__(self, left: Optional['BSTNode'], op: Union[str, float], right: Optional['BSTNode']):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        """The string of a binary syntax tree should be the unambiguous (well bracketed) representation."""
        if self.is_number():
            return f"{self.op}"
        return f"({self.left} {self.op} {self.right})"

    def __repr__(self):
        """Implemented for string serialization."""
        return f"BSTNode({repr(self.left)}, {repr(self.op)}, {repr(self.right)})"

    def is_number(self):
        return type(self.op) == float


def parse(string: str) -> 'BSTNode':
    """Take a string and return a binary syntax tree representing that expression.

    The parsing strategy is in two parts:
    1. Create top level tokens (operators, numbers, bracket expressions)
    2. Fold these into a tree starting with the leftmost, lowest precedence operator

    When a bracket expression is hit the interior is evaluated.

    >>> str(parse("1 + 4 - 2 * (3.0 - 2) - 1"))
    '(((1.0 + 4.0) - (2.0 * (3.0 - 2.0))) - 1.0)'
    """
    return parse_tlt_expression(create_toplevel_tokens(string))


def parse_tlt_expression(tokens: List[str]) -> 'BSTNode':
    """Take a list of top level tokens and fold and recursively parse into a tree."""
    if len(tokens) == 0:
        raise ValueError("Expression wasn't valid, empty list attained.")
    if len(tokens) == 1:
        # This has to be a bracket expression or a number.
        if tokens[0][0] == '(' and tokens[0][-1] == ')':
            # Bracketed expressions need to be further parsed
            return parse(tokens[0][1:-1])
        else:
            # Numbers are leaf nodes
            return BSTNode(None, float(tokens[0]), None)

    pos = get_operator(tokens)

    if not pos:
        raise ValueError("Expression wasn't valid, no operators found in subexpression")

    left = parse_tlt_expression(tokens[:pos])
    right = parse_tlt_expression(tokens[pos+1:])

    return BSTNode(left, tokens[pos], right)


def get_operator(tokens: List[str]) -> int:
    """Returns the last, lowest precedence operator"""
    out = None
    current_prec = -1

    for i in range(len(tokens)-1, -1, -1): # Goes backwards to ensure the last entry is found.
        if tokens[i] in PRECEDENCE and (new_prec := PRECEDENCE[tokens[i]]) > current_prec:
            out = i
            current_prec = new_prec

    return out


def evaluate(tree: BSTNode) -> float:
    """Evaluates a Binary Syntax Tree to a number"""
    if tree.is_number():
        return tree.op
    if tree.op == '+':
        return evaluate(tree.left) + evaluate(tree.right)
    if tree.op == '-':
        return evaluate(tree.left) - evaluate(tree.right)
    if tree.op == '*':
        return evaluate(tree.left) * evaluate(tree.right)
    if tree.op == '/':
        return evaluate(tree.left) / evaluate(tree.right)
    if tree.op == '^':
        return math.pow(evaluate(tree.left), evaluate(tree.right))


def evaluate_string(string: str) -> float:
    """Evaluates a string to a number

    >>> evaluate_string("1 + 2 + 3")
    6.0
    """
    return evaluate(parse(string))


if __name__ == "__main__":
    while True:
        ins = input()
        tree = parse(ins)
        print(tree)
        print(evaluate(tree))
