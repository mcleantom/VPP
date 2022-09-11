import numpy as np
import numpy.typing as npt
from scipy.spatial.transform import Rotation as ScipyRotation

from VPP.rigid_body.vector import Vector

__all__ = ["Rotation"]


class Rotation(ScipyRotation):
    """
    The rotation matrix follows the right hand rule:
        Rx - Rotation about x axis (+ve towards bow), +ve rotation is roll stbd side down
        Ry - Rotation about y axis (+ve towards port), +ve rotation is bow up
        Rz - Rotation about z axis (+ve upwards), +ve rotation is yaw to port
    """

    def __repr__(self):
        rot_vec = np.round(self.as_rotvec(degrees=True)).astype(int)
        if len(rot_vec.shape) > 1:
            rx, ry, rz = rot_vec[0]
        else:
            rx, ry, rz = rot_vec
        return f"<Rotation Rx({rx}°) Ry({ry}°) Rz({rz}°)>"

    def __eq__(self, other):
        if isinstance(other, Rotation):
            return np.allclose(self.as_rotvec(), other.as_rotvec())
        raise NotImplementedError("Only implemented for comparisons between two rotations.")

    def apply(self, vectors: npt.ArrayLike, inverse: bool = ...) -> Vector:
        return Vector(super().apply(vectors, inverse))
