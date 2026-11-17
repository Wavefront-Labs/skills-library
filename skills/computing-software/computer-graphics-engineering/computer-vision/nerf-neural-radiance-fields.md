---
id: computing-software.computer-graphics-engineering.computer-vision.nerf-neural-radiance-fields
name: nerf-neural-radiance-fields
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-based-rendering, nerf, neural-radiance-fields, nerfstudio, instant-ngp, volume-rendering]
level: sme
status: draft
description: "Train and evaluate neural radiance fields: volume rendering basics, nerfstudio/nerfacto and Instant-NGP workflows, unbounded scenes, artefacts, and NeRF vs splatting."
sources: ["https://arxiv.org/abs/2003.08934", "https://docs.nerf.studio/", "https://github.com/NVlabs/instant-ngp", "https://jonbarron.info/zipnerf/", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Neural radiance fields

## 1. Model
A network maps position x (and view direction d) to density sigma and colour c. A pixel is rendered by
marching its ray: `C = sum_i T_i (1 - exp(-sigma_i delta_i)) c_i`, `T_i = exp(-sum_{j<i} sigma_j delta_j)`.
Training minimises photometric error against posed photos. Positional encoding or hash grids (Instant-NGP)
make high-frequency detail learnable quickly.

## 2. Workflow (nerfstudio)
```bash
ns-process-data images --data ./photos --output-dir ./scene      # COLMAP poses, downscaled copies
ns-train nerfacto --data ./scene                                  # viewer URL printed; ~15-30 min on one GPU
ns-eval --load-config outputs/.../config.yml --output-path eval.json
ns-render camera-path --load-config outputs/.../config.yml --camera-path-filename path.json --output-path out.mp4
ns-export poisson --load-config outputs/.../config.yml --output-dir mesh/   # mesh export, quality varies
```
- `nerfacto` handles unbounded scenes (scene contraction), appearance embeddings for exposure changes and
  pose refinement. Zip-NeRF quality is higher but slower.

## 3. Capture and poses
Poses dominate quality: same rules as photogrammetry (overlap, sharp, locked exposure, no moving objects).
Hold out every 8th image for evaluation.

## 4. Artefacts
- Floaters (cloudy blobs near cameras): bad poses or too few views; use distortion/interlevel losses (on in
  nerfacto), more coverage, or crop the scene box.
- Blur in far regions: insufficient coverage or under-sampled proposal network.
- Exposure flicker: enable appearance embeddings; then evaluate with them fixed.

## 5. NeRF vs Gaussian splatting
Splatting renders in real time on consumer GPUs and edits easily; NeRF variants still give smoother geometry
and better view-dependent effects in some scenes and compact models. For interactive delivery, choose splats.

## Gotchas
- Never report metrics on training views; use held-out views (PSNR, SSIM, LPIPS).
- Scene scale/orientation comes from COLMAP; align and scale before measuring anything.

## Verify
- [ ] Held-out PSNR/SSIM/LPIPS recorded; fly-through video free of floaters within the capture volume.
