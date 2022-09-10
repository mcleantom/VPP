from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, List, Type, Union

from VPP.rigid_body.components.rigid_body import RigidBody
from VPP.rigid_body.components.transform import Transform

if TYPE_CHECKING:
    from VPP.rigid_body.components.component import Component
else:
    Component = None

__all__ = ["Object"]


class Object:
    def __init__(self, name: str = None, children: List[Object] = None, components: List[Type[Component]] = None):
        super().__init__()

        if components is None:
            components = []

        initialised_components = defaultdict(list)
        initialised_components[Transform].append(Transform(self))

        for component in components:
            initialised_components[component].append(component(self))

        self.transform = initialised_components[Transform][0]
        self.components = initialised_components

        if children is None:
            children = []
        self.name = name
        for child in children:
            child.transform.parent = self.transform

    def get_component(self, component: Type[Component]) -> Union[Component, None]:
        return next(iter(self.components[component]), None)


class RigidBodyObject(Object):
    def __init__(self, name: str, children: List[Object] = None, components: List[Type[Component]] = None):
        """
        An Object that adds a RigidBody component by default and implements a property to access the objects RigidBody
        component
        """
        if components is None:
            components = []
        components.append(RigidBody)
        super().__init__(name, children, components)
        self.rigid_body = self.get_component(RigidBody)
