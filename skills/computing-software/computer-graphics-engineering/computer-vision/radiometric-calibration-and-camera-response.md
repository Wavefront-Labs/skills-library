---
id: computing-software.computer-graphics-engineering.computer-vision.radiometric-calibration-and-camera-response
name: radiometric-calibration-and-camera-response
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, radiometric-calibration, camera-response, crf, vignetting, flat-field-correction, dark-frame, linearization, calibratedebevec]
level: advanced
status: gated
description: "Make pixel values proportional to scene radiance: recover the camera response curve, flat-field and vignetting correction, dark frames."
sources: ["https://szeliski.org/Book/", "https://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf", "https://docs.opencv.org/4.x/d2/df0/tutorial_py_hdr.html", "https://www.emva.org/standards-technology/emva-1288/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Radiometric calibration and camera response

**Goal:** intensities you can compare across images, cameras and time — for photometric
stereo, HDR merging, colour measurement, direct-method SLAM and inspection.

## 1. Lock the camera
Auto exposure, auto gain, auto white balance, and in-camera "enhancement" (tone curves,
sharpening, HDR modes) all change values frame to frame. Set manual exposure, fixed gain
(ISO), fixed WB, and disable gamma/tone mapping where possible (use RAW or linear output modes
on machine-vision cameras, `Gamma=1`, `BlackLevel` known).

## 2. Camera response function (CRF)
Consumer outputs are non-linear (sRGB-like + tone curve). Recover the inverse CRF from a
static scene shot at several known exposures:
```python
times = np.array([1/30, 1/8, 1/2, 2.0], np.float32)
crf = cv2.createCalibrateDebevec().process(images, times)     # 256x1x3 response
hdr = cv2.createMergeDebevec().process(images, times, crf)    # linear radiance map
```
Robertson's method (`createCalibrateRobertson`) is an alternative. Both ran in OpenCV 5.0.0 and
returned `(256, 1, 3)` float32 responses. Tested with a synthetic gamma-2.2 camera and four exposures
(1/30 to 2 s): the merged radiance correlated with the true log radiance at 0.99997. Apply the inverse CRF via a
LUT to linearise future images from that camera/settings. Machine-vision cameras in linear
mode skip this step (verify linearity with an exposure sweep: mean value vs exposure time
should be a straight line until saturation).

## 3. Dark frame and black level
Capture frames with the lens capped at the operating exposure/gain/temperature; average →
dark frame (fixed-pattern noise, hot pixels). Subtract before any other correction.

## 4. Flat-field (vignetting and pixel response non-uniformity)
Image a uniformly lit target (integrating sphere, diffuser panel, overcast sky through
diffuser) slightly defocused; average many frames; normalise:
```python
flat = (flat_avg - dark) / np.mean(flat_avg - dark)
corrected = (raw - dark) / np.clip(flat, 1e-3, None)
```
(synthetic 20% vignette: relative std 5.2% before, 1e-16 after).
Vignetting depends on aperture and zoom — one flat per lens setting.

## 5. Standards
EMVA 1288 (also published as ISO 24942) defines measurement of sensitivity, noise, linearity and dark
current (gated: unconfirmed, source is paywalled or blocked) — confirm the scope in the current standard text, and use its datasheet values to choose cameras for measurement tasks.

## Gotchas
- Saturated or near-zero pixels carry no radiometric information; mask them (weights in HDR merge).
- JPEG compression and chroma subsampling break per-pixel radiometry — use RAW/uncompressed.
- Temperature changes dark current and sometimes gain; recalibrate or control temperature.

## Verify
- [ ] Exposure sweep shows linear response after correction (R² > 0.999 below saturation).
- [ ] Flat-field corrected image of the uniform target is flat within ±1–2%.
- [ ] Camera settings stored alongside calibration data.
