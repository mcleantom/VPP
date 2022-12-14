from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from anytree import NodeMixin, RenderTree

from VPP.math.vector import Vector, Vector3D
from VPP.rigid_body.components.component import Component
from VPP.rigid_body.components.rotation import Rotation

if TYPE_CHECKING:
    from VPP.rigid_body.object import Object

__all__ = ["Transform"]


class Transform(Component, NodeMixin):
    parent: Transform
    local_transformation: Vector3D
    local_rotation: Rotation

    def __init__(
        self,
        local_rotation: Rotation = Rotation.from_euler("x", [0]),
        local_position: Vector3D = Vector3D([0, 0, 0]),
    ):
        """
        Every object in a VPP has a Transform. It's used to store and manipulate the position and rotation of the object.
        Every transform can have a parent, which allows you to apply position and rotation hierarchically.

        The transform follows a right-hand coordinate system [1]
            +ve x is towards the bow
            +ve y is towards port
            +ve z is upwards (from keel to deck)

        Rotations are defined following the right-hand rule for curve orientation

        [1] https://en.wikipedia.org/wiki/Right-hand_rule#:~:text=Coordinates%20are%20usually%20right%2Dhanded,the%20system%20is%20counter%2Dclockwise.
        """
        super().__init__()
        self.local_position = local_position
        self.local_rotation = local_rotation

    def __repr__(self):
        return f"<Transform {self.object.name} position: {self.position} rotation: {self.rotation}>"

    def hierarchy_tree(self):
        s = []
        for pre, fill, node in RenderTree(self):
            s.append(f"{pre}{node.name}")
        return "\n".join(s)

    @property
    def child_count(self) -> int:
        """
        The number of children the parent transform has.
        """
        return len(self.children)

    @property
    def euler_angles(self) -> Vector:
        """
        The rotation in world space as euler angles in degrees.
        """
        return Vector(self.rotation.as_euler(degrees=True))

    @property
    def local_to_world_matrix(self) -> Vector:
        """
        The matrix that transforms a point from local space into world space
        """
        raise NotImplementedError

    @property
    def position(self) -> Vector3D:
        """
        The world space position of the Transform.
        """
        if not self.is_root:
            return Vector3D(np.add(self.local_position, self.parent.position))
        return self.local_position

    @property
    def rotation(self) -> Rotation:
        """
        The world space rotation of the Transform.
        :return:
        """
        if not self.is_root:
            return self.local_rotation * self.parent.rotation
        return self.local_rotation

    def transform_point(self, position: Vector3D) -> Vector3D:
        """
        Transforms a point from a local coordinates to world coordinates
        """
        return position + self.position

    def transform_vector(self, vector: Vector3D) -> Vector3D:
        """
        Transforms a vector from local space to world space
        """
        return Vector3D(self.rotation.apply(vector).flatten())

    def inverse_transform_point(self, position: Vector3D) -> Vector3D:
        """
        Transforms position from world space to local space.
        """
        return position - self.position

    def inverse_transform_vector(self, vector: Vector3D) -> Vector3D:
        """
        Transforms vector from world space to local space
        """
        return Vector3D(self.rotation.inv().apply(vector).flatten())

    def is_child_of(self, transform: Transform):
        """
        Is this transform a child of parent?
        """
        raise NotImplementedError

    def look_at(self, transform: Transform):
        """
        Rotates the transform so the forward vector points at the targets current position
        """
        raise NotImplementedError

    def rotate(self, rotation: Rotation):
        """
        Use Rotation to rotate the object.
        """
        raise NotImplementedError

    def rotate_around(self, axis: Vector3D, point: Vector3D, angle: float):
        """
        Rotates the transform about axis passing through point in world coordinates by angle degrees.
        """
        raise NotImplementedError

    @property
    def name(self):
        return self.object.name
