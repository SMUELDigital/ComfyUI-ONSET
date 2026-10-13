"""Dependency-free tests for the opt-in camera prompt utility."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "ONSET" / "CameraPrompt.py"
spec = importlib.util.spec_from_file_location("onset_prompt_test", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestCameraPrompt(unittest.TestCase):
    SAMPLE = '{"focal_length_mm":85,"aperture_f":1.8,"iso":3200,"shutter_seconds":0.008}'

    def test_balanced(self):
        prompt = module.build_camera_prompt(self.SAMPLE)
        self.assertIn("85mm", prompt)
        self.assertIn("shallow depth of field", prompt)
        self.assertNotIn("ISO 3200", prompt)

    def test_detailed(self):
        prompt = module.build_camera_prompt(self.SAMPLE, "detailed")
        self.assertIn("ISO 3200", prompt)
        self.assertIn("grain", prompt)

    def test_invalid_json_and_values(self):
        for payload in ("{}", "not json", '{"focal_length_mm":0,"aperture_f":2,"iso":100,"shutter_seconds":0.01}'):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                module.build_camera_prompt(payload)

    def test_combined_prompt(self):
        result, hint = module.CameraPrompt().execute(self.SAMPLE, "portrait", "balanced")
        self.assertTrue(result.startswith("portrait, "))
        self.assertIn(hint, result)


if __name__ == "__main__":
    unittest.main()
