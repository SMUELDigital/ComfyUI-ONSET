class CameraKSampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "ISO": ("INT",),
                "Aperture": ("FLOAT",),
                "Shutterspeed": ("STRING",),
                "Lens_MM": ("FLOAT",),
                "Sensor_Width": ("FLOAT",),
                "Sensor_Height": ("FLOAT",),
                "Aspect_Ratio": ("STRING",),
                "steps": ("INT", {"default": 20, "min": 1, "max": 1000}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 20.0}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
                "sampler_name": (["ddim", "plms", "heun", "euler", "euler_ancestral", "dpm_2", "dpm_2_ancestral"],),
                "scheduler": (["normal", "karras", "exponential"],),
                "denoise": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "execute"
    CATEGORY = "ONSET"

    def execute(self, model, positive, negative, latent_image, ISO, Aperture, Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, steps, cfg, seed, sampler_name, scheduler, denoise):
        # Sample the latent image with the provided settings
        print(f"Sampling with settings: ISO={ISO}, Aperture={Aperture}, Shutterspeed={Shutterspeed}, Lens_MM={Lens_MM}, Sensor_Size={Sensor_Width}x{Sensor_Height}, Aspect_Ratio={Aspect_Ratio}")
        # Add logic to utilize the camera settings here

        # Placeholder for actual sampling logic
        sampled_latent = latent_image
        
        return (sampled_latent,)

NODE_CLASS_MAPPINGS = {
    "CameraKSampler": CameraKSampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CameraKSampler": "CameraKSampler"
}
