---
id: computing-software.systems-network-administration.immich.hardware-transcoding-setup
name: hardware-transcoding-setup
category: computing-software
field: systems-network-administration
product: immich
tags: [nvenc, qsv, vaapi, rkmpp, hwaccel-transcoding, ffmpeg]
level: advanced
status: docs-checked
description: "Enable GPU video transcoding in Immich with hwaccel.transcoding.yml: backends, prerequisites, compose extends, admin setting and config-file keys."
sources:
  - https://docs.immich.app/features/hardware-transcoding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: offload video transcoding to a GPU.

Supported APIs: NVENC (NVIDIA), Quick Sync (Intel), RKMPP (Rockchip) and VAAPI (AMD, NVIDIA, Intel). Only Linux and Windows through WSL2 are supported; WSL2 lacks Quick Sync; Raspberry Pi is not supported. Two-pass mode only works with NVENC. Hardware output is typically larger and lower quality than software output at similar settings. NVIDIA and AMD GPUs do not encode VP9.

Prerequisites: NVENC needs the official NVIDIA driver, plus NVIDIA Container Toolkit on Linux except WSL2. VP9 on QSV needs a 9th gen Intel CPU or newer; older CPUs may require Low-Power mode.

Setup:

1. Download `hwaccel.transcoding.yml` from the latest release into the folder holding `docker-compose.yml`.
2. Under `immich-server`, uncomment `extends` and change `cpu` to `nvenc`, `quicksync`, `rkmpp` or `vaapi` (`vaapi-wsl` for VAAPI on WSL2).
3. Redeploy `immich-server`.
4. In Administration, Video transcoding settings, set the hardware acceleration option and save. On Jasper Lake and Elkhart Lake CPUs set Constant quality mode to `CQP`.
5. Optionally enable hardware decoding for end-to-end acceleration; by default only encoding is accelerated.

Single compose file (Unraid, Portainer): inline the device section instead, for QSV:

```yaml
devices:
  - /dev/dri:/dev/dri
```

With a config file, use `"ffmpeg": {"accel": "qsv", "accelDecode": true}` (`nvenc` for NVIDIA).

You do not need to redo past transcodes; the device is used for jobs that run afterwards.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/hardware-transcoding in full. The service names (`nvenc`, `quicksync`, `rkmpp`, `vaapi`, `vaapi-wsl`) were also read from the `hwaccel.transcoding.yml` release asset.
Added: the `vaapi-wsl` note from the page.
Method: documentation only; no commands were run.
