---
id: computing-software.computer-graphics-engineering.opencv.opencv-stereo-depth-and-point-clouds
name: opencv-stereo-depth-and-point-clouds
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [opencv, stereo-vision, depth-map, disparity, stereo-rectification, point-cloud, sgbm, block-matching, reprojectimageto3d, stereorectify]
level: advanced
status: docs-checked
description: "Turn a calibrated stereo pair into depth: stereoRectify and Q, StereoBM and StereoSGBM parameters, 16x fixed-point disparity, reprojectImageTo3D."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_calib3d/py_depthmap/py_depthmap.markdown", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/calib3d/include/opencv2/calib3d.hpp"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV stereo depth and point clouds

**Goal:** go from two calibrated cameras to a depth map or point cloud, and know which parameters shape the result. Requires `opencv.camera-calibration-and-undistortion` first.

## Rectification (calib3d.hpp)
- `stereoRectify` returns rectification rotations R1, R2, projection matrices P1, P2 and the 4x4 disparity-to-depth matrix Q. The first three columns of P1 and P2 act as the new rectified camera matrices; with R1 and R2 they go to `initUndistortRectifyMap` for each camera.
- For horizontal stereo, Q has the form with `1/Tx` in the bottom row (Tx is the horizontal shift between cameras); `CALIB_ZERO_DISPARITY` makes cx1 equal cx2.
- Check rectification visually: the header's stereo_calib sample draws red horizontal lines through corresponding regions to show the images are well rectified, which most stereo correspondence algorithms rely on. It also checks that the roi1 and roi2 interiors are valid pixels.

## Disparity
Tutorial relation: `disparity = x - x' = B*f / Z`, so depth is inversely proportional to disparity (B is the camera baseline, f the focal length).

`StereoBM.create(numDisparities=0, blockSize=21)` (the tutorial uses `numDisparities=16, blockSize=15` and notes the result is noisy until you adjust these). StereoBM parameters from the tutorial: texture threshold (filters areas without enough texture), speckle range and size, number of disparities (larger gives a larger visible depth range but more computation), min disparity, uniqueness ratio (post-filter), prefilter size and cap.

`StereoSGBM.create(minDisparity=0, numDisparities=16, blockSize=3, P1=0, P2=0, disp12MaxDiff=0, preFilterCap=0, uniquenessRatio=0, speckleWindowSize=0, speckleRange=0, mode=MODE_SGBM)` (calib3d.hpp):
- `numDisparities` is max minus min disparity and must be divisible by 16; `blockSize` odd, normally 3..11.
- `P1` and `P2` penalise disparity changes of 1 and of more than 1 between neighbours; P2 must exceed P1. The header cites 8*channels*blockSize^2 and 32*channels*blockSize^2 as reasonably good values from the stereo_match sample.
- `uniquenessRatio` normally 5-15; `speckleWindowSize` 0 disables speckle filtering, otherwise 50-200; `speckleRange` implicitly multiplied by 16, normally 1 or 2; `disp12MaxDiff` non-positive disables the left-right check.
- Default mode is single-pass (5 directions); `MODE_HH` runs the full two-pass algorithm and uses O(W*H*numDisparities) bytes, large for 640x480 and huge for HD.

## Disparity to 3D
- `StereoBM` and `StereoSGBM` return 16-bit fixed-point disparity with 4 fractional bits. `reprojectImageTo3D` assumes no fractional bits for 16-bit input, so divide by 16 and convert to float first.
- `reprojectImageTo3D(disparity, _3dImage, Q, handleMissingValues=false, ddepth=-1)` computes [X Y Z W] = Q * [x y disparity 1]. With Q from `stereoRectify`, points are in the first camera's rectified coordinate system.
- With `handleMissingValues=true`, pixels with the minimal disparity (outliers) become points with a very large Z (currently 10000); mask those out before computing statistics on the cloud.

## Verify
- [ ] Rectified pair shows the same feature on the same row.
- [ ] `numDisparities` covers the scene's depth range.
- [ ] 16-bit disparity divided by 16 before `reprojectImageTo3D`, and missing values masked.

## Checked
Method: docs-checked 2026-11-09 against the py_depthmap tutorial markdown and calib3d.hpp (4.x; stereoRectify, reprojectImageTo3D, StereoMatcher, StereoBM, StereoSGBM sections), raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: the claim that depth resolution degrades with the inverse square of distance, textureless, occlusion and specular failure-mode discussion (apart from the tutorial's texture-threshold note), structured light and ToF advice, the "numDisparities too small gives a flat foreground blob" claim, effects of blockSize on detail, and stereoCalibrate usage notes.
