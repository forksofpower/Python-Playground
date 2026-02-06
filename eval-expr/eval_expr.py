from typing import List, Tuple
from constants import Operator, Parenthesis, TERMINATOR

def eval_expr(expression: str) -> float:
    # format expression, end with dummy terminator to denote end of string
    expression = expression.lower().replace(" ", "").replace("x", "*") + TERMINATOR

    def sum_stack(s: List[int]):
        return float(sum(s))
        
    # recursive handler
    def _eval_expr_handler(index: int) -> Tuple[float, int]:
        stack = []
        current_number = 0
        previous_operator = Operator.ADD

        while index <= len(expression) - 1:
            char = expression[index]

            # handle digits
            if char.isdigit():
                current_number = (current_number * 10) + int(char)
            
            # handle open paren
            elif char == Parenthesis.OPEN:
                # recurse on rest of expression starting at index + 1
                new_number, new_index = _eval_expr_handler(index + 1)
                current_number = new_number
                index = new_index

            # handle operators
            elif not char.isdigit() or index == len(expression):
                # handle add/subtract out-of-band
                if previous_operator == Operator.ADD:
                    stack.append(current_number)
                elif previous_operator == Operator.SUBTRACT:
                    stack.append(-current_number)

                # handle multiply/divide in-band to respect order of operations
                elif previous_operator == Operator.MULTIPLY:
                    stack.append(stack.pop() * current_number)
                elif previous_operator == Operator.DIVIDE:
                    stack.append(stack.pop() / current_number)
                
                # handle close paren, return immediately
                if char == Parenthesis.CLOSE:
                    return sum_stack(stack), index

                # reset for next number/operator
                previous_operator = char
                current_number = 0
            
            # continue to next character
            index += 1
        return sum_stack(stack), index

    # run the evaluation
    result, _ = _eval_expr_handler(0) # start parsing at the first character
    return result