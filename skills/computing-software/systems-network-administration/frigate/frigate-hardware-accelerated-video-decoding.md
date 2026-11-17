---
id: computing-software.systems-network-administration.frigate.frigate-hardware-accelerated-video-decoding
name: frigate-hardware-accelerated-video-decoding
category: computing-software
field: systems-network-administration
product: frigate
tags: [hwaccel-args, preset-vaapi, intel-quicksync, nvidia-decoding, libva-driver, radeonsi, intel-gpu-stats]
level: advanced
status: docs-checked
description: "Pick the right ffmpeg hwaccel preset for Intel, AMD and Nvidia GPUs in Frigate, set the VA-API driver variable and verify decoding works."
sources: ["https://docs.frigate.video/configuration/hardware_acceleration_video/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hardware accelerated video decoding

Use an integrated or discrete GPU for decoding where possible. Some acceleration is detected automatically; check the logs for a message saying it was detected or a warning that it was not. If you specify acceleration in the config, a clean log means success, because there is no CPU fallback.

Set it globally with `ffmpeg.hwaccel_args` (Settings, Global configuration, FFmpeg) or per camera under Streams (FFmpeg).

Intel presets by CPU generation:
- gen1 to gen5 (driver i965): `preset-vaapi`; QSV is not supported and H.265 may not work.
- gen6 and gen7 (iHD): `preset-vaapi`.
- gen8 to gen12: `preset-vaapi`, or `preset-intel-qsv-h264` / `preset-intel-qsv-h265`.
- gen13 and newer, and Arc A-series or B-series: QSV presets. Arc B-series needs host kernel 6.12 or newer.
The default driver is `iHD`; for older chips add the environment variable `LIBVA_DRIVER_NAME=i965`. VAAPI picks the profile automatically for both H.264 and H.265, while QSV needs the matching H.264 or H.265 preset.

AMD integrated or discrete GPUs use `preset-vaapi` with `LIBVA_DRIVER_NAME=radeonsi`.

Nvidia needs the NVIDIA Container Toolkit. In Compose, add a `deploy.resources.reservations.devices` entry with `driver: nvidia`, `count` (or `device_ids`) and `capabilities: [gpu]`; with `docker run` use `--gpus=all`, and use the `stable-tensorrt` image. Set `hwaccel_args: preset-nvidia`, which selects the profile from the incoming stream and logs an error if the GPU cannot decode it. Verify on the host with `nvidia-smi`, which lists ffmpeg processes; it will not show them from inside the container.

Intel GPU stats are read from the kernel's per-client DRM counters: Broadwell or newer, kernel 5.19+ for i915 (6.5+ on 12th gen and newer) or any xe driver. No `intel_gpu_top`, privileged mode or `CAP_PERFMON` is required; non-root setups may need `CAP_SYS_PTRACE`.

## Checked

2026-11-04. Confirmed against the Video Decoding page: automatic detection and log checks, no CPU fallback, Intel generation table and presets, i965 and LIBVA_DRIVER_NAME, VAAPI profile selection, AMD radeonsi, Nvidia Container Toolkit, Compose deploy section, --gpus=all, stable-tensorrt image, preset-nvidia, nvidia-smi on the host, and Intel GPU stats requirements. Nothing removed.
Method: documentation only; no commands were run.
