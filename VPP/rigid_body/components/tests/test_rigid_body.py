from unittest import TestCase

import numpy as np

from VPP.rigid_body.components.rotation import Rotation
from VPP.rigid_body.object import RigidBodyObject
from VPP.rigid_body.vector import Vector3D


class TestRigidBody(TestCase):
    def test_adding_relative_and_global_forces_at_center(self):
        ship = RigidBodyObject("ship")
        ship.transform.local_rotation = Rotation.from_rotvec([0, 0, 90], degrees=True)
        force_forward = Vector3D([1, 0, 0])
        force_up = Vector3D([0, 0, 1])
        ship.rigid_body.add_relative_force(force_forward)
        ship.rigid_body.add_relative_force(force_up)
        self.assertEqual(Vector3D([0, 1, 1]), ship.rigid_body.resultant_force)  # World space
        self.assertEqual(Vector3D([1, 0, 1]), ship.rigid_body.local_resultant_force)  # Local space

        ship.rigid_body.add_force(Vector3D([1, 0, 0]))
        self.assertEqual(Vector3D([1, 1, 1]), ship.rigid_body.resultant_force)  # World space
        self.assertEqual(Vector3D([1, -1, 1]), ship.rigid_body.local_resultant_force)  # Local space

        # The forces were applied before the rotation was changed, so they are still acting in the same global direction
        # However the force that was pointing +ve y now points +ve x in the local space
        #     and the force that was pointing +ve x now points -ve y in the local space

        # TODO: Define if we should save forces in local or world reference frame.
        # And if a transform happens after a force is applied, what should happen.

        # ship.transform.local_rotation = Rotation.from_rotvec([0, 0, 0], degrees=True)
        # self.assertEqual(Vector3D([1, 1, 1]), ship.rigid_body.resultant_force)
        # self.assertEqual(Vector3D([-1, -1, 1]), ship.rigid_body.local_resultant_force)

    def test_moments(self):
        ship = RigidBodyObject("ship")
        ship.transform.local_position = Vector3D([580, -50, -10])
        ship.transform.local_rotation = Rotation.from_rotvec([0, 0, 90], degrees=True)
        force_position = Vector3D([9, 12, 8])
        force_vector = Vector3D([-14, 7, -3])
        expected_global = Vector3D([85, -92, 231])
        expected_local = Vector3D([-92, -85, 231])
        ship.rigid_body.add_relative_force(force_vector, force_position)
        self.assertEqual(expected_local, ship.rigid_body.local_resultant_moment)
        self.assertEqual(expected_global, ship.rigid_body.resultant_moment)

    def test_moments_2(self):
        ship = RigidBodyObject("ship")
        ship.rigid_body.add_force(Vector3D([0, 0, 1]), Vector3D([0, 0, 10]))
        self.assertTrue(np.isclose(Vector3D([0, 0, 0]), ship.rigid_body.resultant_moment).all())

        ship.rigid_body.add_force(Vector3D([1, 0, 0]), Vector3D([0, 10, 10]))
        self.assertTrue(np.isclose(Vector3D([0, 10, -10]), ship.rigid_body.resultant_moment).all())
