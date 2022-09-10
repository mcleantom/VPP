from __future__ import annotations

from typing import List

from VPP.rigid_body.transform import Transform

__all__ = ["Object"]


class Object:
    def __init__(self, name: str = None, children: List[Object] = None):
        super().__init__()
        self.transform = Transform(self)
        if children is None:
            children = []
        self.name = name
        for child in children:
            child.transform.parent = self.transform
