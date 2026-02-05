import re
from constants import Operator

TERMINATOR = "\0"

def eval_expr(expression: str):
    stack = []
    current_number = 0
    previous_operator = Operator.ADD
    index = 0
    
    # format expression, end with dummy terminator to denote end of string
    expression = expression.lower().replace(" ", "").replace("x", "*") + TERMINATOR 

    while index <= len(expression) - 1:
        char = expression[index]

        # handle digits
        if char.isdigit():
            current_number = (current_number * 10) + int(char)
        
        # handle parenthetical sub-expressions
        elif char == '(':
            sl = 0
            depth = 0
            # dig into expression until closing paren is found
            for i, c in enumerate(expression[index:]):
                sl = i
                if c == "(":
                    depth += 1
                elif c == ")" and depth > 0:
                    depth -= 1
                if c == ")" and depth == 0:
                    break
            end_index = index + sl
            # evaluate sub-expression
            se = expression[index+1 : end_index]
            current_number = eval(se)
            # compensate index for dig depth
            index = end_index

        # handle operators
        elif not char.isdigit() or index == len(expression):
            # handle add/subtract out-of-band
            if previous_operator == Operator.ADD:
                stack.append(current_number)
            elif previous_operator == Operator.SUBTRACT:
                stack.append(-current_number)
            # handle multiply/divide in-band to respect order of operations
            elif previous_operator == Operator.MULTIPLY:
                prev_number = stack.pop()
                stack.append(prev_number * current_number)
            elif previous_operator == Operator.DIVIDE:
                prev_number = stack.pop()
                stack.append(prev_number / current_number)

            # reset for next number/operator
            previous_operator = char
            current_number = 0
        
        # continue to next character
        index += 1

    return float(sum(stack))