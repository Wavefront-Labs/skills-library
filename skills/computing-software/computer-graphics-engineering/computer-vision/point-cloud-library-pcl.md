---
id: computing-software.computer-graphics-engineering.computer-vision.point-cloud-library-pcl
name: point-cloud-library-pcl
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, reconstruction-3d, pcl, point-cloud-library, point-cloud, cpp, voxel-grid]
level: practitioner
status: draft
description: "Use the Point Cloud Library (PCL) in C++: point types, filters (VoxelGrid, outlier removal), kd-tree search, segmentation, registration and building with CMake."
sources: ["https://pointclouds.org/", "https://pcl.readthedocs.io/projects/tutorials/en/latest/", "https://github.com/PointCloudLibrary/pcl"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point Cloud Library

## Build
```cmake
find_package(PCL 1.12 REQUIRED COMPONENTS common io filters features segmentation registration kdtree)
target_link_libraries(app ${PCL_LIBRARIES})
target_include_directories(app PRIVATE ${PCL_INCLUDE_DIRS})
```
Install via apt (`libpcl-dev`), vcpkg or conda; build times are long from source. Mismatched Eigen
versions or `-march=native` differences between PCL and your app cause alignment crashes: build both
with the same flags.

## Basics
```cpp
pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
pcl::io::loadPCDFile("in.pcd", *cloud);
pcl::VoxelGrid<pcl::PointXYZ> vg; vg.setInputCloud(cloud); vg.setLeafSize(0.01f, 0.01f, 0.01f);
pcl::PointCloud<pcl::PointXYZ>::Ptr down(new pcl::PointCloud<pcl::PointXYZ>); vg.filter(*down);
pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor; sor.setInputCloud(down);
sor.setMeanK(20); sor.setStddevMulThresh(2.0); sor.filter(*down);
```
- Point types: `PointXYZ`, `PointXYZRGB`, `PointXYZI`, `PointNormal`; organised clouds keep
  `width x height`.
- Filters: `PassThrough` (range crop), `CropBox`, `RadiusOutlierRemoval`, `ExtractIndices`.
- Search: `pcl::search::KdTree`, `pcl::octree::OctreePointCloudSearch`.

## Common pipelines
- Segmentation: `SACSegmentation` (plane RANSAC), `EuclideanClusterExtraction`,
  `RegionGrowing`.
- Features: `NormalEstimationOMP`, `FPFHEstimationOMP`.
- Registration: `IterativeClosestPoint`, `GeneralizedIterativeClosestPoint`,
  `NormalDistributionsTransform`, `SampleConsensusPrerejective` for global alignment.

## PCL vs Open3D
PCL: mature C++ API, ROS integration (`pcl_ros`, `pcl_conversions`). Open3D: modern Python and
C++ API, GPU tensor pipeline, visualisation. Python bindings for PCL are poorly maintained; use Open3D
for Python work.

## Gotchas
- Large voxel grids overflow integer indices ("Leaf size is too small"): crop first or increase leaf.
- NaN points in organised clouds: `pcl::removeNaNFromPointCloud`.

## Verify
Visualise with `pcl_viewer in.pcd` and print point counts after each filter.
