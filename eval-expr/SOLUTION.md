# Solution
> [!NOTE]
> This article contains my solutions described in the [interview problem](PROBLEM.md).

## Refactor: operator handling
The first issue I wanted to tackle was having to "look ahead" in the expression to find the second operand if the current character is an operator. This was adding a lot of extra pushing and popping to the stack, required skipping the index ahead somehow, and also would not handle the case where an operand was a parenthetical group.

An alternative method would be to save the current character as `prev_operator` and continue the loop. On the next iteration the current character could be pushed to the stack to be added or subtracted if the `prev_operator` was `-`. I added a `current_number` variable to store the operand so that pushing it to the stack (ie: addition) can happen in the operator handling section where it can be pushed as a negative number if necessary.

```python
    for index, char in enumerate(expression):
        # handle digits
        if char.isdigit():
            match = re.search(r'\d+',expression[index:])
            current_number = int(match.group())
            # this WILL NOT WORK
            index = index + len(match.group()) - 1
        
        # handle parentheses
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
## Refactor: Regex optimization
Even though the interviewer had mentioned this could be solved without regex, I wanted to optimize the solution that I currently had. `re.search` stops after the first match so `r'\d+'` will still only scan over the digit characters (plus the next character which acts as a logical separator). Since this is being run on every iteration with a digit character, python's `re` library has to create the regex parser every iteration. This can easily be optimized by pre-compiling the regex beforehand. 

```python
number_pattern = re.compile(r'\d+')

def eval_expr(expression: str):
    # ...
    while index <= len(expression) - 1:
    # ...
    if char.isdigit():
        match = number_pattern.search(expression[index:])
```
In this case the performance advantages only be noticeable when the input expression is extremely long because the per-iteration overhead is reduced. The regex `r\d+` is *very* simple, so the compilation logic of the parser is minimal.
## Refactor: parentheses handling
The next issue was how I was handling parentheses. Currently, the implementation would break when give `(2 * 2) + (3 * 3)` as it doesn't care about the order of opening and closing parentheses. To fix this I added a `depth` variable to keep track of how many layers of parentheses deep the current iteration is at. When an opening parenthesis is found, `depth` is incremented, when a closing parenthesis is found, `depth` is decremented. If `depth` reaches zero again then the sub expression can be extracted from the expression using the index plus the offset index from the length of the sub-expression.
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
Unfortunately, this moved the worst-case time complexity into `O(n^2^)` territory because expressions such as `((((2 * 2))))` will scan through every character between each set of parentheses. Not ideal but I assumed I could optimize this later on.
## Refactor digit handling
At this point I had figured out how to store state while scanning sub-expressions without looking ahead, and I wanted to do something similar with multi-digit number handling. The `current_number` variable was already there to store the result of the regex, so I needed to find a way to use the variable to store the temporary digits.

For example, `468` needs to somehow go from `4` to `46` to `468` as the loop iter... *oh no...*

I had stumbled upon a wonderful secret in base10 notation: every digit multiplies the previous digit by 10. So multiplying the `current_number` by 10 and adding the next digit essentially *shifts* the full multi-digit number into `current_number`:
```python
current_number = (current_number * 10) + int(char)
```
## Refactor: parentheses handling (again)
Now the only remaining inefficiency that I could identify was the nested loops when handling parentheses. Fixing this would require flipping the recursive pattern upside down. If I were to recurse immediately every time a `(` is encountered, then I can assume that encountering a `)` (having processed the characters before that point) means that the parenthetical group is finished, and it is time to sum the stack and return the value.

To ensure the loop doesn't re-process the next characters we can also return the last index processed in the recursive scope so that the index can be fast-forwarded. Since I don't want my main function to return an index, I can create a recursive handler that manages the `while` loop and stack creation. I wanted to stay away from having to track a sub-expression's index offset as well (adding it to the "current" index at the end), however this would mean passing the *entire expression* to every recursive function call. This would balloon the memory complexity to `O(n*k)` where `k` is the number of groups of parentheses. 

Ideally, I want to keep the memory usage as close to `O(n)` as possible, so it would make the most sense to skip passing the expression recursively altogether.
```python
def eval_expr(expression: str) -> float:
    expression = expression.lower().replace(" ", "").replace("x", "*") + TERMINATOR
    # recursive handler
    def eval_expr_handler(index: int) -> (float, int):
        stack = []
        ...
        while index <= len(expression) - 1:
            char = expression[index]

            # handle digits
            ...
            # handle open paren
            elif char == '(':
                # recurse on rest of expression starting at index + 1
                new_number, new_index = eval_expr_handler(index + 1)
                current_number = new_number
                index = new_index

            # handle operators
            elif not char.isdigit() or index == len(expression):
                ...
                # handle close paren, return immediately
                if char == ')':
                    return float(sum(stack)), index

                # reset for next number/operator
                previous_operator = char
                current_number = 0
            # continue to next character
            index += 1
        return float(sum(stack)), index

    # run the evaluation
    result, _ = eval_expr_handler(0) # start parsing at the first character
    return result
```
By scanning the expression in-place and only passing the starting index to the recursive handler, no extra significant portions of memory will be used by the expression string. The memory complexity is still not quite `O(n)` because of the stacks used in each recursive call, but this can safely be ignored.
## Final Thoughts
Since this is a recursive solution, I was worried that I'd run into stack overflow issues from deeply nested parenthesis groups. I added a check in my tests to see what it could handle.
```python
def test_nested_parentheses(self):
    def nested_msg(d):
        return f"Nested Parentheses: depth = {d}"

    for i in range(1, 1000):
        _open = i * '('
        _close = i * ')'
        try:
            eval_expr(f"{_open}5*5{_close}"), 25.0, nested_msg(i)
        except:  # noqa: E722
            self.assertFalse(True, nested_msg(i))
```
This test raised an exception at *982* levels of recursion, so I don't think this would be problematic with everyday infix expressions.

After all that, this was my complete solution:
```python
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

TERMINATOR = "\0"

def eval_expr(expression: str) -> float:
    expression = expression.lower().replace(" ", "").replace("x", "*") + TERMINATOR

    def sum_stack(s: [int]):
        return float(sum(s))
        
    def eval_expr_handler(index: int) -> (float, int):
        stack = []
        current_number = 0
        previous_operator = Operator.ADD

        while index <= len(expression) - 1:
            char = expression[index]

            if char.isdigit():
                current_number = (current_number * 10) + int(char)

            elif char == Parenthesis.OPEN:
                new_number, new_index = eval_expr_handler(index + 1)
                current_number = new_number
                index = new_index

            elif not char.isdigit() or index == len(expression):
                if previous_operator == Operator.ADD:
                    stack.append(current_number)
                elif previous_operator == Operator.SUBTRACT:
                    stack.append(-current_number)
                elif previous_operator == Operator.MULTIPLY:
                    stack.append(stack.pop() * current_number)
                elif previous_operator == Operator.DIVIDE:
                    stack.append(stack.pop() / current_number)
                if char == Parenthesis.CLOSE:
                    return sum_stack(stack), index

                previous_operator = char
                current_number = 0

            index += 1

        return sum_stack(stack), index

    result, _ = eval_expr_handler(0)
    return result
```
<!-- ## Conclusion
I'm pleased with my current solution as it passes all tests and fulfills all the requirements from the interview, but there are a few changes I'd like to make in the future. By moving removing the nested for loop in the parentheses handling logic I can move the `depth` variable outside the while loop and add a variable to track a sub-expression starting position. When `depth` returns to 0 after landing on a `)` character, the substring could be evaluated, removing the need for a `for` loop nested in a `while` loop. -->