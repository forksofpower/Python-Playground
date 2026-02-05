# Solutions
> [!NOTE]
> This article contains my solutions described in the the [main article](ARTICLE.md).

### Unit Tests

The first step I took when trying to tackle this in Python was to write some tests. This would make debugging side effects or regressions much easier in the future. 

```python
import unittest

from eval import eval_expr

class EvalMathTests(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(eval_expr("2 + 3"), 5.0)

    def test_subtraction(self):
        self.assertEqual(eval_expr("5 - 2"), 3.0)
        self.assertEqual(eval_expr("55 - 5"), 50.0)

    def test_multiplication(self):
        self.assertEqual(eval_expr("3 * 4"), 12.0)

    def test_division(self):
        self.assertEqual(eval_expr("8 / 2"), 4.0)
    
    def test_parentheses(self):
        self.assertEqual(eval_expr("(2 + 3) * 4"), 20.0)

    def test_nested_parentheses(self):
        self.assertEqual(eval_expr("(4 * (5 * 5)) + 1"), 101.00)
        # ...

    def test_complex_expression(self):
        self.assertEqual(eval_expr("3 + 5 * (2 - 8)"), -27, msg)
        # ...

if __name__ == '__main__':
    unittest.main()
```

## Refactor: operator handling
The first issue I wanted to tackle was having to "look ahead" in the expression to find the second operand if the current character is an operator. This was adding a lot of extra pushing and popping to the stack, required skipping the index ahead somehow, and also would not handle the case where an operand was a parenthetical group.

An alternative method would be to save a the current character as `prev_operator` and continue the loop. On the next iteration the current character could be pushed to the stack to be added or subtracted if the `prev_operator` was `-`. I added a `current_number` variable to store the operand so that pushing it to the stack (ie: addition) can happen in the operator handling section where it can be pushed as a negative number if necessary.

```python
    for index, char in enumerate(expression):
        # handle digits
        if char.isdigit():
            match = re.search(r'\d+',expression[index:])
            current_number = int(match.group())
            # this WILL NOT WORK
            index = index + len(match.group()) - 1
        
        # handle parenthetical groups
        # ...

        # handle operators
        elif not char.isdigit() or index == len(expression):
            # handle add/subtract out-of-band
            if previous_operator == '+':
                stack.append(current_number)

            elif previous_operator == '-':
                stack.append(-current_number)

            # handle multiply/divide in-band to respect order of operations
            elif previous_operator == '*':
                stack.append(stack.pop() * current_number)

            elif previous_operator == '/':
                stack.append(stack.pop() / current_number)
```
However, the need to modify the loop index still remains due to the regex in the digit handling logic. I couldn't figure out how to iterate over a number without knowing that it has multiple digits or storing the digits in their own variable. I decided a `while` loop with a modifiable index would allow me to do the search ahead with a regex and I could find an alternative solution later.
```python
index = 0
while index <= len(expression):
    char = expression[index]
    # ...
    if char.isdigit():
        match = re.search(r'\d+',expression[index:])
        current_number = int(match.group())
        index = index + len(match.group()) - 1
```
This resulted in the last character not being processed, so I added a termination character `\0` that acts as a null and denotes the end of the string. This is a character symbol that is not a digit or `(` and can't be mistaken for an operator, causing the operator handling logic to process the `prev_operator` variable.
```python
expression = expression.replace(" ", "") + "\0"
index = 0
while index <= len(expression):
    # ...
    elif not char.isdigit() or index == len(expression):
```

## Refactor: parentheses handling
The next issue was how I was handling parenthetical groups. Currently, the implmentation would break when give `(2 * 2) + (3 * 3)` as it doesn't care about the order of opening and closing parentheses. To fix this I added a `depth` variable to keep track of how many layers of parentheses deep the current iteration is at. When an opening parentheses is found, `depth` is incremented, when a closing parentheses is found, `depth` is decremented. If `depth` reaches zero again then the sub expression can be extracted from the expression using the index plus the offset index from the length of the sub-expression. By skipping ahead and never re-scanning any parts of the expression string we stay in `O(n)` time complexity.
```python
elif char == '(':
    sub_expression_length = 0
    depth = 0
    # dig into expression until closing paren is found
    for i, c in enumerate(expression[index:]):
        sub_expression_length = i
        if c == "(":
            depth += 1
        elif c == ")" and depth > 0:
            depth -= 1
        if c == ")" and depth == 0:
            break
    end_index = index + sub_expression_length
    # evaluate sub-expression
    sub_expression = expression[index + 1 : end_index]
    current_number = eval(se)
    # compensate index for dig depth so we don't re-scan the expression
    index = end_index
```
## Refactor: Regex optimization
Even though the interviewer had mentioned this could be solved without regex, my current solution passed all my tests and seemed to *technically* be in `O(n)` territory. `re.search` stops after the first match so `r'\d+'` will still only scan over the digit characters (plus the next character which acts as a logical seperator). Since this is being run on every iteration with a digit character, python's `re` library has to create the regex parser every iteration. This can easily be optimized by pre-compiling the regex beforehand. 

```python
number_pattern = re.compile(r'\d+')

def eval_expr(expression: str):
    # ...
    while index <= len(expression) - 1:
    # ...
    if char.isdigit():
        match = number_pattern.search(expression[index:])
```
In this case the performance advantages only be noticable when the input expression is extremely long because the per-iteration overhead is reduced. The regex `r\d+` is *very* simple so the compilation logic of the parser is minimal.

## Refactor digit handling
At this point I had figured out how to store state while scanning sub-expressions without looking ahead and I wanted to do something similar with multi-digit number handling. The `current_number` variable was already there to store the result of the regex, so I needed to find a way to use the variable to store the temporary digits.

For example, `468` needs to somehow go from `4` to `46` to `468` as the loop iter... *oh no...*

I had stumbled upon a wonderful secret in base10 notation: every digit multiplies the previous digit by 10. So multiplying the `current_number` by 10 and adding the next digit essentially *shifts* the full multi-digit number into `current_number`:
```python
current_number = (current_number * 10) + int(char)
```
With that change I am left with the following solution:
```python
def eval_expr(expression: str):
    stack = []
    current_number = 0
    previous_operator = '+'
    index = 0
    
    expression = expression.replace(" ", "") + "\0"

    while index <= len(expression) - 1:
        char = expression[index]

        if char.isdigit():
            current_number = (current_number * 10) + int(char)
        
        elif char == '(':
            sl = 0
            depth = 0
            for i, c in enumerate(expression[index:]):
                sl = i
                if c == "(":
                    depth += 1
                elif c == ")" and depth > 0:
                    depth -= 1
                if c == ")" and depth == 0:
                    break
            end_index = index + sl
            se = expression[index+1 : end_index]
            current_number = eval(se)
            index = end_index

        elif not char.isdigit() or index == len(expression):
            if previous_operator == '+':
                stack.append(current_number)
            elif previous_operator == '-':
                stack.append(-current_number)
            elif previous_operator == '*':
                stack.append(stack.pop() * current_number)
            elif previous_operator == '/':
                stack.append(stack.pop() / current_number)

            previous_operator = char
            current_number = 0
        
        index += 1
    return float(sum(stack))
```
```shell
$ python -m unittest
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```


## Conclusion
I'm pleased with my current solution as it passes all tests and fulfills all the requirements from the interview, but there are a few changes I'd like to make in the future. By moving removing the nested for loop in the parentheses handling logic I can move the `depth` variable outside of the while loop and add a variable to track a sub-expression starting position. This is something I can work on later.