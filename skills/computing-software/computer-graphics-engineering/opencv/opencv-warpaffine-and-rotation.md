---
id: computing-software.computer-graphics-engineering.opencv.opencv-warpaffine-and-rotation
name: opencv-warpaffine-and-rotation
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-geometric-transforms, warpaffine, getrotationmatrix2d, image-rotation, affine-transform, getaffinetransform, cv-rotate]
level: practitioner
status: verified
description: "Rotate, scale and shift images with cv::warpAffine and getRotationMatrix2D, without cropping corners, and map points with the same matrix."
sources: ["https://docs.opencv.org/4.x/d4/d61/tutorial_warp_affine.html", "https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# warpAffine and rotation

## 1. Rotate about the centre
```python
h, w = img.shape[:2]
M = cv2.getRotationMatrix2D(((w - 1) / 2, (h - 1) / 2), angle_deg, 1.0)   # positive = counter-clockwise
out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
```

## 2. Rotate without cropping
```python
c, s = abs(M[0, 0]), abs(M[0, 1])
nw, nh = int(h * s + w * c), int(h * c + w * s)
M[0, 2] += nw / 2 - w / 2
M[1, 2] += nh / 2 - h / 2
out = cv2.warpAffine(img, M, (nw, nh))
```
The no-crop shift `nw/2 - w/2` is unchanged by the centre convention (a 60x40 image at 30 degrees: 71x64 canvas, 2397 of 2400 pixels kept).
For exact 90-degree steps use `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)`: lossless and faster.

## 3. Affine from three point pairs, and mapping points
```python
M = cv2.getAffineTransform(src3.astype(np.float32), dst3.astype(np.float32))
pts2 = cv2.transform(pts.reshape(-1, 1, 2), M)       # same matrix for keypoints/boxes
Minv = cv2.invertAffineTransform(M)
```
For more than three noisy pairs use `cv2.estimateAffinePartial2D` (rotation+scale+shift, RANSAC)
or `estimateAffine2D` (full affine).

## Gotchas
- `dsize` is (width, height); NumPy shape is (height, width).
- `WARP_INVERSE_MAP` flag means M maps dst to src; useful when you already have the inverse.
- Masks and label images need `INTER_NEAREST` to avoid invented label values.
- Pixel-centre convention: OpenCV treats pixel centres at integer coordinates; the centre is
  ((w-1)/2, (h-1)/2) for symmetric rotation. A 180-degree `warpAffine` (INTER_NEAREST) about (w/2, h/2) differed from
  `img[::-1, ::-1]` in 2392 pixels of a 60x40 image, about ((w-1)/2, (h-1)/2) it was identical.

## Verify
- [ ] Transformed keypoints land on the warped features (draw both).
