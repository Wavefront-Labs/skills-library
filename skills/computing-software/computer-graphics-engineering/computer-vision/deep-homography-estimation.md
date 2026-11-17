---
id: computing-software.computer-graphics-engineering.computer-vision.deep-homography-estimation
name: deep-homography-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, alignment-stitching, deep-homography, homography, kornia, unsupervised-learning, image-alignment]
level: advanced
status: verified
description: "Estimate homographies with deep networks: 4-point parameterisation, supervised vs unsupervised photometric training, kornia DLT/warp layers, and when classic features still win."
sources: ["https://arxiv.org/abs/1606.03798", "https://arxiv.org/abs/1709.03966", "https://kornia.readthedocs.io/en/latest/geometry.transform.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep homography estimation

## Parameterisation
Predict the displacement of the 4 patch corners (8 numbers) rather than the 9 matrix entries:
balanced magnitudes and a well-defined loss. Convert with DLT:
```python
import kornia.geometry as KG
src = corners.expand(B, 4, 2)                     # patch corners
H = KG.get_perspective_transform(src, src + pred_offsets.view(B, 4, 2))
warped = KG.warp_perspective(img_a, H, dsize=(h, w))
```
Ran with Kornia 0.8.3 for a batch of 2 (H shape (2, 3, 3), warped (2, 1, 128, 128)); `corners` there is a tensor of shape (4, 2) or (B, 4, 2).

## Training
- **Supervised (DeTone et al. 2016)**: synthesise pairs by perturbing corners of random crops with
  known offsets (DeTone et al. used 128x128 patches with each corner perturbed by up to rho = 32 px); L2 on offsets. Easy, but synthetic pairs lack
  real parallax, lighting change and moving objects.
- **Unsupervised (Nguyen et al. 2018)**: warp A with predicted H and minimise photometric L1 against
  B (Nguyen et al. use an L1 pixel-wise photometric loss); trained on real video/image pairs. Add masks for moving content and content-aware weighting.
- Iterative refinement (multi-scale or recurrent designs) generally improves accuracy over single-shot regression.

## Where it helps
Low texture, strong illumination change, multimodal (IR/visible), heavy noise and blur where
SIFT/ORB find few matches.

## Where classic wins
Well-textured, high-resolution images: SIFT/SuperPoint+LightGlue + RANSAC homography is more
accurate (subpixel) and generalises without training. A hybrid (learned matcher + robust
estimation) is often the best production choice.

## Evaluation
Mean average corner error (MACE) in pixels (the metric DeTone et al. report) on held-out real pairs; compare against SIFT+RANSAC and a
learned matcher on the same data.

## Checked
Kornia 0.8.3, PyTorch 2.14.1 CPU.
- Run: `get_perspective_transform` and `warp_perspective` with a 4-point offset parameterisation.
- Fetched (arXiv PDFs): DeTone et al. (128x128 patches, rho = 32, Mean Average Corner Error), Nguyen et al. (L1 photometric loss); arXiv API titles.
