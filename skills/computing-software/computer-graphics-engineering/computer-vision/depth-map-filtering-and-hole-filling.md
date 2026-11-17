---
id: computing-software.computer-graphics-engineering.computer-vision.depth-map-filtering-and-hole-filling
name: depth-map-filtering-and-hole-filling
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, depth-filtering, hole-filling, flying-pixels, rgbd, edge-aware-filtering]
level: practitioner
status: verified
description: "Clean depth maps from stereo/ToF/RGB-D: invalid-pixel handling, flying pixels, speckle removal, edge-aware and temporal filters, and hole filling that respects edges."
sources: ["https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md", "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://docs.opencv.org/4.x/da/d17/group__ximgproc__filters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth map filtering and hole filling

## 1. Mark invalid explicitly
Zero (or NaN) depth = invalid. Never blur across invalid pixels with a normal filter: zeros pull
neighbours toward the camera (a 3x3 `cv2.blur` on a 2.0 m plane with one zero pixel returned 1.78 m). Keep a validity mask throughout.

## 2. Remove outliers
- **Speckles** (small isolated blobs) in disparity: `cv2.filterSpeckles(disp16, 0, maxSpeckleSize=200, maxDiff=32)`
  (disparity in 1/16 px for SGBM output; tested: a 9-pixel blob was zeroed and a large region kept).
- **Flying pixels** at depth edges (mixed foreground/background): reject pixels whose depth differs
  from neighbours by more than a relative threshold, or whose surface normal is near-perpendicular
  to the viewing ray.
- Range limits: drop depth outside the sensor's valid range.

## 3. Smooth while keeping edges
- Median 5x5 on valid pixels (masked median).
- Edge-aware joint filtering guided by the colour image: `cv2.ximgproc.guidedFilter`,
  `jointBilateralFilter` (the guide must have the same depth as the source: float32 guide for float32
  depth, uint8 for uint8, otherwise an assertion fails), or WLS for disparity (`cv2.ximgproc.createDisparityWLSFilter`).
- Confidence-weighted: filter `depth*w` and `w`, divide.
- Filter in disparity (1/z) space for stereo: noise is roughly constant there.

## 4. Temporal (static camera or ToF)
Exponential moving average per pixel with a reset when change exceeds a threshold (RealSense
temporal filter defaults: alpha 0.4, delta 20, per the librealsense post-processing doc).

## 5. Hole filling
- Small holes: morphological closing on valid depth, or inpainting `cv2.inpaint` on a normalised
  8/16-bit copy (fine for visualisation, not for metric use).
- Occlusion holes beside foreground objects should be filled from the **background** side (farther
  depth): fill with the max depth of the neighbourhood, not the mean.
- Large holes: leave invalid, or use depth completion networks guided by RGB.

## RealSense pipeline order
decimation -> depth-to-disparity -> spatial -> temporal -> disparity-to-depth -> hole filling.

## Verify
Compare to a flat wall/plane ground truth (RMS plane residual) and inspect depth edges in a point
cloud view for flying pixels.
