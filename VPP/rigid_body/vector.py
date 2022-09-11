from __future__ import annotations

import numpy as np

__all__ = ["Vector", "Vector1D", "Vector2D", "Vector3D"]


class Vector(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __eq__(self, other):
        if isinstance(other, Vector):
            return np.all(np.isclose(other, self))
        raise NotImplementedError("Can only compare two vectors.")

    def unit_vector(self):
        return self / np.linalg.norm(self)

    def length(self):
        return np.linalg.norm(self)

    @classmethod
    def cross(cls, vector1: Vector, vector2: Vector):
        return Vector(np.cross(vector1, vector2))


class Vector1D(Vector):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if len(obj) != 1:
            raise ValueError("A 1D vector must have one value")
        return obj

    @property
    def x(self):
        return self[0]


class Vector2D(Vector1D):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if len(obj) != 2:
            raise ValueError("A 2D vector must have two values")
        return obj

    @property
    def y(self):
        return self[1]


class Vector3D(Vector2D):
    """
    The sign convention is:
    +ve x towards bow
    +ve y towards starboard
    +ve z from keel to deck (upwards)
    """

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if len(obj) != 3:
            raise ValueError("A 3D vector must have three values")
        return obj

    @property
    def z(self):
        return self[2]
