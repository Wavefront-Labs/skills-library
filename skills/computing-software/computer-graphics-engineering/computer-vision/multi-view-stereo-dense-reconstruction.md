---
id: computing-software.computer-graphics-engineering.computer-vision.multi-view-stereo-dense-reconstruction
name: multi-view-stereo-dense-reconstruction
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, multi-view-stereo, mvs, colmap-mvs, patchmatch-stereo, depth-map-fusion, openmvs, dense-point-cloud]
level: advanced
status: draft
description: "Produce dense geometry from posed photos with multi-view stereo: COLMAP PatchMatch stereo and fusion, OpenMVS meshing, parameter choices, GPU limits, and quality checks."
sources: ["https://szeliski.org/Book/", "https://colmap.github.io/tutorial.html#dense-reconstruction", "https://github.com/cdcseacave/openMVS/wiki/Usage", "https://demuc.de/papers/schoenberger2016mvs.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-view stereo dense reconstruction

**Goal:** dense point clouds and meshes from an SfM-posed image set (Szeliski 2e §12.7).

## 1. Prerequisite: good SfM
MVS inherits SfM errors. Sparse model with low reprojection error (< ~1 px), most images
registered, correct intrinsics (shared camera model per physical camera).

## 2. COLMAP dense pipeline
```sh
colmap image_undistorter --image_path images --input_path sparse/0 --output_path dense --output_type COLMAP --max_image_size 3200
colmap patch_match_stereo --workspace_path dense --PatchMatchStereo.geom_consistency true
colmap stereo_fusion --workspace_path dense --output_path dense/fused.ply \
    --StereoFusion.min_num_pixels 5 --StereoFusion.max_reproj_error 2
colmap poisson_mesher --input_path dense/fused.ply --output_path dense/meshed-poisson.ply   # or delaunay_mesher
```
- PatchMatch stereo estimates per-image depth+normal maps using neighbouring views
  (Schönberger 2016); `geom_consistency` enforces cross-view consistency — slower, cleaner.
- Fusion merges depth maps into a point cloud; `min_num_pixels` = minimum consistent views
  per point (higher = fewer, cleaner points).
- Requires CUDA for PatchMatch; `max_image_size` controls memory/time.

## 3. OpenMVS alternative
`InterfaceCOLMAP` → `DensifyPointCloud` → `ReconstructMesh` → `RefineMesh` → `TextureMesh`:
strong meshing/texturing pipeline, commonly paired with COLMAP SfM.

## 4. Capture factors that matter more than parameters
- 60–80% overlap, multiple viewing angles per surface point, baseline/depth ratio not tiny.
- Textured surfaces; shiny, transparent and uniform surfaces fail (use cross-polarisation,
  scanning spray, projected texture).
- Sharp images (fast shutter, stopped-down aperture for depth of field), fixed focus/zoom.

## 5. Quality checks
- Inspect depth maps for holes/noise per image (`dense/stereo/depth_maps`).
- Compare against ground truth scans or known dimensions (scale bars / GCPs for metric scale).
- Cloud-to-mesh distance statistics (CloudCompare).

## Gotchas
- Scale is arbitrary without GPS/GCPs/scale bars.
- Huge datasets: split into clusters or reduce image size; PatchMatch time grows with
  neighbours per image.
- Poisson meshing closes holes with blobs — trim by density (`--PoissonMeshing.trim`).

## Verify
- [ ] Dense cloud completeness and noise inspected; known dimensions within tolerance.
- [ ] Parameters and image sizes recorded for reproducibility.
- [ ] Mesh trimmed of hallucinated surfaces.
