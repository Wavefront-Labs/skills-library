---
id: computing-software.computer-graphics-engineering.opencv.opencv-ximgproc-guided-and-domain-transform-filters
name: opencv-ximgproc-guided-and-domain-transform-filters
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, guided-filter, ximgproc, domain-transform, edge-preserving-smoothing, joint-filtering, opencv-contrib]
level: practitioner
status: docs-checked
description: "Use OpenCV ximgproc edge-aware filters: guidedFilter, dtFilter (domain transform), fastGlobalSmootherFilter and joint filtering for depth/alpha upsampling. Choose radius/eps."
sources: ["https://docs.opencv.org/4.x/da/d17/group__ximgproc__filters.html", "https://docs.opencv.org/4.x/df/d2d/group__ximgproc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guided and domain-transform filters (ximgproc)

Uses the `cv2.ximgproc` module; confirm your OpenCV build or package includes it.

## Guided filter (He et al.)
```python
out = cv2.ximgproc.guidedFilter(guide=bgr, src=depth32f, radius=8, eps=1e-3 * 255**2)
```
- C++ signature: `guidedFilter(guide, src, dst, radius, eps, dDepth=-1, scale=1.0)`. Tune `radius` and `eps` on your own data (units of `eps` depend on the guide range).
- For repeated filtering with the same guide create the
  object once: `gf = cv2.ximgproc.createGuidedFilter(guide, r, eps); gf.filter(src)`.
- Self-guided filtering (`guide=src`) is possible.

## Domain transform (Gastal and Oliveira)
```python
out = cv2.ximgproc.dtFilter(guide, src, sigmaSpatial=30, sigmaColor=20, mode=cv2.ximgproc.DTF_RF)
```
- Modes: `DTF_NC` (the default), `DTF_IC`, `DTF_RF`; `numIters` defaults to 3.

## Other filters in the module
- `fastGlobalSmootherFilter(guide, src, lambda_, sigma_color)`: C++ also takes `lambda_attenuation=0.25`.
- `jointBilateralFilter`, `amFilter` (adaptive manifold), `rollingGuidanceFilter` (defaults: `sigmaColor=25`, `sigmaSpace=3`, `numOfIter=4`), `l0Smooth` (defaults: `lambda=0.02`, `kappa=2.0`).
- `createDisparityWLSFilter(left_matcher)` for stereo disparity refinement.

## Gotchas
- Check each function's page for accepted guide and source types.

## Verify
Visualise a horizontal profile across a guide edge: output should step sharply where the guide
does and be smooth elsewhere.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs: ximgproc edge-aware filters group (da/d17) and ximgproc module page.
- Confirmed: `guidedFilter`/`createGuidedFilter` signatures, `dtFilter`/`createDTFilter` (mode default `DTF_NC`, `numIters=3`), `DTF_NC`/`DTF_IC`/`DTF_RF`, `fastGlobalSmootherFilter` parameters, `jointBilateralFilter`, `amFilter`, `rollingGuidanceFilter` and `l0Smooth` defaults, `createDisparityWLSFilter(matcher_left)`.
- Removed: eps value ranges, O(1) cost claim, gradient-reversal claim, mode quality/speed descriptions, real-time claim, input-type and invalid-depth advice stated as fact, the "requires opencv-contrib-python" statement (packaging not checked; now says to confirm the build includes `cv2.ximgproc`).
- The He et al. reference link (kaiminghe.github.io/eccv10) returned 404 and was dropped from sources.

Method: documentation only; no commands were run.
