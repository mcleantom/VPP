from typing import TYPE_CHECKING, List, Tuple

from VPP.rigid_body.vector import Vector3D
from .component import Component

if TYPE_CHECKING:
    from VPP.rigid_body.object import Object
else:
    Object = None


class RigidBody(Component):
    gravity_acceleration_vector: Vector3D = Vector3D([0, 0, 9.81])

    def __init__(self, vpp_object: Object):
        """
        Adding a RigidBody component to an object will allow the object to apply forces and moments in the VPP.
        """
        super().__init__(vpp_object)
        self.mass = 0
        self.forces: List[Tuple[Vector3D, Vector3D]] = []

    @property
    def position(self) -> Vector3D:
        return self.object.transform.position

    @property
    def rotation(self) -> Vector3D:
        return self.object.transform.rotation

    def add_force(self, force: Vector3D, position: Vector3D = None):
        """
        A force in world coordinates is applied to the RigidBody. If a world-coordinate position Vector is applied,
        the force is applied from the position resulting in a torque and force on the RigidBody.
        """
        if position is None:
            position = self.position
        self.forces.append((force, position))

    def add_relative_force(self, force: Vector3D, position: Vector3D = None):
        """
        A force in the local reference frame is applied to the RigidBody. If a local-coordinate position vector is
        applied, the force is applied from the position resulting in a torque and force on the RigidBody.
        """

    @property
    def weight(self) -> Vector3D:
        """
        The force of gravity = mass * gravity
        """
