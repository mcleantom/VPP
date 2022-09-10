from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from VPP.rigid_body.object import Object
else:
    Object = None


class Component:
    def __init__(self, vpp_object: Object):
        """
        Base class for everything attached to an object
        """
        self.object = vpp_object
