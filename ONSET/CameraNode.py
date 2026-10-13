"""Camera metadata and lens calculations for ComfyUI-ONSET.

Camera parameters are metadata, not physical diffusion-model controls.
"""
import json
import math


def camera_metadata(ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio):
    if min(Aperture, Lens_MM, Sensor_Width, Sensor_Height) <= 0 or ISO <= 0:
        raise ValueError("ISO, aperture, lens and sensor dimensions must be positive.")
    try:
        shutter_seconds = (lambda parts: float(parts[0]) / float(parts[1]))(Shutterspeed.split("/")) if "/" in Shutterspeed else float(Shutterspeed)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("Invalid shutter speed: " + repr(Shutterspeed)) from error
    if shutter_seconds <= 0:
        raise ValueError("Shutter speed must be greater than zero.")
    try:
        aspect = float(Aspect_Ratio.split(":")[0]) / float(Aspect_Ratio.split(":")[1])
    except (ValueError, IndexError, ZeroDivisionError) as error:
        raise ValueError("Invalid aspect ratio: " + repr(Aspect_Ratio)) from error
    horizontal_fov = math.degrees(2.0 * math.atan(Sensor_Width / (2.0 * Lens_MM)))
    vertical_fov = math.degrees(2.0 * math.atan(Sensor_Height / (2.0 * Lens_MM)))
    equivalent_35mm = Lens_MM * math.hypot(36.0, 24.0) / math.hypot(Sensor_Width, Sensor_Height)
    exposure_value_100 = math.log2(Aperture * Aperture / shutter_seconds) - math.log2(ISO / 100.0)
    return {
        "iso": ISO, "aperture_f": Aperture, "shutter": Shutterspeed,
        "shutter_seconds": shutter_seconds, "focal_length_mm": Lens_MM,
        "sensor_width_mm": Sensor_Width, "sensor_height_mm": Sensor_Height,
        "aspect_ratio": Aspect_Ratio, "aspect_ratio_numeric": aspect,
        "horizontal_fov_degrees": round(horizontal_fov, 4),
        "vertical_fov_degrees": round(vertical_fov, 4),
        "full_frame_equivalent_mm": round(equivalent_35mm, 4),
        "ev100": round(exposure_value_100, 4),
    }


class CameraNode:
    """Annotate a latent with camera metadata; do not alter its tensors."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "ISO": ("INT", {"default": 100, "min": 25, "max": 102400, "step": 25}),
            "Aperture": ("FLOAT", {"default": 2.8, "min": 0.7, "max": 64.0, "step": 0.1}),
            "Shutterspeed": (["1/8000", "1/4000", "1/2000", "1/1000", "1/500", "1/250", "1/125", "1/60", "1/30", "1/15", "1/8", "1/4", "1/2", "1", "2", "4", "8", "15", "30"],),
            "Lens_MM": ("FLOAT", {"default": 50.0, "min": 1.0, "max": 2000.0, "step": 1.0}),
            "Sensor_Width": ("FLOAT", {"default": 35.7, "min": 1.0, "max": 100.0, "step": 0.1}),
            "Sensor_Height": ("FLOAT", {"default": 18.8, "min": 1.0, "max": 100.0, "step": 0.1}),
            "Aspect_Ratio": (["1.33:1", "1.37:1", "1.5:1", "1.66:1", "1.78:1", "1.85:1", "2.00:1", "2.35:1", "2.39:1", "2.4:1"],),
            "Empty_Latent": ("LATENT",),
        }}

    RETURN_TYPES = ("LATENT", "STRING", "FLOAT", "FLOAT")
    RETURN_NAMES = ("latent", "camera_json", "horizontal_fov", "vertical_fov")
    FUNCTION = "execute"
    CATEGORY = "ONSET/Camera"

    def execute(self, ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, Empty_Latent):
        metadata = camera_metadata(ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio)
        result = dict(Empty_Latent)
        result["onset_camera"] = metadata
        return (result, json.dumps(metadata, sort_keys=True), metadata["horizontal_fov_degrees"], metadata["vertical_fov_degrees"])


NODE_CLASS_MAPPINGS = {"CameraNode": CameraNode}
NODE_DISPLAY_NAME_MAPPINGS = {"CameraNode": "ONSET Camera Metadata"}
