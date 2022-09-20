from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Type, Union

from VPP.rigid_body.components.rigid_body import RigidBody
from VPP.rigid_body.components.transform import Transform

if TYPE_CHECKING:
    from VPP.rigid_body.components.component import Component
else:
    Component = None

__all__ = ["Object", "RigidBodyObject"]


class Object:
    def __init__(self, name: str = None, children: List[Object] = None, components: List[Component] = None):
        super().__init__()

        if components is None:
            components = []

        self.transform = Transform()
        self.transform.add_to_object(self)

        initialised_components = defaultdict(list)
        initialised_components[Transform].append(self.transform)

        for component in components:
            component.add_to_object(self)
            initialised_components[type(component)].append(component)

        self.transform = initialised_components[Transform][0]
        self.components = initialised_components

        if children is None:
            children = []
        self.name = name
        for child in children:
            child.transform.parent = self.transform

    def get_component(self, component: Type[Component]) -> Union[Component, None]:
        return next(iter(self.components[component]), None)

    def get_components(self, component: Type[Component]) -> List[Component]:
        return self.components[component]


class RigidBodyObject(Object):
    def __init__(
        self, name: str, children: List[Object] = None, components: List[Component] = None, rigid_body: RigidBody = None
    ):
        """
        An Object that adds a RigidBody component by default and implements a property to access the objects RigidBody
        component
        """
        if components is None:
            components = []
        if rigid_body is None:
            rigid_body = RigidBody()
        self.rigid_body = rigid_body
        self.rigid_body.add_to_object(self)
        components.append(self.rigid_body)
        super().__init__(name, children, components)
