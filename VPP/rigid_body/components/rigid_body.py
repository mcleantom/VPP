from typing import TYPE_CHECKING, List, Tuple

import numpy as np

from VPP.rigid_body.vector import Vector, Vector3D
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

    @property
    def resultant_force(self) -> Vector3D:
        """
        The total force vector acting on the body, in the world reference frame.
        """
        return sum(x[0] for x in self.forces)

    @property
    def local_resultant_force(self) -> Vector3D:
        """
        The total force vector acting on the body in the local reference frame.
        """
        return self.object.transform.inverse_transform_vector(self.resultant_force)

    @property
    def resultant_moment(self) -> Vector3D:
        local_frame_forces = [
            (self.object.transform.inverse_transform_vector(f), self.object.transform.inverse_transform_point(r))
            for f, r in self.forces
        ]
        return Vector3D(
            self.object.transform.transform_vector((np.sum([np.cross(r, f) for f, r in local_frame_forces], axis=0)))
        )

    @property
    def local_resultant_moment(self) -> Vector3D:
        return Vector3D(self.object.transform.inverse_transform_vector(self.resultant_moment))

    def add_relative_force(self, force: Vector3D, position: Vector3D = None):
        """
        A force in the local reference frame is applied to the RigidBody. If a local-coordinate position vector is
        applied, the force is applied from the position resulting in a torque and force on the RigidBody.
        """
        if position is None:
            position = self.position
        # Transform the local force vectors to global force vectors
        self.forces.append(
            (self.object.transform.transform_vector(force), self.object.transform.transform_point(position))
        )

    @property
    def weight(self) -> Vector3D:
        """
        The force of gravity = mass * gravity
        """
        return self.mass * self.gravity_acceleration_vector
