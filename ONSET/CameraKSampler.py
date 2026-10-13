"""ComfyUI KSampler with camera metadata pass-through.

Sampling is real; exposure, bokeh and motion blur are NOT simulated.
"""
from .CameraNode import camera_metadata


class CameraKSampler:
    @classmethod
    def INPUT_TYPES(cls):
        import comfy.samplers
        return {"required": {
            "model": ("MODEL",), "positive": ("CONDITIONING",),
            "negative": ("CONDITIONING",), "latent_image": ("LATENT",),
            "ISO": ("INT", {"default": 100, "min": 25, "max": 102400}),
            "Aperture": ("FLOAT", {"default": 2.8, "min": 0.7, "max": 64.0}),
            "Shutterspeed": ("STRING", {"default": "1/125"}),
            "Lens_MM": ("FLOAT", {"default": 50.0, "min": 1.0, "max": 2000.0}),
            "Sensor_Width": ("FLOAT", {"default": 35.7, "min": 1.0, "max": 100.0}),
            "Sensor_Height": ("FLOAT", {"default": 18.8, "min": 1.0, "max": 100.0}),
            "Aspect_Ratio": ("STRING", {"default": "1.78:1"}),
            "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
            "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True}),
            "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
            "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
            "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
        }}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "execute"
    CATEGORY = "ONSET/Sampling"

    def execute(self, model, positive, negative, latent_image, ISO, Aperture, Shutterspeed,
                Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, steps, cfg, seed,
                sampler_name, scheduler, denoise):
        from nodes import common_ksampler
        camera = camera_metadata(ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio)
        sampled = common_ksampler(model, seed, steps, cfg, sampler_name, scheduler,
                                  positive, negative, latent_image, denoise=denoise)
        output = dict(sampled[0])
        output["onset_camera"] = camera
        return (output,)


NODE_CLASS_MAPPINGS = {"CameraKSampler": CameraKSampler}
NODE_DISPLAY_NAME_MAPPINGS = {"CameraKSampler": "ONSET Camera KSampler (Metadata)"}
