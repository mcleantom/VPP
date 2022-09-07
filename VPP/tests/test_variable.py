from unittest import TestCase

import numpy as np

from VPP.variable import Variable


class TestVariable(TestCase):
    def test_standard_operations(self):
        import operator

        x = Variable("x", 2)
        y = Variable("y", 1)
        for operation in [operator.add, operator.sub, operator.pow, operator.mod, operator.truediv, operator.floordiv]:
            for i, j in [(x, y), (y, x)]:
                k = operation(i, j)
                self.assertEqual(operation(i.val, j.val), k)
                self.assertIsInstance(k, Variable)

    def test_chained(self):
        x = Variable("x", 2)
        y = Variable("y", 1)
        z = Variable("z", 3)

        def f(x_, y_, z_):
            return 2 * x_**3 + 3 * y_**2 - z_

        res1 = f(x.val, y.val, z.val)
        res2 = f(x, y, z)
        self.assertEqual(res1, res2)
        self.assertIsInstance(res2, Variable)
        self.assertEqual("2 * x ** 3 + 3 * y ** 2 - z".replace(" ", ""), str(res2).replace(")", "").replace("(", ""))

    def test_convert_to_numpy(self):
        v = Variable("x", [[0, 2, 3], [4, 5, 6]])
        self.assertTrue(np.array_equal(np.array([[0, 2, 3], [4, 5, 6]]), np.asarray(v)))
        self.assertTrue(np.array_equal(np.array([[0, 2, 3], [4, 5, 6]]), v))

    def test_numpy_ufuncs(self):
        x = Variable("x", [[10, 20, 30], [40, 50, 60]])
        y = Variable("y", [[2, 2, 3], [4, 5, 6]])
        for operation in [np.add, np.subtract, np.power, np.divmod, np.divide, np.floor_divide]:
            for i, j in [(x, y), (y, x)]:
                k = operation(i, j)
                self.assertTrue(np.array_equal(operation(i.val, j.val), k))
                self.assertIsInstance(k, Variable)
