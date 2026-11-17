---
id: computing-software.computer-graphics-engineering.opencv.opencv-kmeans-colour-quantization
name: opencv-kmeans-colour-quantization
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, kmeans-quantization, cv-kmeans, dominant-colours]
level: practitioner
status: verified
description: "Quantise image colours and extract dominant colours with cv::kmeans: data layout, criteria, KMEANS_PP_CENTERS, attempts, Lab clustering and subsampling for speed."
sources: ["https://docs.opencv.org/4.x/d5/d38/group__core__cluster.html#ga9a34dc06c6ec9460e90860f15bcd2f88", "https://docs.opencv.org/4.x/d1/d5c/tutorial_py_kmeans_opencv.html", "https://docs.opencv.org/4.x/d5/d38/group__core__cluster.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k-means colour quantisation

## Basic
```python
Z = img.reshape(-1, 3).astype(np.float32)                         # N x 3 samples, float32 required
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
K = 8
compact, labels, centers = cv2.kmeans(Z, K, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
quant = centers.astype(np.uint8)[labels.ravel()].reshape(img.shape)
```
- `attempts=3` runs k-means 3 times and keeps the best (lowest compactness); on random 64x64 data attempts=3
  gave 16577044 vs 16581670 for attempts=1. `labels` is `int32` of shape `(N, 1)`, `centers` is float32 `(K, 3)`; a uint8
  samples array raises an error.
- `KMEANS_PP_CENTERS` (k-means++) initialisation converges better than random.

## Cluster in a perceptual space
Euclidean distance in BGR doesn't match perceived colour difference. Convert to Lab (float) first,
cluster, convert centres back:
```python
lab = cv2.cvtColor(img.astype(np.float32) / 255, cv2.COLOR_BGR2Lab).reshape(-1, 3)
_, labels, centers = cv2.kmeans(lab, K, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
```
Optionally append scaled (x, y) coordinates to each sample to get spatially coherent
segments (a crude superpixel; use `cv2.ximgproc.createSuperpixelSLIC` for the real thing).

## Dominant colours / palettes
Cluster a subsample (e.g. 20k random pixels) for speed, then count label frequency:
```python
idx = np.random.default_rng(0).choice(len(Z), size=min(20000, len(Z)), replace=False)
_, lab_s, cen = cv2.kmeans(Z[idx], 5, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
share = np.bincount(lab_s.ravel(), minlength=5) / len(idx)
palette = sorted(zip(share, cen.astype(int).tolist()), reverse=True)
```
Mask out background (alpha or segmentation) before clustering product images.

## Choosing K
Elbow on `compactness` vs K, or fix K by use case (posterisation 4-16, palette 5-8). For
deterministic results set `cv2.setRNGSeed(0)` before each call (two seeded runs returned identical compactness).

## Gotchas
- Full 4K images = 8M samples: slow; subsample to fit centres, then assign all pixels with a
  nearest-centre lookup (vectorised NumPy or `cv2.ml` KNearest).
- Labels are arbitrary; sort clusters (by share or luminance) for stable output.

## Verify
- [ ] Quantised image PSNR reasonable for chosen K; palette stable across runs with fixed seed.
