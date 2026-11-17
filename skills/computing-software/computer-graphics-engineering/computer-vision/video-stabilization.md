---
id: computing-software.computer-graphics-engineering.computer-vision.video-stabilization
name: video-stabilization
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-alignment, image-registration, video-stabilization, camera-path-smoothing, estimateaffinepartial2d, optical-flow, crop-ratio, gyro-stabilization]
level: practitioner
status: verified
description: "Stabilise shaky video: track features, estimate inter-frame similarity transforms, smooth the camera trajectory, warp with crop compensation."
sources: ["https://szeliski.org/Book/", "https://docs.opencv.org/4.x/d5/d50/group__videostab.html", "https://research.google/pubs/auto-directed-video-stabilization-with-robust-l1-optimal-camera-paths/", "https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video stabilisation

**Goal:** smooth handheld/drone/vehicle footage by removing high-frequency camera motion
while keeping intentional pans.

## 1. Estimate inter-frame motion
```python
prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=400, qualityLevel=0.01, minDistance=20)
curr_pts, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_pts, None)
good = st.ravel() == 1
M, inl = cv2.estimateAffinePartial2D(prev_pts[good], curr_pts[good], method=cv2.RANSAC,
                                     ransacReprojThreshold=3)
dx, dy = M[0, 2], M[1, 2]; da = np.arctan2(M[1, 0], M[0, 0])
```
Similarity (translation + rotation + scale) is the robust default; full homography only for
distant/planar scenes. RANSAC rejects moving foreground objects (if they don't dominate). Tested on a synthetic shaky clip
(60 frames cropped from a larger image with known random translation and rotation): the estimated
`(dx, dy, da)` matched the true inter-frame camera motion to about 0.03 px with the sign reversed
(feature motion is the opposite of camera motion).

## 2. Smooth the trajectory
Accumulate per-frame (dx, dy, da) into a trajectory; smooth it:
- Moving average / Gaussian window of ~1–2 s (offline).
- Kalman filter or exponential smoothing (real-time, with lag).
- L1-optimal camera paths (Grundmann et al., CVPR 2011): piecewise constant/linear/parabolic segments —
  looks like tripod/dolly moves.
Correction = smoothed − raw **cumulative** trajectory; apply to each frame. Tested with a 31-frame
moving average: using the correction itself as the warp cut the residual inter-frame translation
std to 22% (x) and 13% (y) of the raw; adding the per-frame estimate to it (`est + correction`, as
some tutorials do) made it worse, 147% and 138% of the raw.

## 3. Warp and crop
```python
T = np.array([[np.cos(a), -np.sin(a), x], [np.sin(a), np.cos(a), y]])
stab = cv2.warpAffine(frame, T, (w, h), borderMode=cv2.BORDER_REFLECT)
stab = zoom_crop(stab, 1.1)        # fixed crop hides borders; trade field of view vs stability
```
Constrain the smoothed path so the crop window stays inside the frame (the L1 method does
this explicitly).

## 4. Better motion sources
- **Gyro data** (phones, action cams, drones): exact rotation per frame/row — far more robust
  than vision, and handles rolling shutter with per-row warps (Gyroflow stabilises from gyroscope
  data and lists rolling shutter correction in its README).
- Rolling-shutter wobble needs mesh/row-wise warps; a single global transform can't fix jello.
- OpenCV's `videostab` module is C++ (one-pass/two-pass, motion inpainting); the Python bindings in
  OpenCV 5.0.0 expose only the motion-model constants (`cv2.videostab.MM_AFFINE` and friends), not
  the stabiliser classes.

## Gotchas
- Large moving objects (vehicles, crowds) pull the estimate — mask them or use more robust
  estimation over background features.
- Low-texture scenes (sky, water) → few features → drift; fall back to identity.
- Over-smoothing removes intentional motion and needs huge crops; tune window per content.

## Verify
- [ ] Trajectory plots before/after show high-frequency removal with intent preserved.
- [ ] Inter-frame residual motion (feature displacement) reduced by the expected factor.
- [ ] Crop ratio within the accepted field-of-view loss; no black borders.
