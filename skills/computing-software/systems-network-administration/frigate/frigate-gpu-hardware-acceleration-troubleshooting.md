---
id: computing-software.systems-network-administration.frigate.frigate-gpu-hardware-acceleration-troubleshooting
name: frigate-gpu-hardware-acceleration-troubleshooting
category: computing-software
field: systems-network-administration
product: frigate
tags: [gpu-troubleshooting, render-device, dev-dri, failed-to-download-frame, openvino-no-device, scale-vaapi, software-decoding]
level: advanced
status: docs-checked
description: "Fix Frigate GPU problems including missing render devices, OpenVINO not finding an iGPU and ffmpeg Failed to download frame -5 errors."
sources: ["https://docs.frigate.video/troubleshooting/gpu/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting GPU acceleration in Frigate

Hardware acceleration not used: VAAPI and QSV need the GPU render node passed into the container, usually `/dev/dri/renderD128` (compose `devices:` or `docker run --device /dev/dri/renderD128`). Run `ls /dev/dri` on the host; with an iGPU plus a discrete GPU the nodes `renderD128` and `renderD129` are not guaranteed to be in a fixed order, so pass the correct one or map the whole `/dev/dri` directory. Permissions are usually fine as root, but nested setups such as an unprivileged Proxmox LXC may need the node made accessible on the host.

OpenVINO error "Can't get OPTIMIZATION_CAPABILITIES property as no supported devices found": reported fixes include plugging an HDMI dummy plug into the motherboard and, when mixing an Intel iGPU with an Nvidia GPU, confirming the right device or mapping all of `/dev/dri`.

`Failed to download frame: -5` with `Failed to sync surface` in the `ffmpeg.<camera>.detect` log means ffmpeg crashes on a hardware frame synchronisation failure between ffmpeg and the GPU driver (not a Frigate bug). The docs suggest, in order:
- switch between `preset-vaapi` and the QSV presets (QSV is often steadier on Gen 12 and newer);
- try another VAAPI driver: `LIBVA_DRIVER_NAME=i965` on old Intel, `radeonsi` on AMD;
- use a more reliably decoded codec, as H.265 triggers it more than H.264; assign an H.264 sub stream to `detect`; full-range YUV cameras (some Hikvision) are prone;
- match `detect` width and height to the stream, because a mismatch inserts a `scale_vaapi` filter where failures arise;
- match detect `fps` to the stream rather than dropping most frames (lower the camera's own sub-stream frame rate instead);
- as a last resort set `hwaccel_args: []` for that camera and decode in software, which is cheap for a low-resolution sub stream.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/troubleshooting/gpu (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
