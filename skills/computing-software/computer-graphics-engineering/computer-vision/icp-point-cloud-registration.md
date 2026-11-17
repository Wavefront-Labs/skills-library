---
id: computing-software.computer-graphics-engineering.computer-vision.icp-point-cloud-registration
name: icp-point-cloud-registration
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, 3d-reconstruction, icp, point-to-plane-icp, open3d, fpfh, global-registration, point-cloud, voxel-downsampling, colored-icp]
level: practitioner
status: verified
description: "Register point clouds with Open3D: downsampling and normals, FPFH+RANSAC global initialisation, point-to-plane ICP refinement, thresholds, and evaluating fitness and RMSE."
sources: ["https://szeliski.org/Book/", "https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html", "https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html", "https://www.open3d.org/docs/release/tutorial/pipelines/colored_pointcloud_registration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICP point cloud registration

**Goal:** the rigid transform aligning two scans (lidar, depth sensor, photogrammetry) to
millimetre-level accuracy.

## 1. Preprocess
```python
import open3d as o3d
def prep(pcd, voxel):
    p = pcd.voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 2, max_nn=30))
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 5, max_nn=100))
    return p, fpfh
voxel = 0.02                                   # metres; ~1/100 of object size
src, src_f = prep(source, voxel); tgt, tgt_f = prep(target, voxel)
```
Remove outliers first (`remove_statistical_outlier`), crop to the overlap if known.

## 2. Global initialisation (ICP is local)
```python
reg = o3d.pipelines.registration
init = reg.registration_ransac_based_on_feature_matching(
    src, tgt, src_f, tgt_f, mutual_filter=True, max_correspondence_distance=voxel * 1.5,
    estimation_method=reg.TransformationEstimationPointToPoint(False), ransac_n=3,
    checkers=[reg.CorrespondenceCheckerBasedOnEdgeLength(0.9),
              reg.CorrespondenceCheckerBasedOnDistance(voxel * 1.5)],
    criteria=reg.RANSACConvergenceCriteria(100000, 0.999))
```
Alternatives: FGR (`registration_fgr_based_on_feature_matching`; ran here and reached fitness 0.9995 on
the test shape), or a manual/odometry initial guess. ICP from the identity on the same pair failed
(fitness 0.01), which is why the global step matters.

## 3. Refine with point-to-plane ICP
```python
res = reg.registration_icp(source, target, max_correspondence_distance=voxel * 0.4,
        init=init.transformation, estimation_method=reg.TransformationEstimationPointToPlane(),
        criteria=reg.ICPConvergenceCriteria(max_iteration=50))
print(res.fitness, res.inlier_rmse); T = res.transformation
```
- Point-to-plane converges faster and more accurately than point-to-point on smooth surfaces
  (needs target normals).
- Coarse-to-fine: run ICP at decreasing voxel sizes/thresholds (multi-scale).
- Colored ICP (`registration_colored_icp`, needs target normals and colours; it ran here) for flat
geometry with texture (RGB-D); robust kernels (`TukeyLoss`, also Huber, Cauchy, GM, L1 in the same
module) for outliers.

## 4. Interpreting results
`fitness` = fraction of source points with a correspondence within the threshold (overlap
proxy); `inlier_rmse` = residual. High fitness with low RMSE at a tight threshold = good, but a
perfect alignment of two independent 20k-point samples of the same shape still scored only
fitness 0.47 at `voxel * 0.4` (rotation/translation error 8e-5), so judge fitness against the
sampling density, not against 1.0. `point-to-plane` raises an error if the target has no normals.
`get_information_matrix_from_point_clouds` for pose-graph weighting in multi-scan alignment.

## Gotchas
- Wrong scale (mm vs m) between clouds — ICP can't fix scale; normalise units.
- Symmetric/featureless objects (planes, cylinders) have degenerate alignments; add
  constraints or features.
- Threshold too large → wrong correspondences pull the solution; too small → no convergence.

## Verify
- [ ] Fitness/RMSE logged; visual check of overlap with coloured clouds.
- [ ] Registration error on known-pose test pairs (synthetic transforms) within tolerance.
- [ ] Initialisation success rate measured across the dataset.
