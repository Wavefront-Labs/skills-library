---
id: computing-software.computer-graphics-engineering.rendering-techniques.4d-gaussian-splatting-dynamic-scenes
name: 4d-gaussian-splatting-dynamic-scenes
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, image-based-rendering, 4d-gaussian-splatting, dynamic-scenes, deformation-field, volumetric-video, neural-rendering]
level: sme
status: docs-checked
description: "Represent dynamic scenes with 4D Gaussian splatting: deformation fields over canonical Gaussians, tracked Gaussians and native 4D primitives, and how they differ."
sources: ["https://guanjunwu.github.io/4dgs/", "https://arxiv.org/abs/2310.10642", "https://dynamic3dgaussians.github.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic and 4D Gaussian splatting

## 1. Approaches
| Approach | Idea | Example |
|---|---|---|
| Tracked Gaussians | the same Gaussians persist over time, giving novel-view synthesis plus 3D point tracks including 6-DOF (rotation) tracking | Dynamic 3D Gaussians: Tracking by Persistent Dynamic View Synthesis (Luiten et al.) |
| Canonical + deformation field | 3D Gaussians plus a HexPlane-inspired decomposed neural voxel encoding of (Gaussian centre, time) feeding a lightweight MLP that predicts Gaussian deformations at novel timestamps | 4D-GS (Wu et al.) |
| Native 4D primitives | a collection of 4D Gaussians (anisotropic ellipses that can rotate in space and time) with appearance as 4D spherindrical harmonic coefficients, fitted to the spatio-temporal volume | Real-time Photorealistic Dynamic Scene Representation and Rendering with 4D Gaussian Splatting (Yang et al.) |

Yang et al. argue that learning the 6D plenoptic function directly gives inadequate scene
structure and that explicit deformation modelling does not scale to complex dynamics, which is
why they treat spacetime as one entity. Their model handles variable-length video, trains end to
end, and is evaluated on both monocular and multi-view benchmarks.

## 2. Reported performance (as published, not guaranteed on your hardware)
- Wu et al. 4D-GS: learns a high-resolution real dynamic scene within 30 minutes and renders at
  30+ fps on one RTX 3090; 82 FPS at 800 x 800 on the same GPU in the paper's abstract.

## Gotchas
- Two different papers are both called "4D Gaussian splatting": Wu et al. (deformation field, project
  page guanjunwu.github.io/4dgs) and Yang et al. (native 4D primitives, arXiv 2310.10642). Cite the
  right one.
- Published numbers come from benchmark datasets and a specific GPU; measure on your own footage.

## Verify
- [ ] Which method (deformation field, tracked, native 4D) matches the capture type and playback target.
- [ ] Playback FPS and training time measured on the target device.

## Checked
Method: docs-checked 2026-11-09 against the arXiv 2310.10642 abstract page, the 4D-GS project page (abstract and teaser text) and the Dynamic 3D Gaussians project page (title and 6-DOF tracking sections). Removed unconfirmed capture-rig, COLMAP, storage, baking and flicker claims.
