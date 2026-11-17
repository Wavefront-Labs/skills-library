---
id: computing-software.computer-graphics-engineering.computer-vision.point-cloud-normal-estimation
name: point-cloud-normal-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, reconstruction-3d, normal-estimation, point-cloud, open3d, pca, surface-normals]
level: practitioner
status: gated
description: "Estimate point cloud normals: PCA over kNN/radius neighbourhoods, choosing scale, consistent orientation toward the sensor or by MST, and curvature as a by-product (Open3D/PCL)."
sources: ["https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html", "https://pcl.readthedocs.io/projects/tutorials/en/latest/normal_estimation.html", "https://hhoppe.com/recon.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point cloud normal estimation

## PCA normals
For each point, the normal is the eigenvector of the smallest eigenvalue of the neighbourhood
covariance. Curvature (surface variation) = `l0 / (l0 + l1 + l2)`.

```python
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))
pcd.orient_normals_towards_camera_location(camera_location=np.zeros(3))
# or, without a sensor position:
pcd.orient_normals_consistent_tangent_plane(k=15)
```
PCL: `pcl::NormalEstimationOMP<PointXYZ, Normal>` with `setRadiusSearch(0.03)` and
`setViewPoint(vx, vy, vz)` for orientation (gated: unconfirmed, source is paywalled or blocked). PCL is C++ and was not built here.

## Choosing the neighbourhood
- Radius about 2 to 5 times the average point spacing (`np.mean(pcd.compute_nearest_neighbor_distance())`).
  Measured on a noise-free unit sphere with 20,000 samples (spacing 0.0125) and `max_nn=30`: mean
  angle error 27.8 degrees at 1.5x, 11.0 at 2x, 0.37 at 5x, and 0.33 at 10x and 30x (the same,
  because `max_nn=30` caps the neighbourhood once the radius contains more than 30 points). With real
  sensor noise you want the larger value, and `max_nn` must be raised with the radius.
- Too small: noise dominates; too large: smooths edges and corners. Use hybrid radius + max_nn to
  bound cost.
- Downsample first (`voxel_down_sample`) for uneven densities.

## Orientation
PCA gives a sign-ambiguous direction. Orient toward the sensor (known for scans/RGB-D) when you can;
it is reliable (on the sphere test, `orient_normals_towards_camera_location` with the camera outside
gave 100% of normals facing it; with the camera at the sphere centre every normal pointed inward,
so the location must be the real sensor position). `orient_normals_consistent_tangent_plane(k=15)`
made 99.99% of normals outward on the closed sphere. MST propagation (Hoppe et al.) handles closed objects without a viewpoint but fails
on thin structures and noisy regions; check for flipped patches.

## Organised clouds (from depth images)
Faster and better: cross product of neighbouring pixel differences (PCL
`IntegralImageNormalEstimation` (gated: unconfirmed, source is paywalled or blocked)). Open3D's `estimate_normals` does not use the image layout; it searches neighbours in a KD-tree, so organise the depth yourself with NumPy if you need this.

## Uses
Poisson reconstruction (needs oriented normals), point-to-plane ICP, plane segmentation, feature
descriptors (FPFH).

## Verify
On a synthetic sphere, angle error between estimated and analytic normals, and no flipped normals
(dot with outward direction positive everywhere).
