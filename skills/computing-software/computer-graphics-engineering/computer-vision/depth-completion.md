---
id: computing-software.computer-graphics-engineering.computer-vision.depth-completion
name: depth-completion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, depth-completion, sparse-to-dense, lidar-depth, rgb-guided, kitti]
level: advanced
status: verified
description: "Densify sparse depth (lidar, SfM points, ToF holes) with RGB guidance: classical IP-Basic morphology, learned completion networks, input encoding, KITTI-style metrics."
sources: ["https://github.com/kujason/ip_basic", "https://www.cvlibs.net/datasets/kitti/eval_depth.php?benchmark=depth_completion", "https://arxiv.org/abs/1709.07492", "https://arxiv.org/abs/1802.00036"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth completion

Task: given an RGB image and sparse depth (projected lidar covers only a small fraction of pixels; SfM points;
ToF with holes), predict dense depth.

## Classical baseline (IP-Basic)
Invert depth (so near is large), dilate with a custom diamond kernel, morphological close, fill
remaining holes with larger dilations, median and bilateral blur, invert back. No training. The IP-Basic README
lists 90 FPS (0.011 s) on one CPU core for KITTI and, among unguided methods in its table, the best RMSE
(1288 mm vs 1853 mm for Nadaraya-Watson). The 5x5 dilation kernel is a diamond (not OpenCV's cross).
Runnable version of the fast variant (it took 8 to 12 ms on a 352x1216 synthetic frame here):
```python
DIAMOND5 = np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]], np.uint8)
d = depth.astype(np.float32).copy(); valid = d > 0.1
d[valid] = 100.0 - d[valid]                               # invert (max_depth = 100)
d = cv2.dilate(d, DIAMOND5)
d = cv2.morphologyEx(d, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
empty = d < 0.1; d[empty] = cv2.dilate(d, np.ones((7, 7), np.uint8))[empty]   # fill holes
d = cv2.medianBlur(d, 5); d = cv2.bilateralFilter(d, 5, 1.5, 2.0)
valid = d > 0.1; d[valid] = 100.0 - d[valid]              # invert back
```

## Learned
- Inputs: RGB + sparse depth + validity mask. Normalising sparse depth (log or divide by max range)
  helps.
- Architectures: early/late fusion encoders, spatial propagation (CSPN, NLSPN), guided convolutions.
  Monocular depth foundation models + sparse metric anchors (scale/shift fitting or prompt-based
  models) generalise better across sensors.
- Train with loss only on pixels with ground truth (semi-dense accumulated lidar).

## Sparse pattern matters
Models trained on 64-beam KITTI patterns fail on 16-beam or different mounting. Augment by
randomly dropping points/beams.

## Metrics
RMSE and MAE (mm), iRMSE and iMAE (1/km: error of the inverse depth), as defined on the KITTI depth
completion benchmark page; evaluated only where ground truth exists.

## Verify
Hold out a fraction of the sparse points as test points (not given as input) and measure error on
them.

## Checked
OpenCV 5.0.0, NumPy 2.5.4.
- Run: the corrected snippet and the upstream `fill_in_fast` (depth_map_utils.py from kujason/ip_basic) on a synthetic 5 percent sparse 352x1216 depth map: RMSE 0.28 (diamond) vs 0.30 (cross) vs 0.31 (upstream with extrapolation), coverage 99.8 percent, 8-12 ms per frame; printed the OpenCV cross kernel to confirm it is not a diamond.
- Fetched: ip_basic README (90 FPS, 0.011 s, table) and source (max_depth 100, diamond kernel, 7x7 fill, median 5, bilateral 5/1.5/2.0), KITTI depth completion page (metric names and units).
