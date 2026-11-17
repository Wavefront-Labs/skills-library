---
id: computing-software.computer-graphics-engineering.opencv.opencv-hdr-merge-and-exposure-fusion
name: opencv-hdr-merge-and-exposure-fusion
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-photo, exposure-fusion, mergemertens, mergedebevec, hdr-merge, hdr-imaging, tonemap, cv-tonemap]
level: practitioner
status: docs-checked
description: "Merge bracketed exposures in OpenCV: align with AlignMTB, calibrate response, MergeDebevec plus tonemap, or MergeMertens exposure fusion."
sources: ["https://docs.opencv.org/4.x/d3/db7/tutorial_hdr_imaging.html", "https://docs.opencv.org/4.x/d6/df5/group__photo__hdr.html", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# HDR merge and exposure fusion

## 1. Align
```python
cv2.createAlignMTB().process(imgs, imgs)     # median threshold bitmaps, exposure invariant
```
AlignMTB needs no exposure times or camera response, and fills new image regions with zeros. Defaults: `max_bits` 6,
`exclude_range` 4, `cut` true. Handheld brackets need alignment; tripod shots usually do not.

## 2. Radiance map (true HDR)
```python
times = np.array([1/30, 1/8, 1/2], np.float32)       # exposure times in seconds
resp = cv2.createCalibrateDebevec().process(imgs, times)
hdr = cv2.createMergeDebevec().process(imgs, times, resp)   # float32 linear radiance
cv2.imwrite("scene.hdr", hdr)                               # Radiance RGBE, or .exr
ldr = cv2.createTonemapReinhard(gamma=2.2).process(hdr)     # 0..1 float
out = np.clip(ldr * 255, 0, 255).astype(np.uint8)
```
Also `createTonemapDrago` and `createTonemapMantiuk`. `createCalibrateDebevec` defaults: `samples` 70, `lambda` 10. Use this
path when you need radiance values.

## 3. Exposure fusion (no HDR, no times)
```python
fused = cv2.createMergeMertens(contrast_weight=1, saturation_weight=1, exposure_weight=1).process(imgs)
out = np.clip(fused * 255, 0, 255).astype(np.uint8)
```
Pixels are weighted by contrast, saturation and well-exposedness, then combined with Laplacian pyramids. The result needs
no tonemapping and can be converted to 8-bit by multiplying by 255; the docs recommend gamma correction and/or linear tonemapping.
`createMergeMertens` defaults to `exposure_weight` 0.0 (the example passes 1 explicitly). Output is not radiance.

## Gotchas
- `MergeDebevec` input images must be 1-channel or 3-channel (CV_8U, CV_16U or CV_32F); give one exposure time per image, as float32 seconds. The response is a 256x1 matrix with the same number of channels as the images.
- Keep images the same size and in the same order as `times`.
- Moving objects can ghost; no deghosting is shown here.

## Verify
- [ ] No haloes at high-contrast edges; highlights and shadows both have detail.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp. Confirmed: createAlignMTB, createCalibrateDebevec, createMergeDebevec, createMergeMertens and tonemap signatures and defaults, AlignMTB behaviour, Debevec input types, Mertens output guidance. Removed the translation-only, 8-bit-only and RAW-versus-JPEG statements.
Method: documentation only; no commands were run.
