---
id: computing-software.computer-graphics-engineering.opencv.opencv-numpy-interop-and-dtypes
name: opencv-numpy-interop-and-dtypes
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, cv2, python, numpy-interop, cv-dtypes, bgr-rgb, uint8-overflow, contiguous-array, saturate-cast, float32]
level: practitioner
status: docs-checked
description: "Avoid the cv2 + NumPy traps: BGR order, uint8 wraparound vs saturation, float ranges, non-contiguous slices rejected by cv2, shapes vs (x,y) order, and dtype conversions."
sources: ["https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html", "https://docs.opencv.org/4.x/d0/d86/tutorial_py_image_arithmetics.html", "https://numpy.org/doc/stable/reference/arrays.ndarray.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV and NumPy interop: dtypes and layout

**Goal:** Python image code that gives the same numbers as the C++ API and doesn't
silently corrupt images.

## 1. Arrays are images
`cv2.imread` returns `np.ndarray` shape `(H, W, 3)` dtype `uint8`, **BGR** order.
- Size args to OpenCV are `(width, height)`: `cv2.resize(img, (w, h))`; NumPy shape is
  `(h, w)`. Points are `(x, y)`; indexing is `img[y, x]`.
- Consumers that expect RGB (Matplotlib, PIL, many models) need a conversion: `rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`
  (or `img[..., ::-1]`, which is a view; see §3).

## 2. Saturation vs wraparound
```python
a = np.uint8([250]); b = np.uint8([10])
a + b            # -> [4]   NumPy wraps modulo 256
cv2.add(a, b)    # -> [[255]] OpenCV saturates
```
Use `cv2.add/subtract/addWeighted/convertScaleAbs` for pixel math, or convert to
`float32`/`int16` first. `np.clip(x, 0, 255).astype(np.uint8)` when going back.

## 3. Contiguity
The `Mat` docs say its data layout (described by `step`) is compatible with NumPy `ndarray`. Reversed or transposed
views (`img[:, ::-1]`, `img[..., ::-1]`, `arr.T`) are non-contiguous; make them contiguous before passing them on:
```python
img = np.ascontiguousarray(img[..., ::-1])
```
Always pass an explicit dtype when you create arrays, e.g. `np.zeros((h, w), np.uint8)`.

## 4. Float images
Convert float images back to `uint8` explicitly: `(f * 255).round().astype(np.uint8)`.

## 5. Drawing
Drawing functions annotate the array you pass; call `img.copy()` first if you need the original.

## Gotchas
- Grayscale images are 2-D `(H, W)`; code assuming `img.shape[2]` crashes — use
  `img.ndim`.

## Verify
- [ ] Round-trip test: imread → process → imwrite matches a C++ reference within ±1.
- [ ] Unit tests cover grayscale, BGRA and 16-bit inputs.
- [ ] No uint8 arithmetic via `+`/`-` operators on images in the codebase (grep).

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs (Python basic operations, image arithmetics, Mat class and the Mat basic image container tutorial) and the NumPy ndarray reference.
- Confirmed: BGR default for imread/cvtColor examples, OpenCV addition saturates while NumPy addition is modulo, `cv.add`, `cv.addWeighted`, `convertScaleAbs`, `shape` giving rows, cols, channels, Mat layout compatible with ndarray via steps.
- Removed (not on the fetched pages): supported-dtype list, int64 rejection, `(N, 1, 2)` contour shape rule, specific error strings, imwrite float behaviour, `IMREAD_UNCHANGED` uint16 claim, colour-argument error advice, split/merge copy claim, GIL and `cv2.setNumThreads` advice.

Method: documentation only; no commands were run.
