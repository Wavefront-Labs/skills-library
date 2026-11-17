---
id: computing-software.computer-graphics-engineering.opencv.opencv-descriptor-matching-ratio-test
name: opencv-descriptor-matching-ratio-test
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, feature-matching, features2d, flann, ratio-test, bfmatcher, knnmatch, cross-check, hamming-distance, lowe-ratio]
level: practitioner
status: verified
description: "Match keypoint descriptors reliably in OpenCV: BFMatcher norms per descriptor type, FLANN index parameters for float vs binary, Lowe's ratio test."
sources: ["https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html", "https://docs.opencv.org/4.x/d5/d6f/tutorial_feature_flann_matcher.html", "https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV descriptor matching with the ratio test

**Goal:** a correspondence set with high inlier ratio for homography/pose/stitching —
matching quality matters more than detector choice in most pipelines.

## 1. Choose the matcher and norm
| descriptor | type | BFMatcher norm | FLANN index |
|---|---|---|---|
| SIFT, SURF (contrib, non-free), KAZE | float32 | `NORM_L2` | KD-tree: `dict(algorithm=1, trees=5)` |
| ORB, BRISK, AKAZE (binary), BRIEF | uint8 bits | `NORM_HAMMING` (`HAMMING2` for ORB WTA_K=3/4) | LSH: `dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)` |
Wrong norm (L2 on binary descriptors) silently gives poor matches. Brute force is exact and fine
up to a few thousand descriptors; FLANN for large sets.

## 2. Lowe's ratio test
```python
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
knn = bf.knnMatch(des1, des2, k=2)
good = [m for m, n in (p for p in knn if len(p) == 2) if m.distance < 0.75 * n.distance]
```
Keep a match only if the best is clearly better than the second best — removes ambiguous
matches on repetitive texture. 0.7–0.8 typical (Lowe used 0.8; stricter 0.7 for cleaner sets).
FLANN-LSH may return fewer than 2 neighbours — guard `len(p) == 2`.

## 3. Cross-check / mutual nearest neighbour
`cv2.BFMatcher(norm, crossCheck=True).match(des1, des2)` keeps only mutual best matches.
Don't combine crossCheck with knnMatch(k=2): it raises a cv::Exception (checked on 4.14); do mutual
filtering manually if you want both.

## 4. Spatial verification
Pass `good` points to `findHomography` / `findFundamentalMat` with RANSAC/USAC and keep inliers;
for video tracking add a motion-consistency gate (matches near predicted position). Sort matches
by distance/ratio for PROSAC.

## 5. Distribution
Matches clustered in one region give unstable geometry: detect features on a grid
(per-cell max features) or use `cv2.ORB_create(nfeatures=..., scoreType=...)` with adaptive
non-maximal suppression downstream.

## Gotchas
- Descriptor dtype: FLANN KD-tree needs float32 (`des.astype(np.float32)`), LSH needs uint8 (the wrong
  dtype raises an error in `FlannBasedMatcher.knnMatch`, checked). The index ids are plain ints in Python
  (`cv2.FLANN_INDEX_KDTREE` does not exist): `algorithm=1` KD-tree, `algorithm=6` LSH.
- OpenCV 5.0 moved `AKAZE`, `BRISK` and `KAZE` into the contrib `cv2.xfeatures2d` module
  (`cv2.xfeatures2d.AKAZE_create()`); `cv2.AKAZE_create` is gone there. In 4.14 they are in `cv2`.
- L2 on binary descriptors raises no error: it just returns poor matches.
- Empty descriptors (`None`) when no keypoints are found — check before matching.
- Ratio test on symmetric scenes (windows, tiles) still leaves wrong matches — geometric
  verification is mandatory.

## Verify
- [ ] Inlier ratio after RANSAC logged; > 50% on typical pairs indicates healthy matching.
- [ ] Norm/index parameters asserted against descriptor type in code.
- [ ] Matches visualised (`cv2.drawMatches`) on difficult pairs during tuning.
