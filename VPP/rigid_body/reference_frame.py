from __future__ import annotations

import numpy as np

from anytree import NodeMixin, RenderTree

from VPP.rigid_body.rotation import Rotation
from VPP.rigid_body.vector import Vector3D


class ReferenceFrame(NodeMixin):
    parent: ReferenceFrame
    transformation: Vector3D
    rotation: Rotation

    def __init__(
        self, name: str, parent: ReferenceFrame = None, transformation: Vector3D = None, rotation: Rotation = None
    ):
        super().__init__()
        if transformation is None:
            transformation = Vector3D([0, 0, 0])
        if rotation is None:
            rotation = Rotation.from_euler("x", [0])
        self.name = name
        self.parent = parent
        self.transformation = transformation
        self.rotation = rotation

    def __repr__(self):
        s = []
        for pre, fill, node in RenderTree(self):
            s.append(f"{pre}{node.name}")
        return "\n".join(s)

    def global_coordinates(self) -> Vector3D:
        if self.parent:
            return np.add(self.transformation, self.parent.global_coordinates())
        return self.transformation

    def global_rotation(self):
        if self.parent:
            return self.rotation * self.parent.global_rotation()
        return self.rotation
