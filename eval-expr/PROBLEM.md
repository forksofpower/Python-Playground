# Interview Coding Problem: Math Expression Evaluator
> [!NOTE]
> This article describes the interview problem, if you want to skip ahead, view the [solution](SOLUTION.md).

I was recently given the following problem in an interview and asked to solve in pseudocode while walking the interviewers through my thought process.

## Problem
> Write a function called `eval` that takes in a string, `expression`, as input representing a math expression and returns the solution as a `float`. 

You can assume that:
- `expression` will not have any errors
- The only symbols used will be `+ - * / ( )`
- parentheses can be nested

## Initial Thought Process
I've seen problems like this before, and I know that I will need to use a stack to manage the numbers found earlier in the expression, with the most recent number available for immediate use.

In the most basic example `4 * 4` I need to know the last number seen as well as the last symbol. At this point I assume that I'll need to add the operator symbols on to the stack as well.

## Pseudocode
This is not the exact pseudocode from the interview, I've added portions that weren't written down but were assumed. Types have also been added for sanity's sake.
```python
def eval(expression: str) -> float:
    stack = []
    expression = expression.strip_whitespace()

    # split expression at first parentheses character
    left, right = expression.split("(")

    # process left side
    for i, x in left:
        if x is Number:
            # described in interview as "probably should use a regex to get the entire number"
            n = multi_digit_regex(left[i:])
            stack.push(n)
        else:
            # assume is operator, get next number if it exists
            if left[i + 1] is Number:
                l = stack.pop()
                r = left[i + 1]
                
                # do the math
                if x is '+': y = l + r
                elif x is '-': y = l - r
                elif x is '*': y = l * r
                elif x is '/': y = l / r

                # save the result for the next op
                stack.push(y)
    
    # process right side
    # described in interview as "trim the parentheses from either side of the sub expression and evaluate recursively"
    right = right[1: len(left)-1]
    stack.push(eval(right))

    # do something with the stack to get the value
    return process_stack(stack)
```
## Interviewer Hints
At this point the interviewer stopped me to reveal a few hints.
> Assume that you should be able to `sum` the stack to get the return value.

This told me a few things:
- operator symbols should *not* be stored in the stack, otherwise the summing logic would not work
- subtraction should be converted to addition with a negative number
    - ie: `4 - 5` should be treated as `4 + -5`, adding `-5` to the stack to be summed
- order of operations required that multiplication/division happen before any addition/subtraction anyway, so it would need to be done during the parsing process, adding the result to the stack to be summed at the end.

## Updated pseudocode
This gave me enough information to form a plan to deal that actually returned a value and also made the recursive elements make sense. 
```python
def eval(expression: str) -> float:
    # ...
    # process left side
    for i, x in left:
        # ...
        else:
            # assume is operator, get next number if it exists
            if left[i + 1] is Number:
                l = stack.pop()
                r = left[i + 1]
                
                # save the result for the next op
                elif x is '-': stack.push(-r) # add the negative of the next number
                elif x is '*': y = stack.push(l * r)
                elif x is '/': y = stack.push(l / r)
    # ...
    # sum the stack
    return float(sum(stack))
```
## End of Interview
At this point the interviewer stopped the technical portion, affirming they had gotten a good sense of my problem-solving skills. 
However, he did have a few notes:
- I was on the right track with using a stack, although I tripped myself up assuming that symbols needed to be saved on the stack as well
- Using regex would add unnecessary complexity. It is possible to do this without doing a search ahead for multi-digit numbers
- Splitting at the first `(` and truncating the last character before recursive evaluation made too many assumptions and would not work for many cases

### Aftermath
After work I came home and worked on a few solutions that handle most cases, without consulting the internet or an AI overlord.

### [Continue on to the solution](SOLUTION.md)