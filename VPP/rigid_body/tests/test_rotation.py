from unittest import TestCase

from VPP.rigid_body.rotation import Rotation


class TestRotation(TestCase):
    def test_rotations(self):
        N = Rotation.from_euler("xyz", [0, 0, 0], degrees=True)
        rotate_90deg = Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        E = N * rotate_90deg
        S = E * rotate_90deg
        W = S * rotate_90deg
        self.assertEqual(N, W * rotate_90deg)
