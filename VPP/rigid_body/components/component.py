from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from VPP.rigid_body.object import Object
else:
    Object = None


class Component:
    def __init__(self):
        self.object = None

    def add_to_object(self, vpp_object: Object):
        """
        Used by the object class to reference itself when a component is listed in the components parameter of the
        Object initializer.
        """
        self.object = vpp_object
