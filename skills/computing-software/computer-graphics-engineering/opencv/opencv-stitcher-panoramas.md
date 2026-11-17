---
id: computing-software.computer-graphics-engineering.opencv.opencv-stitcher-panoramas
name: opencv-stitcher-panoramas
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, stitcher, panorama-stitching, cv-stitching, scans-mode]
level: practitioner
status: docs-checked
description: "Stitch panoramas and flat scans with cv::Stitcher: modes, resolution setters, status codes, component(), and the estimate/compose split."
sources: ["https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html", "https://docs.opencv.org/4.x/d2/d8d/classcv_1_1Stitcher.html", "https://github.com/opencv/opencv/blob/4.x/samples/cpp/stitching_detailed.cpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/modules/stitching/include/opencv2/stitching.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panorama stitching with cv::Stitcher

## 1. High-level API
```python
st = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)     # or cv2.Stitcher_SCANS
st.setRegistrationResol(0.6)        # resolution in megapixels for registration
st.setPanoConfidenceThresh(1.0)
status, pano = st.stitch(images)
if status != cv2.Stitcher_OK:
    raise RuntimeError(status)
```
- Status codes (stitching.hpp): `OK = 0`, `ERR_NEED_MORE_IMGS = 1`, `ERR_HOMOGRAPHY_EST_FAIL = 2`, `ERR_CAMERA_PARAMS_ADJUST_FAIL = 3`.
- `Mode::PANORAMA` (default): photo panoramas, expects images under perspective transformation and projects the result onto a sphere (SphericalWarper, BestOf2NearestMatcher).
- `Mode::SCANS`: composing scans, expects images under affine transformation, does not compensate exposure by default (AffineWarper, AffineBestOf2NearestMatcher).
- Resolution setters, all in megapixels: `setRegistrationResol`, `setSeamEstimationResol`, `setCompositingResol`; `Stitcher::ORIG_RESOL` (-1) is the placeholder that preserves the original resolution. Also `setPanoConfidenceThresh`, `setWaveCorrection`, `setInterpolationFlags`.
- `stitch(images, masks, pano)` accepts optional masks saying where to look for keypoints.
- `component()` returns the 0-based indices of the input images that made it into the panorama; `cameras()` returns estimated camera parameters; `resultMask()` returns an 8U mask (0xFF filled, 0 unused) usable for inpainting.

## 2. Customising the pipeline
The header exposes setters for the features finder (`setFeaturesFinder`), matcher, bundle adjuster, estimator, warper, exposure compensator, seam finder and blender. For full control the header points to `samples/cpp/stitching_detailed.cpp`, and to `estimateTransform` followed by `composePanorama` when transforms are computed once and reused ("only if you're aware of the stitching pipeline"; otherwise use `stitch`).

## Capture advice (practitioner guidance, not from the sources)
Rotate about the camera's optical centre to limit parallax ghosting; keep exposure and white balance fixed and give neighbouring frames generous overlap.

## Gotchas
- Check `component()` after stitching to find images that were dropped.
- `ERR_NEED_MORE_IMGS` can mean too few images matched with enough confidence; try more overlap, or adjust the confidence threshold and verify the effect on your data.

## Verify
- [ ] All expected image indices appear in `component()`.
- [ ] Straight lines look straight in the output.

## Checked
Method: docs-checked 2026-11-09 against stitching.hpp (4.x) from raw GitHub; docs.opencv.org pages and the stitching_detailed sample were not read.
Removed as unconfirmed: the registration default of 0.6, the 30 to 50 percent overlap rule, the 0.3 to 0.5 confidence-threshold suggestion, claims about bundle adjustment on rotations and focal length for PANORAMA mode, and the list of what the detailed sample can do (SIFT/ORB/AKAZE, cylindrical and fisheye warpers, graph-cut seams), and the whiteboard and drone examples for SCANS.
