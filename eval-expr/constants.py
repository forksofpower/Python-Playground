TERMINATOR = "\0"


# Helper classes for operators & symbols to make sure I don't get my wires crossed
class Bracket:
    OPEN: str
    CLOSE: str

class Parenthesis(Bracket):
    OPEN = '('
    CLOSE = ')'

class Operator:
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'