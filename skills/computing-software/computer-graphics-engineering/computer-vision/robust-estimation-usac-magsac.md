---
id: computing-software.computer-graphics-engineering.computer-vision.robust-estimation-usac-magsac
name: robust-estimation-usac-magsac
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, robust-estimation, usac, magsac, prosac, ransac, inlier-threshold, findhomography, findfundamentalmat, lo-ransac]
level: advanced
status: verified
description: "Estimate homographies, fundamental/essential matrices and poses robustly with modern RANSAC variants (USAC, MAGSAC++, PROSAC): thresholds, confidence, iterations, and refinement."
sources: ["https://docs.opencv.org/4.x/de/d3e/tutorial_usac.html", "https://arxiv.org/abs/1912.05909", "https://szeliski.org/Book/", "https://www.robots.ox.ac.uk/~vgg/hzbook/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust estimation with USAC and MAGSAC

**Goal:** correct geometric models from feature matches with 30–90% outliers, faster and
more accurately than textbook RANSAC (Hartley & Zisserman, ch. 4).

## 1. RANSAC essentials
Sample minimal sets (4 for H, 7/8 for F, 5 for E, 3 for P3P), fit, count inliers within
threshold τ, keep the best. Iterations needed:
`N = log(1 - confidence) / log(1 - w^s)`, w = inlier ratio, s = sample size.
At w = 0.3, s = 8 (F): ~70,000 iterations for 99% (computed: 70,188) — why minimal solvers and
better sampling matter.

## 2. OpenCV USAC (tested on OpenCV 5.0.0)
```python
H, mask = cv2.findHomography(src, dst, cv2.USAC_MAGSAC, ransacReprojThreshold=3.0,
                             maxIters=10000, confidence=0.999)
F, mask = cv2.findFundamentalMat(p1, p2, cv2.USAC_MAGSAC, 1.0, 0.999, 10000)
E, mask = cv2.findEssentialMat(p1, p2, K, method=cv2.USAC_MAGSAC, prob=0.999, threshold=1.0)
```
Flags: `USAC_DEFAULT` (MSAC scoring with inner and iterative local optimisation), `USAC_PROSAC` (needs matches **sorted by quality**,
e.g. ratio-test score; on 2,000 homography matches with 80% outliers, sorted
input took 0.27 ms against 1.2 ms for the same flag on random order, 3.0 ms for `USAC_DEFAULT` and
84 ms for plain `RANSAC`, all with 407 inliers), `USAC_MAGSAC` (MAGSAC++ scoring with sigma-consensus local optimisation, designed to be
less sensitive to the threshold; on the synthetic pair below it was no more accurate than the other USAC flags), `USAC_ACCURATE` (graph-cut local optimisation, i.e. GC-RANSAC),
`USAC_FAST`, `USAC_PARALLEL`. Fine control: `cv2.UsacParams` (fields include `threshold`,
`confidence`, `maxIterations`, `loMethod`, `sampler`, `score`, `randomGeneratorState`). On a
1,000-match synthetic pair with 50% outliers, all USAC flags recovered 94-95% of the true inliers
with 1 to 3 false inliers for F, while plain `RANSAC` at the same settings kept only 74%.

## 3. Thresholds
- In **pixels** for H/F (reprojection or Sampson distance): 1–3 px for good features at
  native resolution; scale with image downsampling.
- `findEssentialMat` takes its threshold in pixels together with K (threshold 1.0 gave 485 of 500
  true inliers at 0.5 px noise).

## 4. Degeneracies
- Planar scene or pure rotation → F/E degenerate (use H, or compare H and F model scores).
- All points clustered in one image region → unstable models; enforce spatial spread (grid
  bucketing of matches).
- Too few matches (< 2–3x minimal) → reject the estimate.

## 5. Refine
Final nonlinear refinement on inliers (Levenberg–Marquardt minimising reprojection/Sampson
error) — OpenCV's USAC does local optimisation; for H also `cv2.findHomography(..., 0)` on
inliers or a custom LM.

## Gotchas
- Inlier ratio alone is misleading: check inlier **count** and spatial distribution.
- Duplicate matches inflate inlier counts — enforce one-to-one matching (cross-check).
- Results vary with random seed; set it for reproducible tests (`UsacParams.randomGeneratorState`).

## Verify
- [ ] On a benchmark pair set: reprojection error and success rate compared across USAC flags.
- [ ] Runtime per estimate within budget at worst-case outlier ratio.
- [ ] Degenerate-scene tests (planar wall, rotation-only) handled without garbage models.
