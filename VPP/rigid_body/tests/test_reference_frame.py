from unittest import TestCase

import numpy as np

from VPP.rigid_body.reference_frame import ReferenceFrame
from VPP.rigid_body.rotation import Rotation
from VPP.rigid_body.vector import Vector3D


class TestReferenceFrame(TestCase):
    def test_adding_reference_frames_positions(self):
        base = ReferenceFrame("base", None)
        bow = ReferenceFrame("bow", base, transformation=Vector3D([10, 0, 0]))
        bow_port = ReferenceFrame("bow_port", bow, transformation=Vector3D([0, -20, 0]))
        self.assertTrue(np.array_equal(np.array([10, -20, 0]), bow_port.global_coordinates()))

    def test_adding_reference_frames_rotation(self):
        base = ReferenceFrame("base")
        base_90deg = ReferenceFrame("90deg", parent=base, rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True))
        base_180deg = ReferenceFrame(
            "180deg", parent=base_90deg, rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        )
        base_270deg = ReferenceFrame(
            "270deg", parent=base_180deg, rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        )
        base_360deg = ReferenceFrame(
            "360deg", parent=base_270deg, rotation=Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
        )
        self.assertEqual(base.rotation, base_360deg.global_rotation())
