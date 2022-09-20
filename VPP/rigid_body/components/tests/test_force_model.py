from typing import Tuple
from unittest import TestCase

import numpy as np

from VPP.math.vector import Vector3D
from VPP.rigid_body.components.force_model import ForceModelBase
from VPP.rigid_body.object import Object, RigidBodyObject
from VPP.state.state_model import StateModelBase


class TestForceModel(TestCase):
    def test_simple_force_model(self):
        test_vpp_state = StateModelBase(wind_vector=Vector3D([1, 0, 0]), boat_vector=Vector3D([2, 2, 0]))

        class DragEquation(ForceModelBase):
            density_air = 1.2754

            def __init__(self, area: float, force_components: Vector3D, moment_components: Vector3D = None):
                super().__init__()
                if moment_components is None:
                    moment_components = Vector3D([0, 0, 0])
                self.area = area
                self.force_components = force_components
                self.moment_components = moment_components

            def calculate_forces_and_moments(self, vpp_state: StateModelBase) -> Tuple[Vector3D, Vector3D]:
                apparent_wind_vector = self.object.transform.inverse_transform_vector(
                    vpp_state.wind_vector + vpp_state.boat_vector
                )
                non_dim_coefficient = 0.5 * self.density_air * apparent_wind_vector**2 * self.area
                force = non_dim_coefficient * self.force_components
                moment = non_dim_coefficient * self.moment_components
                return force, moment

        wing = RigidBodyObject("wing", components=[DragEquation(1, Vector3D([1, 1, 0]))])

        force_model: ForceModelBase
        for force_model in wing.get_components(DragEquation):
            force_model(test_vpp_state)

        lift_force = 0.5 * 1.2754 * 2**2
        drag_force = 0.5 * 1.2754 * 3**2
        self.assertTrue(np.isclose(Vector3D([drag_force, lift_force, 0]), wing.rigid_body.local_resultant_force).all())
        self.assertTrue(np.isclose(Vector3D([0, 0, 0]), wing.rigid_body.local_resultant_moment).all())
