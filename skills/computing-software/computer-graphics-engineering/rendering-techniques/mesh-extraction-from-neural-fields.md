---
id: computing-software.computer-graphics-engineering.rendering-techniques.mesh-extraction-from-neural-fields
name: mesh-extraction-from-neural-fields
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, image-based-rendering, neural-surface-reconstruction, marching-cubes, neus, tsdf-fusion, nerf, mesh-extraction]
level: advanced
status: draft
description: "Extract meshes from neural fields: marching cubes on SDF grids, NeuS/Neuralangelo SDF training, TSDF fusion of rendered depth and 2DGS splat-to-mesh."
sources: ["https://lingjie0206.github.io/papers/NeuS/", "https://research.nvidia.com/labs/dir/neuralangelo/", "https://surfsplatting.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mesh extraction from neural fields

## 1. Why it's not trivial
NeRF density fields aren't surfaces: thresholding density gives noisy, floater-filled meshes.
Methods that model a **signed distance function** or surface-aligned primitives extract far
cleaner geometry.

## 2. Options
| Method | Output quality | Notes |
|---|---|---|
| Marching cubes on NeRF density (threshold) | low | quick preview (nerfstudio `ns-export marching-cubes` requires SDF field models; density export via `poisson`/`tsdf`) |
| **TSDF fusion** of rendered depth maps | medium | render depth from many training views, fuse into a TSDF volume (Open3D `ScalableTSDFVolume`), then marching cubes |
| Poisson reconstruction from rendered point clouds + normals | medium | nerfstudio `ns-export poisson` |
| **NeuS / VolSDF / Neuralangelo** (SDF-based neural rendering) | high | train an SDF network with volume rendering; extract zero level set with marching cubes at high res |
| **2D Gaussian Splatting / Gaussian Surfels / SuGaR** | high, fast | surface-aligned splats; TSDF fusion of their depth gives clean meshes in minutes |

## 3. Pipeline example (2DGS)
1. Train 2DGS on posed images.
2. Render depth + normals for all training views.
3. TSDF fuse (voxel size relative to scene scale, truncation ~4 voxels).
4. Marching cubes -> mesh; clean small components; decimate (meshoptimizer/Quadric).
5. Bake colour into texture from the field or images (xatlas UV + projection).

## 4. Quality knobs
- Grid resolution for marching cubes (512^3-2048^3 with sparse/octree approaches).
- Masking background (object-centric capture) avoids extracting the environment.
- Eikonal regularisation (SDF methods) for smooth surfaces; curvature losses (Neuralangelo).

## Gotchas
- Scene scale/normalisation affects voxel size choices; set in metric units when possible.
- Thin structures (wires, leaves) disappear at coarse grids.
- Specular/transparent surfaces produce holes or bumps (view-dependent effects baked into geometry).

## Verify
- [ ] Chamfer distance against a scanned reference (if available) or visual inspection from novel views.
- [ ] Mesh is manifold where required (check with a mesh validator) before downstream use.
