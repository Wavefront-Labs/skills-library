---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.noise-power-spectrum
name: noise-power-spectrum
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [noise-power-spectrum, digital-radiography, dqe, nnps, wiener-spectrum, flat-field-images, detector-noise, ct-noise-texture]
level: advanced
status: gated
description: "Compute normalised noise power spectrum from flat-field images: linearisation, ROI selection, detrending, 2D FFT averaging, units, sampling requirements and use in DQE."
sources: ["IEC 62220-1-1:2015 (NNPS determination for DQE; https://webstore.iec.ch/en/publication/21937)", "ICRU Report 54 Medical Imaging: The Assessment of Image Quality"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Noise power spectrum (NPS)

**Goal:** describe noise as a function of spatial frequency, for detector characterisation, DQE and CT noise texture.

## Definition
NPS(u, v) = (pixel area / (Nx Ny)) x average over ROIs of |FFT(ROI minus its mean or trend)|^2, with the units of (signal^2 x area). The **normalised NPS (NNPS)** divides by the square of the mean signal in the linear (kerma-proportional) domain.

## Procedure (radiography)
1. Acquire several flat-field images at a defined exposure in the linear region of the detector; use the same beam and processing as the MTF and DQE measurements.
2. Linearise the pixel values so the signal is proportional to incident kerma.
3. Choose **ROIs** (commonly 128 x 128 or 256 x 256 pixels (gated: unconfirmed, source is paywalled or blocked)) overlapping by about 50%, covering the central region, avoiding the edges and heel-effect gradient.
4. **Detrend** each ROI by subtracting a 2D low-order polynomial (second order) to remove low-frequency shading.
5. Apply the 2D FFT (windowing is generally not used in the standard method), compute squared magnitude and average across ROIs; the standard requires enough area (for example at least 4 million pixels total (gated: unconfirmed, source is paywalled or blocked)) for statistical stability.
6. **Reduce to 1D** by averaging along bands around the axes (excluding the axes themselves to avoid streak artefacts) or radial averaging for isotropic noise.
7. Normalise, and use with the MTF and fluence to compute DQE.

## CT noise texture
Compute the 2D NPS in uniform water phantom slices (axial); the peak frequency and shape characterise the reconstruction kernel (see reconstruction-kernels), and the integral of the NPS equals the pixel variance.

## Gotchas
- Fixed-pattern noise (gain structure) dominates at high exposures if the flat field correction is imperfect.
- Lag, ghosting or non-stationary backgrounds bias estimates.
- Sampling: the highest frequency is Nyquist; aliasing folds noise into lower frequencies.

## Verify
- [ ] NNPS at low frequency scales inversely with exposure for a quantum-limited detector.
- [ ] Integrating the NPS reproduces the pixel variance within a few percent.
- [ ] Results repeatable across independent image sets.
