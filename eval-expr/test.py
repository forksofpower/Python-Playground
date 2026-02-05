import unittest

from eval import eval_expr
class EvalMathTests(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(eval_expr("2 + 3"), 5.0, "The sum is wrong.")

    def test_subtraction(self):
        msg = "The difference is wrong."
        self.assertEqual(eval_expr("5 - 2"), 3.0, msg)
        self.assertEqual(eval_expr("55 - 5"), 50.0, msg)

    def test_multiplication(self):
        self.assertEqual(eval_expr("3 * 4"), 12.0, "The product is wrong.")

    def test_division(self):
        self.assertEqual(eval_expr("8 / 2"), 4.0, "The quotient is wrong.")
    
    def test_parentheses(self):
        self.assertEqual(eval_expr("(2 + 3) * 4"), 20.0, "Parentheses handling is broken.")

    def test_nested_parentheses(self):
        def nested_msg(d):
            return f"Nested Parentheses: depth = {d}"

        self.assertEqual(eval_expr("(4 * (5 * 5)) + 1"), 101.00, nested_msg(2))
        self.assertEqual(eval_expr("(4 * (5 * (3 + 2))) + 1"), 101.00, nested_msg(3))
        self.assertEqual(eval_expr("(4 * (5 * (3 + 10))) + 1"), 261.00, nested_msg(3))
        self.assertEqual(eval_expr("(((((5 * 5)))))"), 25.00, nested_msg(5))

    def test_complex_expression(self):
        msg = "Complex expression handling is broken"
        self.assertEqual(eval_expr("3 + 5 * (2 - 8)"), -27, msg)
        self.assertEqual(eval_expr("10 / 2 + 3 * (4 - 1)"), 14, msg)
        self.assertEqual(eval_expr("18 / (3 + 3) * 2 - 4"), 2, msg)
        self.assertEqual(eval_expr("((2 * 2) * (5 * 5)) + 1"), 101.00, "Nested child parentheses: depth = 2")


    
    if __name__ == '__main__':
        unittest.main()