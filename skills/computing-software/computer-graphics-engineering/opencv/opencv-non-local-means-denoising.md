---
id: computing-software.computer-graphics-engineering.opencv.opencv-non-local-means-denoising
name: opencv-non-local-means-denoising
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-photo, computational-photography, fastnlmeansdenoising, image-denoising, non-local-means, fastnlmeansdenoisingcolored, fastnlmeansdenoisingmulti, low-light, noise-reduction]
level: practitioner
status: docs-checked
description: "Denoise images and video frames with OpenCV non-local means: h and template/search window tuning, colored and multi-frame variants, speed limits, and alternatives."
sources: ["https://docs.opencv.org/4.x/d1/d79/group__photo__denoise.html", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV non-local means denoising

**Goal:** reduce sensor noise (low light, high ISO, cheap cameras) while keeping edges and
texture, before thresholding, OCR, or for display.

## 1. Variants
```python
den = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)
den = cv2.fastNlMeansDenoisingColored(bgr, None, h=10, hColor=10,
                                      templateWindowSize=7, searchWindowSize=21)
# video: use temporal neighbours (odd window, middle frame index)
den = cv2.fastNlMeansDenoisingMulti(frames, imgToDenoiseIndex=2, temporalWindowSize=5, h=8)
```
- `Colored` takes an 8-bit 3-channel image, converts to CIELAB and denoises L with `h` and the colour components with
  `hColor` (the docs say a value of 10 suits most images).
- Multi-frame uses images from neighbouring frames in the sequence: `temporalWindowSize` is the number of surrounding
  images used and must be odd, frames from `imgToDenoiseIndex - temporalWindowSize / 2` to `+ temporalWindowSize / 2` are used,
  and all images must have the same type and size.

## 2. Tuning h
- `h` regulates filter strength: a big value removes noise but also image detail, a small value keeps detail and some noise.
  The grayscale function defaults to `h` 3; tune it visually on a crop with flat and textured content.
- `templateWindowSize` 7 and `searchWindowSize` 21 are the recommended values and must be odd; the docs say a larger
  `searchWindowSize` increases the denoising time linearly.
- The algorithm assumes Gaussian white noise.

## 3. Speed
Time it at your production resolution. Options: denoise at reduced resolution when the output is downscaled anyway, lower
`searchWindowSize`, or use another filter such as `cv2.bilateralFilter` for real-time video.

## 4. Input types
`fastNlMeansDenoising` takes 8-bit 1- to 4-channel images; the overload with an `h` array and `normType` also takes 16-bit
images, but only with `NORM_L1`. `fastNlMeansDenoisingColored` takes 8-bit 3-channel images.

## Gotchas
- The algorithm assumes Gaussian white noise; compression artefacts do not fit that model.
- Validate on the downstream task metric, not only on appearance.

## Verify
- [ ] PSNR/SSIM vs a clean reference (or multi-frame average) improves on test images.
- [ ] Visual check on textured crops for over-smoothing.
- [ ] Runtime within budget at production resolution.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp. Confirmed: fastNlMeansDenoising, Colored and Multi signatures, input types, recommended template 7 and search 21 windows, linear cost in search window, odd temporal window, h and hColor guidance, Gaussian noise assumption. Removed the unconfirmed timing, CUDA and h-equals-sigma statements.
Method: documentation only; no commands were run.
