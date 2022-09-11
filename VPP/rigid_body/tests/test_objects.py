from unittest import TestCase

from VPP.rigid_body.components.rigid_body import RigidBody
from VPP.rigid_body.object import Object, RigidBodyObject


class TestObjectCreation(TestCase):
    def test_object_hierarchy_in_single_line(self):
        leading_element = Object("leading_element")
        trailing_element = Object("trailing_element")
        ship = Object("ship", [Object("wing", [Object("main_element", [leading_element, trailing_element])])])
        self.assertEqual(ship.transform, leading_element.transform.root)

    def test_rigid_body_object(self):
        ship = RigidBodyObject("ship")
        rigid_body = ship.rigid_body
        self.assertIsInstance(rigid_body, RigidBody)
