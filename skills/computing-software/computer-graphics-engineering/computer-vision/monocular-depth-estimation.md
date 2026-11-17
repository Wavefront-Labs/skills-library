---
id: computing-software.computer-graphics-engineering.computer-vision.monocular-depth-estimation
name: monocular-depth-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, monocular-depth, depth-anything, midas, metric-depth, relative-depth, scale-alignment]
level: practitioner
status: draft
description: "Use monocular depth networks (Depth Anything, MiDaS, metric models) correctly: relative vs metric outputs, scale/shift alignment to sparse ground truth, temporal stability."
sources: ["https://szeliski.org/Book/", "https://github.com/DepthAnything/Depth-Anything-V2", "https://github.com/isl-org/MiDaS", "https://arxiv.org/abs/1907.01341"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monocular depth estimation

**Goal:** dense depth from a single RGB image for effects (bokeh, relighting, 3D photos),
occlusion in AR, or robotics priors — understanding what the output actually means
(Szeliski 2e §12.8).

## 1. Relative vs metric
- **Relative (affine-invariant)** models (MiDaS, Depth Anything relative): output inverse
  depth / disparity **up to unknown scale and shift**. Ordering and shape are good; absolute
  distances are not.
- **Metric** models (Depth Anything V2 metric indoor/outdoor, ZoeDepth, Metric3D, UniDepth):
  predict metres, but accuracy depends on camera intrinsics and domain (indoor vs outdoor
  checkpoints).

## 2. Run
```python
from transformers import pipeline
depth = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")
out = depth(Image.open("frame.jpg"))["predicted_depth"]     # relative inverse depth (H', W')
d = torch.nn.functional.interpolate(out[None], size=(H, W), mode="bicubic")[0, 0].numpy()
```
Input resolution: models trained at ~518 px — larger inputs give finer detail but may
degrade globally; tile carefully.

## 3. Align to metric using sparse measurements
If you have a few metric depths (lidar points, stereo, ARKit/ARCore depth, known object):
```python
# fit scale s and shift t in inverse-depth space by least squares (or RANSAC/median for robustness)
A = np.stack([pred_invdepth[mask], np.ones(mask.sum())], 1)
s, t = np.linalg.lstsq(A, 1.0 / gt_depth[mask], rcond=None)[0]
metric_depth = 1.0 / np.clip(s * pred_invdepth + t, 1e-6, None)
```
Align in the space the model predicts (inverse depth for MiDaS-style).

## 4. Video / temporal stability
Per-frame predictions flicker in scale. Options: per-frame alignment to tracked sparse depth,
temporal smoothing of s/t, or video depth models (Video Depth Anything, consistent video depth
methods).

## 5. Evaluation
AbsRel = mean(|d − d*| / d*), RMSE, δ < 1.25 accuracy — on in-domain data with ground truth,
after the same alignment you'll use in production.

## Gotchas
- Mirrors, glass, sky, screens and thin structures are systematically wrong.
- Depth edges bleed ("flying pixels") when back-projecting to point clouds — filter by depth
  gradient before 3D use.
- Licences: check model weights licences (some are non-commercial).

## Verify
- [ ] AbsRel/δ1 measured on representative frames with ground truth.
- [ ] Alignment method chosen by robustness test (lstsq vs RANSAC vs median scaling).
- [ ] Video output checked for scale flicker.
