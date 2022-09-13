from typing import TYPE_CHECKING, List, Tuple

import numpy as np

from VPP.rigid_body.vector import Vector3D
from .component import Component

if TYPE_CHECKING:
    from VPP.rigid_body.object import Object
else:
    Object = None


class RigidBody(Component):
    gravity_acceleration_vector: Vector3D = Vector3D([0, 0, 9.81])

    def __init__(self, mass: float = 0):
        """
        Adding a RigidBody component to an object will allow the object to apply forces and moments in the VPP.
        """
        super().__init__()
        self.mass = mass
        self.forces: List[
            Tuple[Vector3D, Vector3D]
        ] = []  # A list of forces and their positions in a local reference frame

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
        position = self.object.transform.inverse_transform_point(position)
        force = self.object.transform.inverse_transform_vector(force)
        self.forces.append((force, position))

    @property
    def resultant_force(self) -> Vector3D:
        """
        The total force vector acting on the body, in the world reference frame.
        """
        return Vector3D(self.object.transform.transform_vector(self.local_resultant_force))

    @property
    def local_resultant_force(self) -> Vector3D:
        """
        The total force vector acting on the body in the local reference frame.
        """
        return Vector3D(sum(x[0] for x in self.forces))

    @property
    def resultant_moment(self) -> Vector3D:
        return Vector3D(self.object.transform.transform_vector(self.local_resultant_moment))

    @property
    def local_resultant_moment(self) -> Vector3D:
        return Vector3D((np.sum([np.cross(r, f) for f, r in self.forces], axis=0)))

    def add_relative_force(self, force: Vector3D, position: Vector3D = None):
        """
        A force in the local reference frame is applied to the RigidBody. If a local-coordinate position vector is
        applied, the force is applied from the position resulting in a torque and force on the RigidBody.
        """
        if position is None:
            position = self.position
        self.forces.append((force, position))

    @property
    def weight(self) -> Vector3D:
        """
        The force of gravity = mass * gravity
        """
        return self.mass * self.gravity_acceleration_vector
