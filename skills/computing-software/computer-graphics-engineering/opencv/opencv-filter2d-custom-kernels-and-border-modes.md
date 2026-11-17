---
id: computing-software.computer-graphics-engineering.opencv.opencv-filter2d-custom-kernels-and-border-modes
name: opencv-filter2d-custom-kernels-and-border-modes
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, filter2d, border-types, convolution, kernel, imgproc]
level: practitioner
status: verified
description: "Apply custom convolution kernels in OpenCV with filter2D: ddepth choice, anchor, correlation vs convolution, BORDER_* modes and the overflow traps that silently clip results."
sources: ["https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html", "https://docs.opencv.org/4.x/d4/dbd/tutorial_filter_2d.html", "https://docs.opencv.org/4.x/d2/de8/group__core__array.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filter2D: custom kernels and border modes

`cv2.filter2D(src, ddepth, kernel, anchor=(-1,-1), delta=0, borderType=cv2.BORDER_DEFAULT)`

## 1. It is correlation, not convolution
filter2D does **not** flip the kernel. For symmetric kernels it does not matter; for asymmetric
ones (derivatives, motion blur direction) flip first to get true convolution:
```python
k = np.array([[-1, 0, 1]], np.float32)
conv = cv2.filter2D(img, cv2.CV_32F, cv2.flip(k, -1), anchor=(k.shape[1]-1-1, 0))
```
When flipping, mirror the anchor too: `(kcols - anchor.x - 1, krows - anchor.y - 1)`.

## 2. Pick ddepth deliberately
- `ddepth=-1` keeps the input depth. On uint8 a derivative kernel saturates negatives to 0 and
  values above 255 to 255: half of every edge disappears.
- Use `cv2.CV_32F` (or `CV_16S` for integer kernels) for anything that can go negative, then
  `cv2.convertScaleAbs` or normalise for display.
- Normalise blur kernels so they sum to 1 (`k /= k.sum()`), otherwise brightness drifts.

## 3. Border modes
| Mode | Pads `abcdefgh` as | Use |
|---|---|---|
| `BORDER_REFLECT_101` (=`BORDER_DEFAULT`) | `gfedcb|abcdefgh|gfedcba` | Default, no edge seam |
| `BORDER_REFLECT` | `fedcba|abcdefgh|hgfedcb` | Duplicates the edge pixel |
| `BORDER_REPLICATE` | `aaaaaa|abcdefgh|hhhhhhh` | Depth maps, masks |
| `BORDER_CONSTANT` | `000000|abcdefgh|0000000` | Zero padding (darkens borders on blur) |
| `BORDER_WRAP` | `cdefgh|abcdefgh|abcdefg` | Periodic signals, FFT-consistent |
`BORDER_WRAP` is rejected by `filter2D`, `sepFilter2D` and `GaussianBlur` (assertion `columnBorderType != BORDER_WRAP`,
OpenCV 5.0.0) while `blur` accepts it; for a periodic filter pad with `copyMakeBorder(..., BORDER_WRAP)`, filter, and
crop. `BORDER_ISOLATED` stops ROI filtering from reading pixels outside the ROI.

## 4. Performance
- Kernels of about 11x11 or larger switch to a DFT-based path internally (OpenCV header text); on a 1200x1200
  float32 image a 15x15 kernel took 11 ms.
- If the kernel is rank 1 (outer product of two vectors) use `sepFilter2D` instead: O(k) not O(k^2).
  Check with `np.linalg.matrix_rank(k) == 1` (a 15x15 Hann outer product: `sepFilter2D` 1.8 ms vs `filter2D` 11.4 ms, max difference 6e-6).

## Verify
- Filter an impulse image (single 1 at the centre): the output must equal the kernel (flipped
  for filter2D vs your convolution definition).
- Compare against `scipy.ndimage.correlate(img, k, mode='mirror')` on float input.
