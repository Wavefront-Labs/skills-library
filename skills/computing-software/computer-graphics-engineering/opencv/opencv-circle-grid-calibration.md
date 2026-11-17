---
id: computing-software.computer-graphics-engineering.opencv.opencv-circle-grid-calibration
name: opencv-circle-grid-calibration
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, circle-grid, findcirclesgrid, asymmetric-circles, camera-calibration, simpleblobdetector]
level: practitioner
status: verified
description: "Calibrate with circle grids in OpenCV: symmetric vs asymmetric patterns, findCirclesGrid with a tuned SimpleBlobDetector, object point layout and circle-centre perspective bias."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://docs.opencv.org/4.x/da/d0d/tutorial_camera_calibration_pattern.html", "https://docs.opencv.org/4.x/d4/d94/tutorial_camera_calibration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Circle grid calibration

Circle centres are found from blob moments over many pixels: robust to blur and noise, good for
thermal cameras (heated/cooled discs) and low-resolution sensors.

## Generate patterns
`python generate_pattern.py -o acircles.svg -r 11 -c 4 -T acircles -s 20 -R 5`
(`apps/pattern-tools` in the OpenCV repo; older releases call it `gen_pattern.py` under `doc/pattern_tools`;
`-r` rows, `-c` columns, `-T` type, `-s` square size, `-R` radius rate, per its docstring). Asymmetric grids are unambiguous under 180-degree rotation;
symmetric ones are not.

## Detect
```python
p = cv2.SimpleBlobDetector_Params()
p.minArea = 50; p.maxArea = 50000; p.filterByCircularity = True; p.minCircularity = 0.6
det = cv2.SimpleBlobDetector_create(p)
ok, centers = cv2.findCirclesGrid(gray, (4, 11), flags=cv2.CALIB_CB_ASYMMETRIC_GRID, blobDetector=det)
```
- Pattern size for asymmetric grids is `(points_per_row, rows)`, e.g. `(4, 11)` for the standard
  OpenCV asymmetric pattern.
- Default blob detector looks for **dark** blobs (`blobColor` 0); for white circles on black set
  `p.blobColor = 255` (checked: a white 4x11 grid with 14 px radius is found only with it).
- Default `maxArea` (5000) misses large circles at close range (radius 42 px, area about 5540: not found
  until `maxArea` is raised): raise it.
- Add `cv2.CALIB_CB_CLUSTERING` for strong perspective/wide-angle views.

## Object points (asymmetric)
```python
objp = np.array([[(2 * j + i % 2) * s, i * s, 0] for i in range(11) for j in range(4)], np.float32)
```
where `s` is half the diagonal centre spacing of the printed pattern. Mismatch here is the most
common cause of high RMS.

## Perspective bias
A projected circle is an ellipse whose centroid is not the projection of the circle centre. Bias
grows with circle size and obliquity: keep circles small relative to spacing, avoid extreme
tilts, or use an iterative refinement. Checkerboard/ChArUco corners do not have this bias.

## Verify
Draw with `cv2.drawChessboardCorners(img, (4,11), centers, ok)`: ordering must be consistent
across all views; RMS typically 0.1 to 0.3 px.
