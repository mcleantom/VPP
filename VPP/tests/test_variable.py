from unittest import TestCase
from VPP.variable import Variable


class TestVariable(TestCase):

    def test_standard_operations(self):
        import operator
        x = Variable("x", 2)
        y = Variable("y", 1)
        for operation in [operator.add, operator.sub, operator.pow, operator.mod, operator.truediv, operator.floordiv]:
            i = operation(x, y)
            self.assertEqual(operation(x.val, y.val), i)
            self.assertIsInstance(i, Variable)
            j = operation(y, x)
            self.assertEqual(operation(y.val, x.val), j)
            self.assertIsInstance(j, Variable)
