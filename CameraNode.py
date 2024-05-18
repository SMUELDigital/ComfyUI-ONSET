class CameraNode:
    """
    A custom camera node for ComfyUI.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ISO": ("INT", {
                    "default": 100,
                    "min": 100,
                    "max": 12800,
                    "step": 100,
                    "display": "number"
                }),
                "Aperture": ("FLOAT", {
                    "default": 2.8,
                    "min": 1.2,
                    "max": 22.0,
                    "step": 0.1,
                    "round": 0.01,
                    "display": "number"
                }),
                "Shutterspeed": (["1/8000", "1/4000", "1/2000", "1/1000", "1/500", "1/250", "1/125", "1/60", "1/30", "1/15", "1/8", "1/4", "1/2", "1", "2", "4", "8", "15", "30"],),
                "Lens_MM": ("FLOAT", {
                    "default": 50.0,
                    "min": 10.0,
                    "max": 300.0,
                    "step": 1.0,
                    "round": 0.1,
                    "display": "number"
                }),
                "Sensor_Width": ("FLOAT", {
                    "default": 35.70,
                    "min": 10.0,
                    "max": 50.0,
                    "step": 0.1,
                    "round": 0.01,
                    "display": "number"
                }),
                "Sensor_Height": ("FLOAT", {
                    "default": 18.80,
                    "min": 10.0,
                    "max": 50.0,
                    "step": 0.1,
                    "round": 0.01,
                    "display": "number"
                }),
                "Aspect_Ratio": (["1.33:1", "1.37:1", "1.5:1", "1.66:1", "1.78:1", "1.85:1", "2.00:1", "2.35:1", "2.39:1", "2.4:1"],),
                "Empty_Latent": ("LATENT",)
            },
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "execute"
    CATEGORY = "ONSET"

    def execute(self, ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, Empty_Latent):
        print(f"Camera settings:\nISO: {ISO}\nAperture: {Aperture}\nShutterspeed: {Shutterspeed}\nLens MM: {Lens_MM}\nSensor Size: {Sensor_Width} x {Sensor_Height}\nAspect Ratio: {Aspect_Ratio}")
        
        # Modify the latent image based on camera settings (dummy operation)
        modified_latent = Empty_Latent  # Placeholder for actual modification logic

        return (modified_latent,)

    @classmethod
    def IS_CHANGED(s, ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, Empty_Latent):
        return f"{ISO}-{Aperture}-{Shutterspeed}-{Lens_MM}-{Sensor_Width}-{Sensor_Height}-{Aspect_Ratio}-{Empty_Latent}"

NODE_CLASS_MAPPINGS = {
    "CameraNode": CameraNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CameraNode": "Camera Node"
}
