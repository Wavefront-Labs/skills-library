---
id: computing-software.computer-graphics-engineering.computer-vision.depth-to-point-cloud-conversion
name: depth-to-point-cloud-conversion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, depth-to-point-cloud, back-projection, open3d, rgbd, point-cloud]
level: practitioner
status: verified
description: "Back-project depth images to 3D point clouds: intrinsics, depth scale, z-depth vs range, aligned RGB, Open3D create_from_rgbd_image, organised clouds, world frame."
sources: ["https://www.open3d.org/docs/release/tutorial/geometry/rgbd_image.html", "https://www.open3d.org/docs/release/python_api/open3d.geometry.PointCloud.html", "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth to point cloud conversion

## Back-projection
```python
def depth_to_points(depth_m, K):
    h, w = depth_m.shape
    u, v = np.meshgrid(np.arange(w), np.arange(h))
    z = depth_m
    x = (u - K[0, 2]) * z / K[0, 0]
    y = (v - K[1, 2]) * z / K[1, 1]
    pts = np.stack([x, y, z], -1).reshape(-1, 3)
    return pts[z.reshape(-1) > 0]
```
- **Depth scale**: 16-bit PNG depth is usually millimetres (`/1000`); TUM uses 5000 per metre (the factor in Open3D's `CreateFromTUMFormat`);
  RealSense reports `depth_scale` from the device (often 0.001). Wrong scale = everything 5x too big.
- **z-depth vs range**: most RGB-D sensors give z (distance along the optical axis); some lidars,
  ToF and renderers give Euclidean range along the ray. Convert range r with
  `z = r / sqrt(1 + x_n^2 + y_n^2)` where `x_n, y_n` are normalised coordinates.
- Use the intrinsics of the image the depth is registered to (depth-aligned-to-colour uses colour K).
- Pixel centre convention: OpenCV K assumes integer pixel indices are centres; renderers might use
  `u + 0.5`.

## Open3D
```python
color = o3d.io.read_image("rgb.png"); depth = o3d.io.read_image("depth.png")
rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(color, depth, depth_scale=1000.0,
                                                          depth_trunc=4.0, convert_rgb_to_intensity=False)
intr = o3d.camera.PinholeCameraIntrinsic(w, h, fx, fy, cx, cy)
pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intr, extrinsic=T_cam_world)
```
`extrinsic` is world-to-camera; the cloud comes out in world coordinates (checked against
`inv(T) @ p_cam` from the NumPy back-projection above, agreement 1e-7; applying `T` instead is off
by several metres).

## Organised clouds
Keep the (H, W, 3) layout for neighbour operations (normals by cross product of pixel neighbours,
fast segmentation); PCL calls these organised point clouds.

## From disparity
`cv2.reprojectImageTo3D(disp, Q)` with Q from `stereoRectify` (disparity as float pixels).

## Verify
Back-project a flat wall: plane fit residual should match sensor noise; measured distance between two
known points should match a tape measure.
