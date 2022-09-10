from unittest import TestCase

from VPP.rigid_body.vector import Vector1D, Vector2D, Vector3D


class TestVectors(TestCase):
    def test_value_errors(self):
        v = Vector1D([1])
        v = Vector2D([1, 2])
        v = Vector3D([1, 2, 3])
        with self.assertRaises(ValueError):
            v = Vector1D([1, 2])
        with self.assertRaises(ValueError):
            v2 = Vector2D([1, 2, 3])
        with self.assertRaises(ValueError):
            v3 = Vector3D([1, 2, 3, 4])
