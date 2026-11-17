---
id: computing-software.computer-graphics-engineering.computer-vision.gaussian-splatting-capture-and-training
name: gaussian-splatting-capture-and-training
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-based-rendering, novel-view-synthesis, gaussian-splatting, 3dgs, nerfstudio, gsplat, splat-compression, densification]
level: advanced
status: draft
description: "Capture and train 3D Gaussian Splatting scenes: capture rules, COLMAP poses, training with gsplat/nerfstudio, densification and floaters, compression."
sources: ["https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/", "https://docs.nerf.studio/nerfology/methods/splat.html", "https://github.com/nerfstudio-project/gsplat", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gaussian splatting: capture and training

**Goal:** photoreal, real-time-renderable captures of real places/objects from photos or
video (Kerbl et al. 2023), with predictable quality.

## 1. Capture
- 100–300 sharp images (or 2–4 fps frames from slow video), fixed exposure/white balance,
  no motion blur, fixed focal length.
- Orbit objects at 2–3 heights; for rooms walk a path facing inward and outward with large
  overlap. Cover every surface you want to view from novel angles — splats don't extrapolate.
- Avoid moving people, reflections and changing light during capture.

## 2. Poses
SfM with COLMAP (or GLOMAP for speed); in nerfstudio:
```sh
ns-process-data images --data ./photos --output-dir ./scene          # runs COLMAP, downscales
ns-train splatfacto --data ./scene                                    # gsplat-based 3DGS
ns-viewer --load-config outputs/.../config.yml
ns-export gaussian-splat --load-config outputs/.../config.yml --output-dir export/
```
Bad poses = blurry, doubled results no training trick can fix; check the sparse model first.

## 3. Training knobs
- Iterations ~30k; densification (clone/split by view-space gradient) between ~500–15k
  iterations with periodic opacity reset — controls splat count and detail.
- Floaters (stray splats near cameras): increase densify gradient threshold, add
  regularisation (opacity/scale), crop the scene bounding box, or mask sky.
- Spherical harmonics degree 3 for view-dependent colour (bigger files); degree 0–1 for
  compact assets.
- Anti-aliased variants (Mip-Splatting) reduce popping when rendered at different scales.

## 4. Delivery
Raw `.ply` is large (~250 bytes/splat; millions of splats → hundreds of MB). Compress:
quantisation/SH pruning (`.splat`, `.ksplat`, SPZ, compressed PLY formats), prune low-opacity
splats. Web viewers: three.js-based (Spark, gaussian-splats-3d), PlayCanvas/SuperSplat
(editing/cleanup), Babylon.js.

## Gotchas
- Splats are not meshes: no clean collision/physics; extract meshes separately (SuGaR, 2DGS)
  if needed.
- Lighting is baked into the capture; relighting is not supported by vanilla 3DGS.
- Sorting cost on web/mobile: splat count is the performance budget (~1–3M desktop, < 1M mobile).

## Verify
- [ ] Held-out test views: PSNR/SSIM/LPIPS reported.
- [ ] Novel camera paths inspected for floaters/holes before publishing.
- [ ] Compressed asset size and viewer frame rate measured on target devices.
