---
id: computing-software.computer-graphics-engineering.opencv.opencv-perspective-warp-document-rectification
name: opencv-perspective-warp-document-rectification
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, geometric-transforms, image-warping, warpperspective, perspective-transform, getperspectivetransform, document-scanner, corner-ordering, cv-perspectivetransform-points]
level: practitioner
status: verified
description: "Rectify documents, screens and planar targets in OpenCV: find the quad, order corners, compute output size, getPerspectiveTransform plus warpPerspective, and map points back."
sources: ["https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html", "https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html", "https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV perspective warp: document rectification

**Goal:** turn a photo of a page, whiteboard, monitor or label into a straight, fronto-
parallel image with the right aspect ratio.

## 1. Find the quadrilateral
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
edges = cv2.dilate(edges, None)                                  # close small gaps
cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in sorted(cnts, key=cv2.contourArea, reverse=True)[:5]:
    approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
    if len(approx) == 4 and cv2.isContourConvex(approx): quad = approx.reshape(4, 2); break
```

## 2. Order corners consistently
```python
def order(p):
    s = p.sum(1); d = np.diff(p, axis=1).ravel()
    return np.float32([p[np.argmin(s)], p[np.argmin(d)], p[np.argmax(s)], p[np.argmax(d)]])
    # top-left, top-right, bottom-right, bottom-left
src = order(quad.astype(np.float32))
```
Wrong ordering produces mirrored or twisted output — the most common bug. `order` returned TL,TR,BR,BL for all four
rotations of a test quad (checked).

## 3. Output size
```python
wA = np.linalg.norm(src[2] - src[3]); wB = np.linalg.norm(src[1] - src[0])
hA = np.linalg.norm(src[1] - src[2]); hB = np.linalg.norm(src[0] - src[3])
W, H = int(max(wA, wB)), int(max(hA, hB))
# known aspect (A4 = 1:1.414): force H = int(W * 1.414) for true proportions
dst = np.float32([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]])
```

## 4. Warp
```python
M = cv2.getPerspectiveTransform(src, dst)                        # exactly 4 points
out = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)
```
More than 4 noisy correspondences → `cv2.findHomography(src, dst, cv2.RANSAC, 3.0)`.
Map points (e.g. detected text boxes) back to the original:
`cv2.perspectiveTransform(pts.reshape(-1, 1, 2), np.linalg.inv(M))`.

## 5. Affine vs perspective
`warpAffine` (2x3, 3 points via `getAffineTransform`) preserves parallel lines: rotation,
scale, shear — use for scanned-but-skewed pages. Perspective (3x3, 4 points) handles camera
tilt.

## Gotchas
- Size argument is `(width, height)`.
- Detected quads at image borders (page cut off) — fall back to manual corner adjustment UI.
- Downscale for detection, then scale the corners back up and warp the full-res image.
- `INTER_AREA` does no area averaging in `warpPerspective`: the call is accepted but gave output identical to `INTER_LINEAR`
  (5.0.0, 4x shrink test); pre-scale with `resize(..., INTER_AREA)` first or use CUBIC/LINEAR.

## Verify
- [ ] Rectified page text lines are horizontal (Hough angle ≈ 0).
- [ ] Output aspect matches the known page format within 2%.
- [ ] Rotated input photos (90°, 180°) still produce upright output (corner order robust).
