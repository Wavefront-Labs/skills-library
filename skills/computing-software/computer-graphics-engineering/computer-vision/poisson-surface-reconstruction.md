---
id: computing-software.computer-graphics-engineering.computer-vision.poisson-surface-reconstruction
name: poisson-surface-reconstruction
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, reconstruction-3d, poisson-reconstruction, surface-reconstruction, open3d, point-cloud-normals, meshing]
level: sme
status: gated
description: "Mesh point clouds with screened Poisson reconstruction: normal estimation and orientation, depth choice, density trimming, and alternatives like ball pivoting."
sources: ["https://www.open3d.org/docs/release/tutorial/geometry/surface_reconstruction.html", "https://github.com/mkazhdan/PoissonRecon", "https://hhoppe.com/poissonrecon.pdf", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poisson surface reconstruction

## 1. Normals first
Poisson needs oriented normals; bad orientation is the most common failure.
```python
import open3d as o3d, numpy as np
pcd = o3d.io.read_point_cloud("fused.ply")
pcd = pcd.voxel_down_sample(0.005)
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
if not pcd.has_normals():
    pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.02, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(15)     # or orient_normals_towards_camera_location(cam)
```
MVS/scanner output usually has normals from the sensor direction; keep them.

## 2. Screened Poisson
```python
mesh, dens = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10, scale=1.1, linear_fit=False)
dens = np.asarray(dens)
mesh.remove_vertices_by_mask(dens < np.quantile(dens, 0.02))    # trim low-support blobs
mesh = mesh.filter_smooth_taubin(5)
o3d.io.write_triangle_mesh("mesh.ply", mesh)
```
- `depth` = octree depth: resolution ~ bounding size / 2^depth. 8-9 for objects at preview quality, 10-12 for
  detailed scans; vertex count grew 3.9x to 4.0x per level (10,040, 39,354, 158,562, 631,312 vertices for
  depth 6 to 9 on a torus sampled with 500,000 points) and time about 2.5x to 3.3x. **The octree adapts to
  the samples, so depth stops paying off when the cloud is too sparse for it**: depth 10 gave only 768,409
  vertices on that cloud, and on a 19,419-point cloud depths 7, 8, 9 and 10 all returned about 39,310
  vertices.
- Reference CLI (Kazhdan): `PoissonRecon --in pts.ply --out mesh.ply --depth 10 --density` then
  `SurfaceTrimmer --in mesh.ply --out trimmed.ply --trim 7` (gated: unconfirmed, source is paywalled or blocked); the CLI tools are not installed here, so these were not run.
- Poisson produces a watertight surface; it closes holes by inventing smooth surface where there is no data -
  hence density trimming.

## 3. Alternatives
- Ball pivoting (`create_from_point_cloud_ball_pivoting`): preserves holes, needs uniform density
  (ran with radii r, 2r, 4r from the mean neighbour distance: 38,728 triangles on the 19k-point torus).
  Alpha shapes: `create_from_point_cloud_alpha_shape` exists.
- Alpha shapes: quick for convex-ish shapes.
- TSDF fusion for depth-camera streams.

## Gotchas
- Mixed-scale point clouds (dense close, sparse far): Poisson over-smooths detail or creates bubbles; crop the
  region of interest first.
- Flipped normals create inside-out bubbles; check by colouring by normal direction (negating all
  normals of a torus cloud made 0% of the reconstructed vertex normals point outward, against 100% with
  the right orientation).
- Huge meshes: decimate (quadric) afterwards rather than lowering depth too far.

## Verify
- [ ] Hausdorff/cloud-to-mesh distance (CloudCompare) within scanner noise; no blobs beyond the scanned area.
