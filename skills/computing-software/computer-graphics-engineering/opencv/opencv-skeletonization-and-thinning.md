---
id: computing-software.computer-graphics-engineering.opencv.opencv-skeletonization-and-thinning
name: opencv-skeletonization-and-thinning
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-contours, skeletonization, thinning, medial-axis, ximgproc, morphology]
level: practitioner
status: docs-checked
description: "Skeletonise binary shapes in OpenCV: ximgproc.thinning (Zhang-Suen, Guo-Hall), morphological skeleton, pruning spurs, and extracting endpoints/junctions for graph analysis."
sources: ["https://docs.opencv.org/4.x/df/d2d/group__ximgproc.html", "https://scikit-image.org/docs/stable/auto_examples/edges/plot_skeleton.html", "https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skeletonisation and thinning

## ximgproc.thinning (contrib)
```python
skel = cv2.ximgproc.thinning(binary, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
# or cv2.ximgproc.THINNING_GUOHALL
```
Input: a binary blob image. Clean the mask first (morphological opening, fill
small holes): every hole becomes a loop in the skeleton and every bump a spur.

## Pure-OpenCV morphological skeleton (no contrib)
```python
def morph_skeleton(img):
    skel = np.zeros_like(img); k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while cv2.countNonZero(img):
        eroded = cv2.erode(img, k)
        skel |= img - cv2.dilate(eroded, k)
        img = eroded
    return skel
```

## Alternatives
`skimage.morphology.skeletonize` and `medial_axis` (also returns the distance to boundary =
local stroke half-width, useful for vessel/crack width measurement).

## Endpoints and junctions
```python
nb = cv2.filter2D((skel > 0).astype(np.uint8), -1, np.ones((3, 3), np.uint8)) * (skel > 0)
endpoints = np.argwhere(nb == 2)        # self + 1 neighbour
junctions = np.argwhere(nb >= 4)        # self + 3 or more neighbours
```
Junction clusters of several adjacent pixels are common: merge them with connectedComponents.

## Pruning spurs
Iteratively remove endpoint pixels N times then regrow from the surviving endpoints along the
original skeleton, or build a graph of the skeleton and delete terminal branches shorter
than a length threshold.

## Gotchas
- Skeletons are very sensitive to boundary noise: smooth the mask (Gaussian blur + re-threshold)
  before thinning.
- Length from pixel count overestimates diagonals by up to 41 percent: weight diagonal steps by
  sqrt(2).

## Verify
A filled rectangle should thin to a straight line; a ring should become a single closed loop.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 ximgproc module page, the OpenCV morphological operations tutorial and the scikit-image skeleton example.
- Confirmed: `cv2.ximgproc.thinning(src[, dst[, thinningType]])`, `THINNING_ZHANGSUEN` (default, 0) and `THINNING_GUOHALL` (1), "binary blob thinning ... skeletization", `getStructuringElement`/`MORPH_CROSS`, `skimage.morphology.skeletonize` and `medial_axis` returning the distance transform (object width).
- Removed: staircase-artefact claim, uint8/255 input requirement, connectivity claim for the morphological skeleton, `skan` mention, corner-branch claim.
- The neighbour-count endpoint/junction recipe and the sqrt(2) diagonal weighting are arithmetic on the code shown.

Method: documentation only; no commands were run.
