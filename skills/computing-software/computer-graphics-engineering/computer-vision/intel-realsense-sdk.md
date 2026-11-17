---
id: computing-software.computer-graphics-engineering.computer-vision.intel-realsense-sdk
name: intel-realsense-sdk
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, realsense, pyrealsense2, librealsense, rgbd-camera, depth-camera]
level: practitioner
status: draft
description: "Use Intel RealSense cameras with librealsense/pyrealsense2: stream config, depth-to-colour alignment, intrinsics and depth scale, post-processing filters, presets, bags."
sources: ["https://github.com/IntelRealSense/librealsense", "https://dev.intelrealsense.com/docs/python2", "https://dev.intelrealsense.com/docs/post-processing-filters"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intel RealSense SDK

```python
import pyrealsense2 as rs, numpy as np
pipe = rs.pipeline(); cfg = rs.config()
cfg.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
prof = pipe.start(cfg)
scale = prof.get_device().first_depth_sensor().get_depth_scale()     # metres per unit, often 0.001
align = rs.align(rs.stream.color)
frames = align.process(pipe.wait_for_frames())
depth = np.asanyarray(frames.get_depth_frame().get_data()) * scale
color = np.asanyarray(frames.get_color_frame().get_data())
intr = frames.get_color_frame().profile.as_video_stream_profile().intrinsics   # fx, fy, ppx, ppy, coeffs
```

## Key points
- **848x480** is the optimal depth resolution for D4xx (best accuracy per compute); minimum range
  grows with resolution.
- `rs.align(rs.stream.color)` reprojects depth into the colour frame: after alignment use **colour
  intrinsics**. Alternatively align colour to depth.
- `rs.rs2_deproject_pixel_to_point(intr, [u, v], z)` handles the SDK distortion models.
- Visual presets (`rs.option.visual_preset`: High Accuracy, High Density) trade fill rate for
  outliers. The IR emitter (`rs.option.emitter_enabled`) helps on textureless surfaces; disable it
  when multiple cameras interfere, or use inter-camera sync.

## Post-processing (host side)
```python
dec = rs.decimation_filter(); spat = rs.spatial_filter(); temp = rs.temporal_filter()
d2disp = rs.disparity_transform(True); disp2d = rs.disparity_transform(False); hole = rs.hole_filling_filter()
f = dec.process(depth_frame); f = d2disp.process(f); f = spat.process(f); f = temp.process(f); f = disp2d.process(f)
```

## Recording
`cfg.enable_record_to_file("x.bag")`; replay with `cfg.enable_device_from_file("x.bag")`. The
`realsense-viewer` tool records and tunes options interactively.

## Gotchas
- USB 2 connections silently limit modes: check `device.get_info(rs.camera_info.usb_type_descriptor)`.
- Depth error grows quadratically with distance (about 2 percent at 2 m for D435).
- Run on-chip self-calibration in the viewer if plane-fit RMS degrades.

## Verify
Plane-fit RMS on a flat wall at working distance; compare a measured distance against a tape measure.
