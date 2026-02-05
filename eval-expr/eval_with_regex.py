import re
from constants import Operator

TERMINATOR = "\0"

# optional: pre-compile regex
number_pattern = re.compile(r'\d+')

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
            # optional: use pre-compiled regex
            match = number_pattern.search(expression[index:])
            # match = re.search(r'\d+',expression[index:])
            #
            current_number = int(match.group())
            index = index + len(match.group()) - 1
        
        # handle 
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

if __name__ == "__main__":
    print(eval("5 * (2 - 8)"))