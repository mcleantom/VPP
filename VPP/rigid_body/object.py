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

        self.components = initialised_components

        if children is None:
            children = []
        self.name = name
        for child in children:
            child.transform.parent = self.transform

    def get_component(self, component: Type[Component]) -> Union[Component, None]:
        return next(iter(self.components[component]), None)


class RigidBodyObject(Object):
    def __init__(
        self,
        name: str,
        rigid_body: RigidBody = RigidBody(),
        children: List[Object] = None,
        components: List[Type[Component]] = None,
    ):
        """
        An Object that adds a RigidBody component by default and implements a property to access the objects RigidBody
        component
        """
        if components is None:
            components = []
        components.append(rigid_body)
        super().__init__(name, children, components)
        self.rigid_body = rigid_body
