from unittest import TestCase

import numpy as np

from VPP.rigid_body.object import Object
from VPP.rigid_body.rotation import Rotation
from VPP.rigid_body.transform import Transform
from VPP.rigid_body.vector import Vector3D


class TestReferenceFrame(TestCase):
    def test_adding_transform_positions(self):
        ship = Object("ship")
        wing = Object("wing")
        main_element = Object("main_element")
        leading_element = Object("leading_element")
        trailing_element = Object("trailing_element")
        main_element.transform.parent = wing.transform
        leading_element.transform.parent = main_element.transform
        trailing_element.transform.parent = main_element.transform
        wing.transform.parent = ship.transform
        pass
        # bow_port = Transform("bow_port", local_position=Vector3D([0, -20, 0]))
        # self.assertTrue(np.array_equal(np.array([10, -20, 0]), bow_port.position))

    # def test_adding_transform_rotations(self):
    #     base = Transform("base")
    #     base_90deg = Transform("90deg", parent=base, local_rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True))
    #     base_180deg = Transform(
    #         "180deg", parent=base_90deg, local_rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
    #     )
    #     base_270deg = Transform(
    #         "270deg", parent=base_180deg, local_rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
    #     )
    #     base_360deg = Transform(
    #         "360deg", parent=base_270deg, local_rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
    #     )
    #     self.assertEqual(base.rotation, base_360deg.rotation)
    #     self.assertEqual(Rotation.from_euler("xyz", [0, 0, 270], degrees=True), base_270deg.rotation)
    #
    # def test_get_root(self):
    #     base = Transform("base", None)
    #     bow = Transform("bow", base, local_position=Vector3D([10, 0, 0]))
    #     bow_port = Transform("bow_port", bow, local_position=Vector3D([0, -20, 0]))
    #     self.assertEqual(base, bow_port.root)
    #
    #
