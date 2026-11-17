---
id: computing-software.computer-graphics-engineering.computer-vision.sensor-noise-models
name: sensor-noise-models
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, sensor-noise, photon-transfer-curve, poisson-gaussian, emva-1288, read-noise]
level: advanced
status: gated
description: "Model image sensor noise: shot (Poisson), read, dark current, PRNU/DSNU and quantisation; heteroscedastic Poisson-Gaussian fits, photon transfer curves, noise-aware denoising."
sources: ["https://www.emva.org/standards-technology/emva-1288/", "https://doi.org/10.1109/TIP.2008.2001399", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensor noise models

## Components (per pixel, linear raw domain)
- **Shot noise**: Poisson in photo-electrons, variance = signal. Dominates in bright regions.
- **Read noise**: Gaussian, signal-independent (amplifier, ADC). Dominates in shadows.
- **Dark current**: grows with exposure time and roughly doubles every 6 to 8 C (gated: unconfirmed, source is paywalled or blocked).
- **Fixed pattern**: DSNU (offset non-uniformity), PRNU (gain non-uniformity, about 0.5 to 2
  percent (gated: unconfirmed, source is paywalled or blocked)), hot pixels. Not random over time: calibrate and subtract.
- **Quantisation**: variance LSB^2/12.

## Poisson-Gaussian model
In raw digital numbers (after black-level subtraction): `var(y) = a * E[y] + b`, where `a` is the
system gain (DN per electron) and `b` the read-noise variance. Fit `a, b` from flat patches (simulated check: true a = 0.5, b = 4 gave a = 0.499, b = 4.46 over 40 levels
with 200 frames each; one brightness level alone returned slope 0.04 and intercept 463):
```python
# frames: N raw frames of a static scene with a RANGE of brightness (gradient, step wedge or
# grey-card chart), black level subtracted; a uniformly bright scene gives one (mean, var) cluster
mean = frames.mean(0); var = frames.var(0, ddof=1)
a, b = np.polyfit(mean.ravel(), var.ravel(), 1)
```
Or from a single image (Foi et al.): local mean/variance in flat regions after wavelet
decomposition. Repeat per ISO/gain setting: `a` scales with analogue gain.

## Photon transfer curve (EMVA 1288)
Log-log plot of temporal noise vs mean signal (simulated shot-noise slope 0.497): slope 0 (read noise floor), slope 0.5 (shot noise),
then saturation. Gives gain, read noise in electrons, full-well capacity, dynamic range.

## Using the model
- Variance-stabilise with the generalised Anscombe transform (`2/a * sqrt(a z + 3/8 a^2 + b)`; checked: output std 1.0 at
  low, mid and high intensity where raw std went 3.8, 19.9, 38.5), denoise with a Gaussian denoiser
  (BM3D), invert: standard practice for raw denoising.
- Synthesize realistic training noise for learned denoisers on raw data (not additive Gaussian on
  sRGB, which is wrong after demosaic, gamma and JPEG).
- Weight observations by inverse variance in HDR merging and photometric fits.

## Gotchas
- After demosaic, tone curve, sharpening and JPEG the noise is spatially correlated and
  signal-dependent in complicated ways; fit models on raw whenever possible.
- Clipped pixels have reduced variance: exclude near-saturation samples from fits.

## Verify
Predicted variance vs measured on held-out flat patches across the intensity range should agree
within about 10 percent.
