---
id: computing-software.computer-graphics-engineering.opencv.opencv-usac-flags-in-calib3d
name: opencv-usac-flags-in-calib3d
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, usac-flags, usac, magsac, findhomography, findessentialmat, robust-estimation]
level: advanced
status: docs-checked
description: "Use OpenCV USAC estimators in calib3d: USAC_MAGSAC/ACCURATE/FAST/PROSAC flags, UsacParams for findHomography and findEssentialMat, thresholds, confidence and iteration control."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://docs.opencv.org/4.x/de/d3e/tutorial_usac.html", "https://github.com/opencv/opencv/blob/4.x/doc/tutorials/calib3d/usac.markdown", "https://github.com/opencv/opencv/blob/4.x/modules/calib3d/src/usac/ransac_solvers.cpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USAC flags in calib3d

`findHomography`, `findFundamentalMat`, `findEssentialMat` and `estimateAffine2D` accept the USAC flags as the `method`
in place of `cv2.RANSAC` (the 4.x sources dispatch methods from `USAC_DEFAULT` to `USAC_MAGSAC` to the USAC framework), and
`solvePnPRansac` accepts a USAC flag in `flags` or a `UsacParams` overload. The USAC tutorial is marked compatible with OpenCV >= 4.0
and the framework came from Google Summer of Code 2020.

| Flag | What it is | Use |
|---|---|---|
| `USAC_DEFAULT` (32) | uniform sampling, MSAC score, inner and iterative local optimisation | General drop-in |
| `USAC_PARALLEL` (33) | MSAC score, parallel, inner local optimisation | Large match sets |
| `USAC_FM_8PTS` (34) | 8-point fundamental matrix solver | Fundamental matrix |
| `USAC_FAST` (35) | fewer local optimisation iterations | Speed |
| `USAC_ACCURATE` (36) | graph-cut local optimisation (GC-RANSAC), slower | Accuracy |
| `USAC_PROSAC` (37) | PROSAC sampling | Matches sorted by quality |
| `USAC_MAGSAC` (38) | MAGSAC++ score with sigma local optimisation | Unknown noise level |
The table follows `setParameters` in `modules/calib3d/src/usac/ransac_solvers.cpp` (4.x) and the header comments.

```python
H, mask = cv2.findHomography(p1, p2, cv2.USAC_MAGSAC, ransacReprojThreshold=3.0,
                             maxIters=10000, confidence=0.999)
E, mask = cv2.findEssentialMat(p1, p2, K, method=cv2.USAC_ACCURATE, prob=0.999, threshold=1.0)
```

## UsacParams for full control
```python
p = cv2.UsacParams()
p.threshold = 1.5; p.confidence = 0.9999; p.maxIterations = 20000
p.sampler = cv2.SAMPLING_PROSAC; p.score = cv2.SCORE_METHOD_MAGSAC
p.loMethod = cv2.LOCAL_OPTIM_SIGMA; p.loIterations = 10      # the struct also has isParallel, loSampleSize, neighborsSearch, randomGeneratorState
H, mask = cv2.findHomography(p1, p2, p)
```

## Practical notes
- The tutorial says PROSAC assumes input points sorted by quality (for example by descriptor distance ratio of best to second match).
- The tutorial recommends MAGSAC when image noise is unknown because it does not need a threshold, but still advises giving an
  approximate threshold, since termination depends on the number of points with error below it (a threshold of 0 runs to the maximum iterations).
- `findEssentialMat` documents its `threshold` as the maximum distance from a point to an epipolar line in pixels.
- Parallel RANSAC is not deterministic with default options (tutorial); PROSAC without SPRT and local optimisation is the easiest way to make it deterministic.
- `UsacParams.randomGeneratorState` seeds the generator for repeatable runs.

## Verify
Compare inlier counts and reprojection RMS of `cv2.RANSAC` vs USAC flags on the same matches; also
time them.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/calib3d/include/opencv2/calib3d.hpp, doc/tutorials/calib3d/usac.markdown and modules/calib3d/src/usac/ransac_solvers.cpp. Confirmed: flag values and meanings, UsacParams fields, which functions take USAC methods or UsacParams, MAGSAC and PROSAC guidance, determinism note. Removed the unconfirmed 4.5.0 version, SPRT attribution for DEFAULT, 2 to 5 px guidance and cv2.setRNGSeed claim.
Method: documentation only; no commands were run.
