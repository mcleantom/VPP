import numbers
import operator
import warnings
from typing import Any, Callable, Optional, Union

import numpy as np

__all__ = ["Variable"]


class Variable:
    def __init__(
        self,
        name: str,
        initial_guess: Any = None,
        scale: Optional[Union[float, Callable]] = None,
        fixed: bool = False,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
    ):
        if initial_guess is None:
            initial_guess = lower_bound or 1
            warnings.warn(f"No initial guess was set for variable {name}, defaulting to {initial_guess}")
        self.name = name
        self.initial_guess = initial_guess
        try:
            self.val = np.asarray(self.initial_guess)
        except AttributeError:  # Class implements property method for val
            pass
        self.scale = scale
        self.fixed = fixed
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.optimized = False

    def __repr__(self):
        return f"<Variable {self.name} val={self.val} optimized={self.optimized} fixed={self.fixed}>"

    def __str__(self):
        return self.name

    def __add__(self, other):
        return CombinedVariable(self, other, operation=operator.add)

    def __radd__(self, other):
        return CombinedVariable(other, self, operation=operator.add)

    def __mul__(self, other):
        return CombinedVariable(self, other, operation=operator.mul)

    def __rmul__(self, other):
        return CombinedVariable(other, self, operation=operator.mul)

    def __truediv__(self, other):
        return CombinedVariable(self, other, operation=operator.truediv)

    def __rtruediv__(self, other):
        return CombinedVariable(other, self, operation=operator.truediv)

    def __floordiv__(self, other):
        return CombinedVariable(self, other, operation=operator.floordiv)

    def __rfloordiv__(self, other):
        return CombinedVariable(other, self, operation=operator.floordiv)

    def __sub__(self, other):
        return CombinedVariable(self, other, operation=operator.sub)

    def __rsub__(self, other):
        return CombinedVariable(other, self, operation=operator.sub)

    def __pow__(self, power, modulo=None):
        return CombinedVariable(self, power, operation=operator.pow)

    def __rpow__(self, power, modulo=None):
        return CombinedVariable(power, self, operation=operator.pow)

    def __mod__(self, other):
        return CombinedVariable(self, other, operation=operator.mod)

    def __rmod__(self, other):
        return CombinedVariable(other, self, operation=operator.mod)

    def __array__(self, *args, **kwargs):
        return np.asarray(self.val, *args, **kwargs)

    def __float__(self):
        return float(self.val)

    def __eq__(self, other):
        return self.val == other

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        def is_array_like(x):
            try:
                np.array(x)
            except Exception:
                return False
            return True

        out = kwargs.get("out", ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not is_array_like(x):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(np.asarray(x) if not isinstance(x, Variable) else x for x in inputs)
        return CombinedVariable(*inputs, operation=ufunc)

    @classmethod
    def convert_to_variable(cls, val):
        if not isinstance(val, Variable):
            return Variable(str(val), val)
        return val


class CombinedVariable(Variable):
    operator_mappings = {
        operator.add: "+",
        operator.sub: "-",
        operator.mul: "*",
        operator.truediv: "/",
        operator.floordiv: "//",
        operator.pow: "**",
    }

    def __init__(self, *inputs, operation: operator):
        self.inputs = tuple(self.convert_to_variable(i) for i in inputs)
        name = self.operator_mappings.get(operation, " " + operation.__name__ + " ").join(str(i) for i in self.inputs)
        name = "(" + name + ")"
        super().__init__(
            name=name,
            initial_guess=operation(*(i.val for i in self.inputs)),
            fixed=False,
            lower_bound=None,
            upper_bound=None,
        )
        self.operation = operation

    @property
    def val(self):
        return self.operation(*(i.val for i in self.inputs))
