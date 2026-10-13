"""Opt-in photographic prompt hints derived from ONSET camera JSON.

Text hints do not guarantee that a model will follow camera physics.
"""
import json
import math


def parse_camera_json(camera_json):
    try:
        data = json.loads(camera_json)
    except (TypeError, ValueError) as exc:
        raise ValueError("Expected valid camera JSON from ONSET Camera Metadata.") from exc
    if not isinstance(data, dict):
        raise ValueError("Camera JSON must be an object.")
    required = ("focal_length_mm", "aperture_f", "iso", "shutter_seconds")
    try:
        fields = {k: float(data[k]) for k in required}
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Camera JSON is missing numeric camera parameters.") from exc
    if not all(math.isfinite(v) and v > 0 for v in fields.values()):
        raise ValueError("Camera parameters must be finite, positive numbers.")
    if fields["focal_length_mm"] > 10000 or fields["aperture_f"] > 1000:
        raise ValueError("Camera parameters exceed supported descriptive limits.")
    return fields


def build_camera_prompt(camera_json, detail="balanced"):
    data = parse_camera_json(camera_json)
    focal = data["focal_length_mm"]
    aperture = data["aperture_f"]
    iso = data["iso"]
    shutter = data["shutter_seconds"]
    lens = ("ultra-wide-angle" if focal < 20 else
            "wide-angle" if focal < 35 else
            "normal perspective" if focal < 70 else
            "telephoto" if focal < 200 else "super-telephoto")
    depth = ("shallow depth of field, soft background bokeh" if aperture <= 2.8
             else "moderate depth of field" if aperture <= 8
             else "deep depth of field")
    parts = [f"photographed with a {focal:g}mm lens", lens,
             f"f/{aperture:g}", depth]
    if detail == "detailed":
        parts += [f"ISO {iso:g}", f"{shutter:g}-second exposure"]
        if shutter >= 1 / 15:
            parts.append("potential motion blur for moving subjects")
        if iso >= 3200:
            parts.append("possible high-ISO grain")
    elif detail != "balanced":
        raise ValueError("detail must be 'balanced' or 'detailed'")
    return ", ".join(parts)


class CameraPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "camera_json": ("STRING", {"forceInput": True}),
            "base_prompt": ("STRING", {"default": "", "multiline": True}),
            "detail": (["balanced", "detailed"],),
        }}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("combined_prompt", "camera_hint")
    FUNCTION = "execute"
    CATEGORY = "ONSET/Camera"

    def execute(self, camera_json, base_prompt, detail):
        hint = build_camera_prompt(camera_json, detail)
        combined = ", ".join(value for value in (base_prompt.strip(), hint) if value)
        return (combined, hint)


NODE_CLASS_MAPPINGS = {"ONSETCameraPrompt": CameraPrompt}
NODE_DISPLAY_NAME_MAPPINGS = {"ONSETCameraPrompt": "ONSET Camera Prompt"}
