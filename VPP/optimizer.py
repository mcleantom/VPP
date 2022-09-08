from VPP.condition import Condition
from VPP.variable import Variable


class Optimizer:
    def optimize(self, variable: Variable, subject_to: Condition):
        ...
