---
id: computing-software.computer-graphics-engineering.computer-vision.superpoint-lightglue-feature-matching
name: superpoint-lightglue-feature-matching
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, feature-matching, superpoint, lightglue, disk, learned-features, hloc]
level: sme
status: draft
description: "Match images with learned features: SuperPoint/DISK/ALIKED keypoints with LightGlue, hloc integration with COLMAP, and when classical SIFT still wins."
sources: ["https://github.com/cvg/LightGlue", "https://arxiv.org/abs/2306.13643", "https://arxiv.org/abs/1712.07629", "https://github.com/cvg/Hierarchical-Localization"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Learned features and matchers: SuperPoint and LightGlue

## 1. Pair matching
```python
from lightglue import LightGlue, SuperPoint
from lightglue.utils import load_image, rbd
extractor = SuperPoint(max_num_keypoints=2048).eval().cuda()
matcher = LightGlue(features="superpoint").eval().cuda()     # also "disk", "aliked", "sift"
f0 = extractor.extract(load_image("a.jpg").cuda())
f1 = extractor.extract(load_image("b.jpg").cuda())
m = matcher({"image0": f0, "image1": f1})
f0, f1, m = [rbd(x) for x in (f0, f1, m)]                   # remove batch dim
idx = m["matches"]                                           # (K, 2)
p0, p1 = f0["keypoints"][idx[:, 0]], f1["keypoints"][idx[:, 1]]
```
Then geometric verification as usual: `cv2.findFundamentalMat(p0, p1, cv2.USAC_MAGSAC, 1.0)` or essential
matrix with intrinsics.

## 2. Choosing
| Case | Pick |
|---|---|
| Wide baseline, day/night, viewpoint change | SuperPoint or ALIKED + LightGlue |
| Speed critical | LightGlue adaptive depth/width (default on) prunes; reduce keypoints to 1024 |
| Easy video sequences, licensing constraints | SIFT/ORB + ratio test (classic) |
| Textureless or extreme change | Dense matchers (LoFTR, RoMa) |

## 3. SfM with learned features
hloc runs extraction (SuperPoint), pair selection (NetVLAD retrieval or sequential), matching (LightGlue), then
imports into COLMAP for triangulation and bundle adjustment.

## Gotchas
- SuperPoint's original weights are non-commercial (Magic Leap licence); DISK and ALIKED are permissive. Check
  before shipping.
- Feature extractor and LightGlue weights must correspond (`features=` argument).
- Resize consistently (e.g. long side 1024); keypoints are returned in the input image's pixel coordinates.
- Rotation beyond ~45 deg hurts SuperPoint; add rotation augmentation or test rotated copies.

## Verify
- [ ] Inlier count and inlier ratio after MAGSAC compared against SIFT on your hardest pairs; pose AUC on a
  small labelled set if available.
