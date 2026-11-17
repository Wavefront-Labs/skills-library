---
id: computing-software.computer-graphics-engineering.computer-vision.learned-stereo-matching
name: learned-stereo-matching
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, learned-stereo, raft-stereo, stereo-matching, disparity, foundationstereo]
level: advanced
status: draft
description: "Use learned stereo networks (RAFT-Stereo, CREStereo, FoundationStereo): rectified input needs, iterations vs speed, disparity to depth, fine-tuning and comparing against SGBM."
sources: ["https://github.com/princeton-vl/RAFT-Stereo", "https://github.com/megvii-research/CREStereo", "https://github.com/NVlabs/FoundationStereo", "https://vision.middlebury.edu/stereo/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Learned stereo (RAFT-Stereo)

## Inputs
- Pairs must be **rectified** (epipolar lines horizontal): `stereoRectify` +
  `initUndistortRectifyMap` from your calibration. Networks do not fix bad rectification.
- Left image is the reference; disparity is positive for standard left/right order.
- Resolution: most models are trained around 0.5 to 1 MP; pad to multiples of 32 and crop back.

## Running RAFT-Stereo
```bash
python demo.py --restore_ckpt models/raftstereo-middlebury.pth --corr_implementation alt \
  --mixed_precision -l left/*.png -r right/*.png --valid_iters 32
```
- `valid_iters`: more iterations refine detail (16 for speed, 32 for quality). Realtime variants
  use fewer levels and iterations.
- Output disparity in pixels at input resolution; if you downscale input by s, multiply disparity
  by 1/s when mapping back.

## Disparity to depth
`Z = f_px * baseline / d` (f in pixels of the rectified images, baseline in metres). Depth error
grows with Z^2: `dZ = Z^2 / (f B) * dd`.

## Model choice
| Model | Strength |
|---|---|
| RAFT-Stereo / IGEV | Accurate, iterative refinement |
| CREStereo | Robust on real-world, thin structures |
| FoundationStereo / zero-shot models | Strong generalisation without fine-tuning |
| SGBM (classic) | Deterministic, CPU, no generalisation risk, weaker on textureless |

## Domain gap
Synthetic-trained models can fail on reflective, transparent and low-texture surfaces, or unusual
baselines. Fine-tune with self-supervised photometric loss or a small labelled set (laser/LiDAR
depth) when needed.

## Verify
On a scene with known geometry (plane, measured objects), compare depth error vs distance for the
network and SGBM; check left-right consistency to estimate confidence.
