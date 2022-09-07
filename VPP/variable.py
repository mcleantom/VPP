from typing import Union, Callable, Optional
import warnings
import numpy as np
import operator

__all__ = ["Variable"]


class Variable:

    def __init__(
            self,
            name: str,
            initial_guess: float = None,
            scale: Optional[Union[float, Callable]] = None,
            fixed: bool = False,
            lower_bound: Optional[float] = None,
            upper_bound: Optional[float] = None
    ):
        if initial_guess is None:
            initial_guess = lower_bound or 1
            warnings.warn(f"No initial guess was set for variable {name}, defaulting to {initial_guess}")
        self.name = name
        self.initial_guess = initial_guess
        try:
            self.val = self.initial_guess
        except AttributeError:  # Class implements property method for val
            pass
        self.scale = scale
        self.fixed = fixed
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.optimized = False

    def __repr__(self):
        return f"<Variable {self.name} val={self.val} optimized={self.optimized} fixed={self.fixed}>"

    def __add__(self, other):
        return CombinedVariable(self, other, operator.add)

    def __radd__(self, other):
        return CombinedVariable(other, self, operator.add)

    def __mul__(self, other):
        return CombinedVariable(self, other, operator.mul)

    def __rmul__(self, other):
        return CombinedVariable(other, self, operator.mul)

    def __truediv__(self, other):
        return CombinedVariable(self, other, operator.truediv)

    def __rtruediv__(self, other):
        return CombinedVariable(other, self, operator.truediv)

    def __floordiv__(self, other):
        return CombinedVariable(self, other, operator.floordiv)

    def __rfloordiv__(self, other):
        return CombinedVariable(other, self, operator.floordiv)

    def __sub__(self, other):
        return CombinedVariable(self, other, operator.sub)

    def __rsub__(self, other):
        return CombinedVariable(other, self, operator.sub)

    def __pow__(self, power, modulo=None):
        return CombinedVariable(self, power, operator.pow)

    def __rpow__(self, power, modulo=None):
        return CombinedVariable(power, self, operator.pow)

    def __mod__(self, other):
        return CombinedVariable(self, other, operator.mod)

    def __rmod__(self, other):
        return CombinedVariable(other, self, operator.mod)

    def __array__(self, *args, **kwargs):
        return np.array(self.val, *args, **kwargs)

    def __float__(self):
        return float(self.val)

    def __eq__(self, other):
        return self.val == other


class CombinedVariable(Variable):
    operator_mappings = {
        operator.add: "+",
        operator.sub: "-",
        operator.mul: "*",
        operator.truediv: "/",
        operator.floordiv: "//"
    }

    def __init__(self, v1: Variable, v2: Variable, operation: operator):
        super().__init__(
            name=f"({v1.name}{self.operator_mappings.get(operation)}{v2.name})",
            initial_guess=operation(v1.val, v2.val),
            fixed=v1.fixed and v2.fixed,
            lower_bound=operation(v1.lower_bound or float("-inf"), v2.lower_bound or float("-inf")),
            upper_bound=operation(v1.upper_bound or float("inf"), v2.upper_bound or float("inf"))
        )
        self.operation = operation
        self.v1 = v1
        self.v2 = v2

    @property
    def val(self):
        return self.operation(self.v1.val, self.v2.val)
