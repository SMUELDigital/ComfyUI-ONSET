"""Unit tests for dependency-free camera calculations."""
import importlib.util
import math
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "ONSET" / "CameraNode.py"
spec = importlib.util.spec_from_file_location("onset_camera_under_test", MODULE_PATH)
camera = importlib.util.module_from_spec(spec)
spec.loader.exec_module(camera)


class TestCameraMetadata(unittest.TestCase):
    def test_field_of_view(self):
        meta = camera.camera_metadata(100, 2.8, "1/125", 50, 36, 24, "1.5:1")
        self.assertAlmostEqual(meta["horizontal_fov_degrees"], math.degrees(2 * math.atan(36 / 100)), places=3)
        self.assertAlmostEqual(meta["vertical_fov_degrees"], math.degrees(2 * math.atan(24 / 100)), places=3)
        self.assertAlmostEqual(meta["full_frame_equivalent_mm"], 50, places=3)
        self.assertAlmostEqual(meta["shutter_seconds"], 0.008)
        self.assertAlmostEqual(meta["aspect_ratio_numeric"], 1.5)

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            camera.camera_metadata(100, 0, "1/125", 50, 36, 24, "1.5:1")
        with self.assertRaises(ValueError):
            camera.camera_metadata(100, 2.8, "abc", 50, 36, 24, "1.5:1")
        with self.assertRaises(ValueError):
            camera.camera_metadata(100, 2.8, "1/0", 50, 36, 24, "1.5:1")

    def test_latent_is_not_mutated(self):
        latent = {"samples": object(), "other": {"x": 1}}
        result, json_text, hfov, vfov = camera.CameraNode().execute(
            100, 2.8, "1/125", 50, 36, 24, "1.5:1", latent)
        self.assertIsNot(result, latent)
        self.assertIs(result["samples"], latent["samples"])
        self.assertNotIn("onset_camera", latent)
        self.assertIn("onset_camera", result)
        self.assertGreater(hfov, vfov)
        self.assertIn("shutter_seconds", json_text)


if __name__ == "__main__":
    unittest.main()
