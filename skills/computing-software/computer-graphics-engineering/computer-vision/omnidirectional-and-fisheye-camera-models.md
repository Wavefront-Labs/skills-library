---
id: computing-software.computer-graphics-engineering.computer-vision.omnidirectional-and-fisheye-camera-models
name: omnidirectional-and-fisheye-camera-models
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, omnidirectional-camera, fisheye, camera-model, kannala-brandt, double-sphere]
level: advanced
status: gated
description: "Pick a camera projection model for wide-angle optics: pinhole+Brown, Kannala-Brandt, unified/Mei, double sphere, Scaramuzza, equirectangular, and their calibration tools."
sources: ["https://arxiv.org/abs/1807.08957", "https://docs.opencv.org/4.x/dd/d12/tutorial_omnidir_calib_main.html", "https://github.com/ethz-asl/kalibr/wiki/supported-models", "https://sites.google.com/site/scarabotix/ocamcalib-omnidirectional-camera-calibration-toolbox-for-matlab"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera projection models (fisheye, omnidirectional)

| Model | FOV | Params | Where supported |
|---|---|---|---|
| Pinhole + radial-tangential (Brown) | < ~120 deg | fx,fy,cx,cy,k1..k6,p1,p2 | OpenCV `calibrateCamera`, everything |
| Equidistant / Kannala-Brandt | up to ~220 deg | + k1..k4 | `cv2.fisheye`, Kalibr `pinhole-equi`, COLMAP `OPENCV_FISHEYE` |
| Unified (Mei) | > 180 deg | xi + distortion | `cv2.omnidir`, Kalibr `omni` |
| Extended unified (EUCM) | > 180 deg | alpha, beta | Basalt, Kalibr `eucm` |
| Double sphere | > 180 deg | xi, alpha | Basalt, Kalibr `ds`; closed-form unprojection |
| Scaramuzza polynomial | catadioptric/fisheye | polynomial a0..aN | OCamCalib, MATLAB (gated: unconfirmed, source is paywalled or blocked) |
| Equirectangular | 360 x 180 | none | 360 cameras, panoramas |

## Choosing
- Under 120 degrees: pinhole + Brown is fine.
- Fisheye up to about 200 degrees, VO/SLAM: double sphere or Kannala-Brandt (Usenko et al. 2018
  propose DS as computationally inexpensive with a closed-form inverse, per the abstract).
- Mirrors (catadioptric): unified/Mei or Scaramuzza.
- Pick a model the downstream tool supports (COLMAP, ORB-SLAM3, Kalibr, OpenVINS) rather than the
  theoretically best one.

## Unprojection (pixel to ray)
Wide-angle pipelines should work with **bearing vectors** (unit rays), not normalised image
coordinates `(x/z, y/z)`, which blow up near 90 degrees and do not exist beyond (checked with
`cv2.fisheye.undistortPoints`: rays at 10, 45, 80, 100, 120 degrees came back as x/z = 0.176, 1.0,
5.67, -5.67, -1.73, i.e. tan(theta), and the 100 and 120 degree rays flipped sign).
Essential-matrix estimation and triangulation on bearings: OpenGV (gated: unconfirmed, source is paywalled or blocked).

## Calibration
- Kalibr (`kalibr_calibrate_cameras --models pinhole-equi ...`; the Kalibr wiki lists the projection models
pinhole, omni, ds, eucm and the distortions radtan, equi, fov, none) with an AprilGrid: also gives
  reprojection error per model so you can compare.
- `cv2.omnidir.calibrate(objectPoints, imagePoints, size, K, xi, D, flags, criteria)` (signature
  confirmed in OpenCV 5.0.0 contrib; it returns `retval, K, xi, D, rvecs, tvecs, idx`).

## Verify
Reprojection RMS under 0.5 px across the full image including the periphery; unproject then
project round-trip error near zero.
