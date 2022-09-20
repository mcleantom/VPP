from abc import ABC, abstractmethod
from typing import Tuple

from VPP.math.vector import Vector3D
from VPP.rigid_body.components.component import Component
from VPP.rigid_body.object import RigidBodyObject
from VPP.state.state_model import StateModelBase


class ForceModelBase(Component, ABC):
    def __call__(self, vpp_state: StateModelBase):
        force, moment = self.calculate_forces_and_moments(vpp_state)
        self.object.rigid_body.add_relative_force(force)
        self.object.rigid_body.add_relative_moment(moment)

    @abstractmethod
    def calculate_forces_and_moments(self, vpp_state: StateModelBase) -> Tuple[Vector3D, Vector3D]:
        """
        Takes a VPP state in and returns a tuple of Vectors of the forces and moments in the local reference frame, at
        the bodies' origin.
        """
        ...

    def add_to_object(self, vpp_object: RigidBodyObject):
        self.object = vpp_object
