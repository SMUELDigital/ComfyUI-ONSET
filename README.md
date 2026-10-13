# ComfyUI-ONSET

Camera metadata and an operational KSampler for [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

> **Important:** ONSET's camera settings are metadata only. They do **not** physically change diffusion output, apply depth of field, simulate ISO noise, motion blur, or change exposure. The sampler does perform actual diffusion sampling.

## Installation

From `ComfyUI/custom_nodes`:

```bash
git clone https://github.com/SMUELDigital/ComfyUI-ONSET.git
```

Restart ComfyUI. Nodes appear under **ONSET/Camera** and **ONSET/Sampling**. No additional pip dependencies are required.

## Nodes

### ONSET Camera Metadata (legacy ID: `CameraNode`)
Inputs: ISO, Aperture (f-number), Shutterspeed, Lens_MM, Sensor_Width, Sensor_Height, Aspect_Ratio, Empty_Latent.

Outputs:
- `latent`: shallow-copy of the input latent mapping with an `onset_camera` metadata dictionary (latent tensors are unchanged)
- `camera_json`: JSON string with camera settings and calculations
- `horizontal_fov`, `vertical_fov`: field of view in degrees

Calculations include shutter duration in seconds, exposure value at ISO 100 (EV100), full-frame-equivalent focal length (by diagonal crop factor), and horizontal/vertical FOV. The aspect-ratio preset is descriptive metadata; it **does not resize** the latent or override the provided sensor dimensions.

### ONSET Camera KSampler (legacy ID: `CameraKSampler`)
Runs the real ComfyUI `nodes.common_ksampler`, using sampler and scheduler options provided by the installed ComfyUI. Adds `onset_camera` metadata to its output latent. Camera inputs **do not alter** sampling behavior.

For an ordinary text-to-image pipeline:

`CheckpointLoader -> CLIP Text Encode -> ONSET Camera KSampler -> VAE Decode -> Save Image`

Also connect an Empty Latent Image to `latent_image`.

**Compatibility:** Node IDs and the original CameraNode latent input are retained so old workflows can resolve them. CameraNode adds output sockets after its original LATENT output. However, custom nodes that discard nonstandard latent fields may drop the camera metadata; use the JSON output if persistence is required.

## Development

Run the Python tests with:

```bash
python -m unittest discover -s tests -v
```

Integration smoke test: install into an existing ComfyUI, restart it, check that both nodes register, then run a KSampler workflow with a small model. The repository tests do not replace that ComfyUI integration test.

## Roadmap

- Add explicit camera-conditioning or post-processing nodes (depth-aware defocus, noise/exposure simulation, motion blur) rather than implying passive metadata changes pixels.
- Add image metadata export and opt-in prompt conditioning.
- Add integration checks against supported ComfyUI releases.

## License

No new license is asserted here; see repository licensing before redistribution.
