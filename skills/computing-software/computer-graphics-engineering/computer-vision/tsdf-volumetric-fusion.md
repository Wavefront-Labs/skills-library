---
id: computing-software.computer-graphics-engineering.computer-vision.tsdf-volumetric-fusion
name: tsdf-volumetric-fusion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, 3d-reconstruction, tsdf-fusion, kinectfusion, scalable-tsdf, voxel-block-grid, marching-cubes, rgbd, open3d]
level: advanced
status: verified
description: "Fuse posed RGB-D frames into a TSDF volume and extract meshes: voxel size and truncation, scalable voxel-block grids, depth filtering, marching cubes, and drift effects."
sources: ["https://szeliski.org/Book/", "https://www.open3d.org/docs/release/tutorial/t_reconstruction_system/integration.html", "https://graphics.stanford.edu/papers/volrange/volrange.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDF volumetric fusion

**Goal:** a watertight-ish, denoised mesh of a room or object from a depth camera (RealSense,
Azure Kinect, iPhone LiDAR) and known poses (Curless & Levoy 1996; KinectFusion).

## 1. Concept
A voxel grid stores a truncated signed distance to the nearest surface and a weight. Each
depth frame updates voxels near the observed surface with a running weighted average —
noise averages out; zero crossing = surface.

## 2. Integrate with Open3D (tensor API, scalable)
```python
import open3d as o3d, open3d.core as o3c
vbg = o3d.t.geometry.VoxelBlockGrid(attr_names=("tsdf", "weight", "color"),
        attr_dtypes=(o3c.float32, o3c.float32, o3c.float32), attr_channels=((1), (1), (3)),
        voxel_size=0.006, block_resolution=16, block_count=50000, device=o3c.Device("CUDA:0"))   # "CPU:0" works too, slower
for depth, color, T_world_cam in frames:
    extr = o3c.Tensor(np.linalg.inv(T_world_cam))             # world->camera
    blocks = vbg.compute_unique_block_coordinates(depth, intrinsic, extr, depth_scale=1000.0, depth_max=3.0)
    vbg.integrate(blocks, depth, color, intrinsic, extr, depth_scale=1000.0, depth_max=3.0)
mesh = vbg.extract_triangle_mesh().to_legacy()               # marching cubes; weight_threshold=3.0
```
Voxel-block hashing only allocates space near surfaces — large scenes fit in memory.
`depth` and `color` must be `o3d.t.geometry.Image`, `intrinsic` and `extr` `o3c.Tensor`s (float64).

Tested on the CPU device (Open3D 0.20.0, code above with `CPU:0`) with a synthetic sphere of radius
0.4 m in front of a wall at 2.5 m: the extracted sphere radius was 0.4001 m (std 1.8 mm) and the
wall z 2.5 m. **`extract_triangle_mesh` returned an empty mesh after 3 integrated frames and a full
mesh after 4**, because the default `weight_threshold=3.0` needs accumulated weight above 3; lower
it (`extract_triangle_mesh(weight_threshold=1.0)`) for short sequences or single-frame tests.

## 3. Parameters
- **voxel_size**: 4–6 mm for objects, 1–2 cm for rooms. Halving it multiplies a dense grid by 8,
  but with voxel-block hashing the allocated block count grew about 3.3x to 3.6x per halving in the
  sphere test (334, 1118, 4017 blocks at 12, 6 and 3 mm), since memory follows surface area.
- **truncation**: the classic `TSDFVolume` takes `sdf_trunc` in metres (~3–5 voxels is common);
  `VoxelBlockGrid.integrate` instead takes `trunc_voxel_multiplier` (default 8.0, truncation =
  multiplier x voxel size). Too small → holes, too large → thin structures merge and surfaces
  thicken.
- `depth_max`: discard far, noisy depth (consumer sensors degrade quadratically with range).
- Pre-filter depth: bilateral filter, remove flying pixels at depth discontinuities.

## 4. Poses
TSDF fusion assumes accurate poses: from tracking (frame-to-model ICP as in KinectFusion,
VIO, or SLAM with loop closure). Drift shows as doubled surfaces; after loop closure,
re-integrate with optimised poses (or use deformable/submap approaches).

## Gotchas
- Depth scale mismatch (mm vs m) → empty or exploded volume.
- Dynamic objects leave ghost geometry; mask people/moving objects.
- Black/shiny/transparent surfaces return no depth → holes; can't be fixed by fusion.

## Verify
- [ ] Known-dimension object measured on the mesh within tolerance.
- [ ] No doubled walls after a loop (poses consistent).
- [ ] Memory/time per frame logged for the chosen voxel size.
