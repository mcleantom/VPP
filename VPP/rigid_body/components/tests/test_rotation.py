from unittest import TestCase

from VPP.rigid_body.components.rotation import Rotation
from VPP.rigid_body.vector import Vector3D


class TestRotation(TestCase):
    def test_rotation_chains(self):
        N = Rotation.from_euler("xyz", [0, 0, 0], degrees=True)
        rotate_90deg = Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        E = N * rotate_90deg
        S = E * rotate_90deg
        W = S * rotate_90deg
        self.assertEqual(N, W * rotate_90deg)

    def test_using_rotation_to_modify_vector(self):
        # Trying to work out applying rotations by hand is hard.
        force = Vector3D([1, 0, 0])
        rotate_z_axis = Rotation.from_rotvec([0, 0, 90], degrees=True)
        force_rotated = rotate_z_axis.apply(force)
        self.assertEqual(Vector3D([0, -1, 0]), force_rotated)
        pointing_down = Rotation.from_rotvec([90, 0, 0], degrees=True)
        self.assertEqual(Vector3D([0, 0, 1]), pointing_down.apply(force_rotated))
