from unittest import TestCase

from VPP.rigid_body.components.rigid_body import RigidBody
from VPP.rigid_body.components.rotation import Rotation
from VPP.rigid_body.object import Object, RigidBodyObject
from VPP.rigid_body.vector import Vector3D


class TestRigidBody(TestCase):
    def test_adding_forces_at_center(self):
        ship = RigidBodyObject("ship")
        ship.transform.local_rotation = Rotation.from_rotvec([0, 0, 90], degrees=True)
        force_forward = Vector3D([1, 0, 0])
        force_up = Vector3D([0, 0, 1])
        ship.rigid_body.add_relative_force(force_forward)
        ship.rigid_body.add_relative_force(force_up)
        self.assertEqual(Vector3D([0, -1, 1]), ship.rigid_body.resultant_force)  # World space
        self.assertEqual(Vector3D([1, 0, 1]), ship.rigid_body.local_resultant_force)  # Local space

        ship.rigid_body.add_force(Vector3D([1, 0, 0]))
        self.assertEqual(Vector3D([1, -1, 1]), ship.rigid_body.resultant_force)  # World space
        self.assertEqual(Vector3D([1, 1, 1]), ship.rigid_body.local_resultant_force)  # Local space

        # The forces were applied before the rotation was changed, so they are still acting in the same global direction
        # However the force that was pointing +ve y now points +ve x
        #     and the force that was pointing +ve x now points -ve y
        ship.transform.local_rotation = Rotation.from_rotvec([0, 0, 0], degrees=True)
        self.assertEqual(Vector3D([1, -1, 1]), ship.rigid_body.resultant_force)
        self.assertEqual(Vector3D([1, -1, 1]), ship.rigid_body.local_resultant_force)
