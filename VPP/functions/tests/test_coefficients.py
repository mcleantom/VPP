from unittest import TestCase

from VPP.functions import KinematicViscosity, ReynoldsNumber
from VPP.variable import Variable


class TestCoefficients(TestCase):
    def test_reynolds_number(self):
        length = Variable("length", 0.5)
        velocity = Variable("velocity", 20)
        density = Variable("density", 0.146)
        dynamic_viscosity = Variable("μ", 0.0000122)
        kinematic_viscosity = KinematicViscosity(dynamic_viscosity, density)
        reynolds_number = ReynoldsNumber(velocity, length, kinematic_viscosity=kinematic_viscosity)
        self.assertEqual(119672, round(reynolds_number))
