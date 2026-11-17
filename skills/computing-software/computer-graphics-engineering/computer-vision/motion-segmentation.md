---
id: computing-software.computer-graphics-engineering.computer-vision.motion-segmentation
name: motion-segmentation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, motion-estimation, motion-segmentation, layered-motion, optical-flow, ego-motion-compensation, moving-object-detection]
level: sme
status: verified
description: "Segment independently moving objects: ego-motion compensation via homography/epipolar residuals on optical flow, layered motion models, and learned video segmentation."
sources: ["https://szeliski.org/Book/", "https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html", "https://arxiv.org/abs/2104.07658"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Motion segmentation

## 1. Static camera
Background subtraction (MOG2/KNN) is enough; see the OpenCV background subtraction skill.

## 2. Moving camera: compensate ego-motion, then find residual motion
1. Dense flow between frames (RAFT, or `cv2.DISOpticalFlow` for speed).
2. Fit the dominant motion robustly:
   - Distant/planar scenes or pure rotation: homography via `cv2.findHomography(p0, p1, cv2.USAC_MAGSAC, 2.0)`
     on a grid of flow samples.
   - General 3D scene: fundamental/essential matrix; residual = distance of the flow endpoint to its epipolar
     line (Sampson distance). Static points with parallax still lie on their epipolar line.
3. Pixels with residual above a threshold (2-3 px) are independently moving. Clean with morphology and
   connected components; enforce temporal consistency over 3-5 frames.
```python
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
flow = dis.calc(gray0, gray1, None)                       # h x w x 2, float32
h, w = gray0.shape
ys, xs = np.mgrid[0:h:8, 0:w:8]
pts0 = np.stack([xs.ravel(), ys.ravel()], 1).astype(np.float32)
pts1 = pts0 + flow[ys.ravel(), xs.ravel()]
H, inl = cv2.findHomography(pts0, pts1, cv2.USAC_MAGSAC, 2.0)
grid = np.stack(np.meshgrid(np.arange(w), np.arange(h)), -1).astype(np.float32)
pred = cv2.perspectiveTransform(grid.reshape(-1, 1, 2), H).reshape(h, w, 2)
res = np.linalg.norm((grid + flow) - pred, axis=2)
moving = (res > 2.5).astype(np.uint8)
```
On a synthetic pair (textured plane under a homography plus one 40 px square moving 10 px) this flagged 1676 pixels, all inside the moving square's neighbourhood, with 1175 of 1200 grid samples as homography inliers.

## 3. Layered motion (multiple motions)
Fit several parametric models (affine/homography) with sequential RANSAC or EM: assign each pixel to the
best-fitting layer, refit, repeat; regularise assignments with a graph cut / MRF so layers are spatially
coherent. Classic Wang-Adelson layers; still useful for a few rigid movers.

## 4. Learned
Video object segmentation and motion-grouping networks (e.g. SAM 2 with prompts from the residual mask)
give crisp masks; use the geometric residual as the prompt/seed, the network for boundaries.

## Gotchas
- Homography residuals flag static objects with parallax (near poles, trees) as moving; use epipolar residual
  or depth when the scene is not planar.
- Objects moving along the epipolar line are invisible to epipolar residuals; add depth consistency checks.
- Flow errors at occlusion boundaries: use forward-backward consistency to mask them.

## Verify
- [ ] On a sequence with labelled movers, report IoU of the moving mask; parked cars and buildings stay
  unflagged while the camera moves.

## Checked
OpenCV 5.0.0, NumPy 2.5.4.
- Run: `DISOpticalFlow_create` + `calc`, `findHomography(..., cv2.USAC_MAGSAC, 2.0)`, `perspectiveTransform` residual threshold 2.5 on the synthetic pair described above (the original snippet lacked the flow, grid and sample definitions, now added).
- Fetched: arXiv API title for 2104.07658 (Self-supervised Video Object Segmentation by Motion Grouping).
