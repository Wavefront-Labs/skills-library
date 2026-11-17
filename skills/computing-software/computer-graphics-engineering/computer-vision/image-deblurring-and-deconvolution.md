---
id: computing-software.computer-graphics-engineering.computer-vision.image-deblurring-and-deconvolution
name: image-deblurring-and-deconvolution
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, deblurring, deconvolution, wiener-filter, richardson-lucy, point-spread-function]
level: sme
status: gated
description: "Remove blur from images: model the PSF, non-blind Wiener and Richardson-Lucy deconvolution, blind kernel estimation, and learned deblurring, with ringing control."
sources: ["https://szeliski.org/Book/", "https://scikit-image.org/docs/stable/api/skimage.restoration.html", "https://docs.opencv.org/4.x/de/d3c/tutorial_out_of_focus_deblur_filter.html", "https://github.com/swz30/Restormer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deblurring and deconvolution

## 1. Model
`observed = image (*) PSF + noise`. Know the PSF first:
- Defocus: disc of radius r.
- Linear motion: line segment of length L at angle theta.
- Optical (lens/microscope/telescope): measured from a point source or slanted edge.
Work on linear data (undo gamma/sRGB first), per channel.

## 2. Non-blind (PSF known)
```python
from skimage import restoration
img = img_linear.astype(np.float64)                    # 0..1
wien = restoration.wiener(img, psf, balance=0.01)      # balance: regularisation weight, tune it
rl = restoration.richardson_lucy(img, psf, num_iter=30)
```
- **Wiener**: frequency-domain `G* / (|G|^2 + K)`; K trades sharpness for noise. Fast, prone to ringing.
  In scikit-image 0.26 `balance` is not the noise-to-signal ratio: on the camera test image
  (11 px horizontal motion PSF, noise sigma 0.001) interior PSNR was 23.6 dB blurred, 15.9 at
  `balance=0.001` (about the true noise-to-signal ratio), 23.5 at 0.01, 26.4 at 0.1 and 24.7 at 1,
  so sweep it on a synthetic copy of your data.
- **Richardson-Lucy**: iterative, keeps positivity, good for Poisson noise (astronomy, microscopy). Stop
  early; more iterations amplify noise (interior PSNR with noise sigma 0.01: 25.2 dB at 5 iterations,
  27.1 at 30, 24.5 at 100; with sigma 0.001 it kept rising to 29.3 at 100).
- Total-variation or hyper-Laplacian priors (Krishnan-Fergus) reduce ringing further (gated: unconfirmed, source is paywalled or blocked); not run here.

## 3. Ringing at borders
FFT deconvolution assumes periodic images; pad by reflection and taper edges (`cv2.copyMakeBorder` +
window) before transforming, crop afterwards. Measured: the 8-pixel border strip had 10x the
mean squared error of the interior (0.031 against 0.0032) with no padding, and 0.027 with a
32-pixel reflect pad.

## 4. Blind (PSF unknown)
- Estimate the kernel from strong edges with a sparse-gradient prior in a coarse-to-fine pyramid (Fergus 2006,
  Levin, Pan dark-channel; literature pointers, not run here), then non-blind deconvolve.
- Spatially varying blur (camera shake with rotation, depth-dependent defocus) breaks a single-kernel model:
  split into tiles or use learned methods.

## 5. Learned
Restormer, NAFNet and similar trained on GoPro/RealBlur generalise to real motion blur (gated: unconfirmed, source is paywalled or blocked); not run here (no GPU); they may hallucinate
texture. Use classical methods where measurement fidelity matters (forensics, science).

## Gotchas
- Saturated highlights violate the linear model: mask them or they cause strong ringing.
- JPEG artefacts get amplified; deconvolve RAW or high-quality sources.
- A slightly wrong PSF size produces worse results than no deconvolution; sweep r or L and compare
  (true length 11 px, Wiener `balance=0.01`: a 15 px PSF gave 13.9 dB and a 21 px PSF 7.1 dB
  against 23.3 dB for the undeconvolved image; a 7 px PSF gave 21.6).

## Verify
- [ ] Synthetic test: blur a sharp image with a known PSF plus noise, recover, report PSNR/SSIM; on real
  images, slanted-edge MTF improves without visible ringing.
