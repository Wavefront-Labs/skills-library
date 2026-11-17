---
id: computing-software.computer-graphics-engineering.computer-vision.cylindrical-and-spherical-panorama-projection
name: cylindrical-and-spherical-panorama-projection
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, alignment-stitching, cylindrical-projection, spherical-panorama, equirectangular, panorama, remap]
level: practitioner
status: verified
description: "Warp images to cylindrical or spherical (equirectangular) coordinates for panoramas: focal length in pixels, forward/inverse maps with remap, and OpenCV stitching warpers."
sources: ["https://szeliski.org/Book/", "https://docs.opencv.org/4.x/d1/d46/group__stitching.html", "https://docs.opencv.org/4.x/d0/d33/tutorial_table_of_content_stitching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cylindrical and spherical projection

For a camera rotating about its optical centre, warping each image to a cylinder or sphere turns
rotation into translation (cylinder: pan only) so images can be aligned by shifts.

## Inverse map (cylindrical)
```python
def cyl_maps(w, h, f):
    cx, cy = w / 2, h / 2
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    theta = (xs - cx) / f                 # output column -> angle
    hgt = (ys - cy) / f
    X, Y, Z = np.sin(theta), hgt, np.cos(theta)
    mapx = (f * X / Z + cx).astype(np.float32); mapy = (f * Y / Z + cy).astype(np.float32)
    return mapx, mapy
cyl = cv2.remap(img, *cyl_maps(w, h, f), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
```
Always build the **inverse** map (output pixel -> source pixel) for remap; forward mapping leaves
holes.

## Spherical / equirectangular
Output column = longitude, row = latitude: `X = sin(lon) cos(lat)`, `Y = sin(lat)`,
`Z = cos(lon) cos(lat)`, then rotate by the camera's R before projecting with K. A full 360x180
panorama is 2:1; width about `2 * pi * f` keeps native resolution.

## Focal length matters
f must be in pixels (`f_mm / sensor_width_mm * image_width`, or from calibration/EXIF). Wrong f
bends straight lines and causes drift at the panorama ends. Undistort lens distortion first.

## OpenCV stitching warpers
`cv2.Stitcher` uses `SphericalWarper` by default in PANORAMA mode (`AffineWarper` in SCANS mode;
source `stitcher.cpp`). In Python the C++ warper classes are not exposed by name; build one with
`cv2.PyRotationWarper(type, scale)` where `type` is a string that was accepted in OpenCV 5.0.0:
`"plane"`, `"cylindrical"`, `"spherical"`, `"fisheye"`, `"stereographic"`, `"mercator"`,
`"transverseMercator"`, `"compressedPlaneA2B1"`, `"paniniA2B1"`, `"paniniPortraitA2B1"`
(Panini keeps verticals straight with wide FOV). Class names such as `"CylindricalWarper"` raise
an error.

## Choosing
| Coverage | Projection |
|---|---|
| < ~120 deg | Planar (perspective) |
| Horizontal 360, limited vertical | Cylindrical |
| Full sphere / VR | Equirectangular (spherical) |
| Wide architectural | Panini / stereographic |

## Verify
Pan a camera on a tripod (nodal point aligned): after cylindrical warping, consecutive images
should align by a pure horizontal shift with no vertical drift.
