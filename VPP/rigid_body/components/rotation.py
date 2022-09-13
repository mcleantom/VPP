import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation


class Rotation(ScipyRotation):
    def __repr__(self):
        rot_vec = np.round(self.as_rotvec(degrees=True)).astype(int)
        if len(rot_vec.shape) > 1:
            rx, ry, rz = rot_vec[0]
        else:
            rx, ry, rz = rot_vec
        return f"<Rotation Rx({rx}°) Ry({ry}°) Rz({rz}°)>"

    def __eq__(self, other):
        if isinstance(other, Rotation):
            return np.array_equal(self.as_rotvec(), other.as_rotvec())
        raise NotImplementedError("Only implemented for comparisons between two rotations.")
