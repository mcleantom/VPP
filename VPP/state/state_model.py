from dataclasses import dataclass

from VPP.math.vector import Vector3D


@dataclass
class StateModelBase:
    wind_vector: Vector3D  # Wind speed and direction
    boat_vector: Vector3D
