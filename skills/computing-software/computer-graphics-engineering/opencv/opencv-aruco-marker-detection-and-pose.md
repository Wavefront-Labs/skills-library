---
id: computing-software.computer-graphics-engineering.opencv.opencv-aruco-marker-detection-and-pose
name: opencv-aruco-marker-detection-and-pose
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, objdetect, marker-detection, aruco, arucodetector, fiducial-markers, solvepnp, marker-pose, apriltag, generateimagemarker, aruco-dictionary]
level: practitioner
status: verified
description: "Detect ArUco/AprilTag markers with the OpenCV 4.7+ ArucoDetector API, tune detector parameters, estimate marker pose with solvePnP, and print markers at a known size."
sources: ["https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html", "https://docs.opencv.org/4.x/d2/d1a/classcv_1_1aruco_1_1ArucoDetector.html", "https://docs.opencv.org/4.x/d1/dcd/structcv_1_1aruco_1_1DetectorParameters.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV ArUco marker detection and pose

**Goal:** reliable IDs and 6-DoF poses of printed fiducial markers for AR, robot
localisation, calibration targets and measurement.

## 1. Generate and print
```python
d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)   # small dict = more robust
img = cv2.aruco.generateImageMarker(d, id=7, sidePixels=600, borderBits=1)
cv2.imwrite("marker7.png", img)
```
Print with a white quiet zone around the black border; **measure the printed black square
side** with calipers — that measured length is `markerLength` for pose.
Choose the smallest dictionary covering your IDs (4x4_50 beats 6x6_1000 on detection range
and false positives). AprilTag families: `DICT_APRILTAG_36h11`.

## 2. Detect (OpenCV ≥ 4.7 API)
```python
params = cv2.aruco.DetectorParameters()
params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX    # better pose accuracy
det = cv2.aruco.ArucoDetector(d, params)
corners, ids, rejected = det.detectMarkers(gray)
cv2.aruco.drawDetectedMarkers(frame, corners, ids)
```
The legacy free functions (`cv2.aruco.detectMarkers`, `estimatePoseSingleMarkers`) were deprecated
in 4.7 but still exist in 4.14; they are gone in OpenCV 5.0 (AttributeError, checked on 5.0.0), so
old tutorial code breaks on 5.x.

Useful parameters: `adaptiveThreshWinSizeMin/Max/Step` (lighting), `minMarkerPerimeterRate`
(small/distant markers), `polygonalApproxAccuracyRate`, `errorCorrectionRate` (lower =
fewer false IDs).

## 3. Pose per marker
```python
L = 0.05                                                   # metres, measured
obj = np.array([[-L/2,  L/2, 0], [ L/2,  L/2, 0],
                [ L/2, -L/2, 0], [-L/2, -L/2, 0]], np.float32)   # corner order TL, TR, BR, BL
for c in corners:
    ok, rvec, tvec = cv2.solvePnP(obj, c.reshape(4, 2), K, dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
    cv2.drawFrameAxes(frame, K, dist, rvec, tvec, L * 0.5)
```
`estimatePoseSingleMarkers` is deprecated (and removed in 5.0); `SOLVEPNP_IPPE_SQUARE` is designed for this
square layout. Requires calibrated `K` and `dist`.

## 4. Accuracy
- Single small marker poses flip (planar ambiguity) at near-frontal views and jitter in
  rotation; use a **board** (`cv2.aruco.GridBoard` / ChArUco) or multiple markers with
  `solvePnP` on all corners for stable poses.
- Filter temporally (One-Euro filter / Kalman) for AR overlays.
- Marker pixel size ≥ ~20 px side for reliable decoding; pose accuracy improves with size.

## Gotchas
- Glossy prints/laminate reflect → missed detections; matte paper, flat mounting.
- Motion blur kills detection; short exposure.
- Mixed-up corner order between object and image points gives wild poses.

## Verify
- [ ] Measured distance to a marker at known range matches within ~1–2%.
- [ ] Detection rate logged across test videos; false IDs = 0 on marker-free footage.
- [ ] Code uses ArucoDetector (no deprecated free functions).
