from unittest import TestCase

import numpy as np

from VPP.math.vector import Vector3D
from VPP.rigid_body.components.rotation import Rotation


class TestRotation(TestCase):
    def test_rotation_chains(self):
        N = Rotation.from_euler("xyz", [0, 0, 0], degrees=True)
        rotate_90deg = Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        E = N * rotate_90deg
        S = E * rotate_90deg
        W = S * rotate_90deg
        self.assertTrue(np.isclose(N.as_rotvec(), (W * rotate_90deg).as_rotvec()).all())

    def test_using_rotation_to_modify_vector(self):
        # Trying to work out applying rotations by hand is hard.
        pointing_towards_x_axis = Vector3D([1, 0, 0])
        rotate_z_axis = Rotation.from_rotvec([0, 0, 90], degrees=True)
        pointing_towards_port = rotate_z_axis.apply(pointing_towards_x_axis)
        # Vector pointing +ve x axis now points +ve y axis
        self.assertTrue(np.isclose(Vector3D([0, 1, 0]), pointing_towards_port).all())
        pointing_upwards = Rotation.from_rotvec([90, 0, 0], degrees=True)
        # Vector pointing +ve y axis now points +ve z axis
        self.assertTrue(np.isclose(Vector3D([0, 0, 1]), pointing_upwards.apply(pointing_towards_port)).all())
