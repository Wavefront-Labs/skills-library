---
id: computing-software.computer-graphics-engineering.computer-vision.camera-pose-and-slam
name: camera-pose-and-slam
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-vision, slam, visual-odometry, pnp, pose-estimation, essential-matrix, fundamental-matrix, bundle-adjustment, orb-slam, g2o, ceres, loop-closure, epipolar-geometry]
level: advanced
status: verified
description: "Estimate camera pose from images (PnP, essential/fundamental matrix) and run visual odometry/SLAM: feature tracks, bundle adjustment, loop closure, drift causes."
sources: ["https://www.robots.ox.ac.uk/~vgg/hzbook/", "https://github.com/raulmur/ORB_SLAM2", "http://ceres-solver.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera pose estimation and SLAM fundamentals

**Goal:** recover a camera's position/orientation from image correspondences, and
chain that into visual odometry/SLAM without silently accumulating drift. This
sits one layer above `computer-vision.detection-and-tracking-pipeline` and under
`opencv.camera-calibration-and-undistortion` (you need intrinsics calibrated first).

## Single-frame pose: PnP
Given 3D points with known 2D projections (e.g. a calibration rig, or a sparse map
already built) and known intrinsics `K`:
- `cv2.solvePnP` / `solvePnPRansac` (`SOLVEPNP_SQPNP`/`EPNP` with enough points, RANSAC when correspondences
  have outliers — always use RANSAC for anything from real feature matching).
- Point counts depend on the flag (OpenCV 5.0.0, run on noise-free synthetic data): `SOLVEPNP_P3P` and `SOLVEPNP_AP3P` take exactly 4 points (3 raises an error; the 4th resolves the P3P ambiguity); `SOLVEPNP_ITERATIVE` raised an error with 4 non-coplanar points; `SOLVEPNP_EPNP` accepted 4 points but returned a wrong pose (5 points were exact), so give EPnP/ITERATIVE 6 or more. Planar targets work with EPNP, ITERATIVE and SQPNP; `SOLVEPNP_IPPE` is for planar targets whose object points all have z = 0 (it gave a wrong pose when they did not).
- Output is `rvec, tvec` = **object-to-camera**, not camera-to-world — invert
  (`R.T`, `-R.T @ t`) if you want the camera's position in world space. This sign/
  frame confusion is the single most common pose bug.

## Two-frame pose: epipolar geometry (no 3D points yet)
- Match features (ORB/SIFT) between two frames, filter with RANSAC while estimating
  the **essential matrix** `E` (calibrated cameras, `cv2.findEssentialMat`) or
  **fundamental matrix** `F` (uncalibrated, `cv2.findFundamentalMat`).
- Recover `R, t` from `E` via `cv2.recoverPose` — gives rotation and translation
  **up to scale**: monocular vision never recovers absolute scale from two frames
  alone. Scale comes from a known baseline (stereo), an IMU, a known object size, or
  drifts freely (monocular SLAM scale drift).
- Degenerate case: pure rotation (no translation) makes `E` degenerate — common
  when a user just pans the camera in place. `findEssentialMat` still returned a 3x3 matrix in a run,
  but `recoverPose` kept 0 inlier points and `t` was arbitrary, so check the inlier count and low
  parallax, and fall back to homography-only tracking (on the same pure-rotation data all 200 points were
  homography inliers).

## Visual odometry → SLAM
VO = chain frame-to-frame poses. SLAM = VO + a persistent map + **loop closure** to
correct drift when you revisit a place.
- Track 2D features frame-to-frame (KLT optical flow or descriptor matching),
  triangulate new 3D map points when parallax is sufficient, solve PnP against the
  existing map for new frames (this is what keeps scale/drift from compounding as
  fast as frame-to-frame-only VO).
- **Bundle adjustment**: nonlinear least-squares refinement of poses + 3D points
  jointly, minimising reprojection error. Local BA (sliding window, every frame) for
  speed; global BA / pose-graph optimisation (g2o, Ceres, GTSAM) on loop closure.
- **Loop closure**: detect revisits via place recognition (bag-of-words on
  descriptors — DBoW2 is what ORB-SLAM uses, or a learned global descriptor), then
  add a constraint and re-optimise the pose graph. Without it, a long monocular
  trajectory drifts unboundedly, especially in scale.
- Keyframe selection: don't triangulate/BA every frame — select keyframes by parallax
  or tracked-feature-count threshold, or cost explodes and redundant frames add
  nothing.

## Failure modes
- **Scale drift** (monocular): unavoidable without an external scale reference;
  stereo or RGB-D fixes it structurally.
- **Low-texture / repetitive scenes** (blank walls, checkerboard floors): feature
  matching fails or aliases; VO loses tracking — have a relocalisation fallback.
- **Rolling shutter**: feature positions are time-skewed across the frame; at high
  angular velocity this biases pose estimates. Global-shutter sensors avoid it.
- **Dynamic objects** (people, cars) in features: violates the static-scene
  assumption and corrupts `E`/PnP unless outlier-rejected — RANSAC helps but a
  moving object that covers a large frame fraction can out-vote the static background.

## Verify
- [ ] Reprojection error after PnP/BA is sub-pixel on average (print RMS error).
- [ ] Recovered trajectory is consistent with a known path shape (e.g. closes a loop
      you physically walked) before trusting absolute positions.
- [ ] Pose frame convention (object-to-camera vs camera-to-world) is checked, not
      assumed — a sign error here still "runs" but silently produces nonsense.
- [ ] Scale is anchored by something other than monocular two-view geometry if
      absolute units matter.

## Checked
OpenCV 5.0.0 (opencv-python 5.0.0.93), NumPy 2.5.4, scratch venv on Windows.
- Run: synthetic scene (30 points, K = 800 px focal) through `solvePnP` with EPNP, ITERATIVE, P3P, AP3P, SQPNP, IPPE at 3, 4, 5 and 10 points, planar and non-planar (results in the corrected bullet); `solvePnPRansac` recovered the pose (30/30 inliers) and `-R.T @ t` matched the true camera centre to 1e-7, confirming `rvec, tvec` are object-to-camera; `findEssentialMat` + `recoverPose` recovered R (error 3e-13) and the translation direction (unit length, so no scale) on a two-view scene; pure rotation behaviour as above; `findFundamentalMat` and `findHomography` calls ran.
- Fetched: ORB_SLAM2 README (credits DBoW2, g2o bundled in Thirdparty).
