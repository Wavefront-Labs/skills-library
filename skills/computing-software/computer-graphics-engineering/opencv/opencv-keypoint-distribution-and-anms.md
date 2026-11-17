---
id: computing-software.computer-graphics-engineering.opencv.opencv-keypoint-distribution-and-anms
name: opencv-keypoint-distribution-and-anms
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, keypoint-distribution, anms, feature-bucketing, detector-tuning, orb]
level: advanced
status: docs-checked
description: "Spread OpenCV keypoints evenly: grid bucketing, the ANMS-Codes SSC implementation, and the ORB and SIFT create() parameters that control how many points survive."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/features2d/include/opencv2/features2d.hpp", "https://raw.githubusercontent.com/BAILOOL/ANMS-Codes/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keypoint distribution and ANMS

Detectors rank keypoints by score, so the retained set can cluster on high-texture regions; pose and homography estimation benefit from points spread over the image (practitioner guidance).

## Grid bucketing (practitioner helper)
Split the image into cells and keep the highest-response keypoints per cell:
```python
def bucket(kps, shape, rows, cols, per_cell):
    h, w = shape; cells = {}
    for k in kps:
        key = (int(k.pt[1] * rows / h), int(k.pt[0] * cols / w))
        cells.setdefault(key, []).append(k)
    out = []
    for v in cells.values():
        out += sorted(v, key=lambda k: -k.response)[:per_cell]
    return out
```
Choose rows, cols and per_cell for your image; detect more keypoints than you need first.

## ANMS code base (BAILOOL/ANMS-Codes README)
The repository implements the paper "Efficient adaptive non-maximal suppression algorithms for homogeneous spatial keypoint distribution" (Pattern Recognition Letters 2018), with C++, Python, Matlab and Java versions. Its README says the proposed SSC method has similar spatial distribution to competing ANMS methods but is substantially faster and scales better, and compares it visually with TopM and bucketing. Also implemented: bucketing, the original ANMS from "Multi-Image Matching using Multi-Scale Oriented Patches", and a more efficient ANMS. Tested with OpenCV 2.4.8, 3.3.1 and 4.2.0.

## ORB (features2d.hpp)
`ORB.create(nfeatures=500, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0, WTA_K=2, scoreType=HARRIS_SCORE, patchSize=31, fastThreshold=20)`.
- `nfeatures` is the maximum retained; features are ranked by score.
- `scaleFactor` greater than 1; the header warns a factor of 2 degrades matching scores dramatically, and a value too close to 1 needs more levels and costs speed.
- `edgeThreshold` is the border width where no features are detected and should roughly match `patchSize`.
- `scoreType`: HARRIS_SCORE ranks by Harris; FAST_SCORE is slightly less stable but a little faster.

## SIFT (features2d.hpp)
`SIFT.create(nfeatures=0, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6, enable_precise_upscale=false)`.
- Larger `contrastThreshold` yields fewer features; it is divided by `nOctaveLayers` when applied (the Lowe paper's 0.03 equals 0.09 here with the default 3 layers).
- Larger `edgeThreshold` retains more features (opposite sense to contrastThreshold).

## Measure
Track coverage (grid cells with inliers) and reprojection error rather than judging by eye (practitioner guidance).

## Checked
Method: docs-checked 2026-11-09 against features2d.hpp (4.x, ORB and SIFT sections) and the ANMS-Codes README, raw GitHub; the MOPS paper page was not read.
Removed as unconfirmed: the ANMS suppression-radius rule with c_robust 0.9, O(N^2) and O(N log N) complexities, ORB-SLAM's per-cell FAST fallback and quadtree description, SIFT contrastThreshold 0.01 to 0.02 for low-texture, the specific example detector settings (nfeatures 5000), the bucketing-before-matching gotcha and cross-detector response remark.
