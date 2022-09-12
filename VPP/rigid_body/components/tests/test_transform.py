from unittest import TestCase

import numpy as np

from VPP.rigid_body.components.rotation import Rotation
from VPP.rigid_body.components.transform import Transform
from VPP.rigid_body.object import Object
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

        leading_element.transform.local_position = Vector3D([5, 0, 0])
        trailing_element.transform.local_position = Vector3D([-5, 0, 0])
        main_element.transform.local_position = Vector3D([0, 0, 10])
        wing.transform.local_position = Vector3D([30, -5, 10])

        main_element.transform.local_rotation = Rotation.from_euler("xyz", [0, 0, 45])
        leading_element.transform.local_rotation = Rotation.from_euler("xyz", [0, 0, 10])
        trailing_element.transform.local_rotation = Rotation.from_euler("xyz", [0, 0, -10])

        self.assertTrue(np.array_equal(Vector3D([5 + 30, -5, 20]), leading_element.transform.position))
        self.assertEqual(Rotation.from_euler("xyz", [0, 0, 55]), leading_element.transform.rotation)

    def test_converting_world_to_local_positions(self):
        ship = Object("ship")
        ship.transform.local_position = Vector3D([0, 0, -10])

        # convert world space to local space
        ten_m_above_origin = ship.transform.inverse_transform_point(Vector3D([0, 0, 10]))
        self.assertEqual(Vector3D([0, 0, 20]), ten_m_above_origin)

        # convert local space to world space
        ship_origin_world_space = ship.transform.transform_point(Vector3D([0, 10, 0]))
        self.assertEqual(Vector3D([0, 10, -10]), ship_origin_world_space)

        test_point = Vector3D([102, -93, 4.20493028])
        self.assertEqual(test_point, ship.transform.transform_point(ship.transform.inverse_transform_point(test_point)))
