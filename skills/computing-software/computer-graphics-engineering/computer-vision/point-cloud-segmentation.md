---
id: computing-software.computer-graphics-engineering.computer-vision.point-cloud-segmentation
name: point-cloud-segmentation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, reconstruction-3d, point-cloud-segmentation, plane-ransac, dbscan, euclidean-clustering, open3d]
level: practitioner
status: gated
description: "Segment point clouds: RANSAC planes (floors, walls, tables), DBSCAN/Euclidean clustering of objects, region growing on normals, and learned semantic segmentation options."
sources: ["https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html", "https://pcl.readthedocs.io/projects/tutorials/en/latest/cluster_extraction.html", "https://github.com/Pointcept/Pointcept"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point cloud segmentation (plane RANSAC, clustering)

## Tabletop pattern
```python
pcd = pcd.voxel_down_sample(0.005)
plane, inl = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=2000)
objects = pcd.select_by_index(inl, invert=True)
labels = np.array(objects.cluster_dbscan(eps=0.02, min_points=20))
clusters = [objects.select_by_index(np.where(labels == i)[0]) for i in range(labels.max() + 1)]
```
- `distance_threshold` about 2 to 3 times sensor noise at that range. Tested on a synthetic tabletop
  (2 m plane with 2 mm noise, a box, a cylinder, a sphere; 84,392 points after 5 mm voxel
  downsampling, spacing 4.9 mm): the plane came out as normal (0, 0, 1) with 71,631 inliers.
- Multiple planes: repeat RANSAC on the remaining points until the plane has too few inliers; check
  plane normals (floor ~ gravity, walls ~ perpendicular).
- DBSCAN `eps` about 2 to 4 times point spacing; label -1 = noise. On the tabletop `eps=0.02` (4x)
  and `0.05` found the 3 objects (4,945, 4,159, 3,653 points, 4 noise points) while `eps=0.005` (1x
  spacing) returned 0 clusters, everything noise.

## PCL equivalents
`SACSegmentation` with `SACMODEL_PLANE`/`SACMODEL_PERPENDICULAR_PLANE` (axis constraint),
`EuclideanClusterExtraction` (`setClusterTolerance`, `setMinClusterSize`),
`RegionGrowing` (normal angle + curvature thresholds) for smooth surfaces (gated: unconfirmed, source is paywalled or blocked). PCL is C++ and was not built here.

## Region growing
Grow from low-curvature seeds while neighbour normals differ by less than about 5 to 10 degrees:
segments smooth surfaces (curved walls, pipes) that RANSAC planes cannot.

## Learned semantic segmentation
PointNet++, KPConv, MinkowskiNet, Point Transformer V3 (Pointcept) (gated: unconfirmed, source is paywalled or blocked). Needed for categories
(car, vegetation, building) in lidar scans; train on data from the same sensor type and density. Not run here (GPU).

## Gotchas
- Density varies with range: fixed eps over-segments far objects. Range-adaptive thresholds or
  downsampling to uniform density.
- Touching objects merge in Euclidean clustering: split with region growing or by colour.

## Verify
Count clusters vs ground truth on labelled scenes; for planes report inlier RMS and normal angle
vs known orientation.
