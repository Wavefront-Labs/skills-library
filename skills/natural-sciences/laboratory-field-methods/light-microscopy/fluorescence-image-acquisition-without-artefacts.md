---
id: natural-sciences.laboratory-field-methods.light-microscopy.fluorescence-image-acquisition-without-artefacts
name: fluorescence-image-acquisition-without-artefacts
category: natural-sciences
field: laboratory-field-methods
product: light-microscopy
tags: [light-microscopy, fluorescence-microscopy, widefield, confocal, laser-scanning-confocal, kohler-illumination, objective-choice, numerical-aperture, immersion-oil, coverslip-thickness, nyquist-sampling, pinhole, airy-unit, exposure-time, detector-gain, saturation, histogram, lut, bleed-through, crosstalk, sequential-scanning, photobleaching, phototoxicity, single-stain-controls, secondary-only-control, flat-field, 16-bit, image-quantification]
level: practitioner
status: draft
description: "Acquire quantifiable fluorescence images: Köhler setup, NA and #1.5 coverslips, Nyquist sampling, no saturation, bleed-through checks, and locked settings across conditions."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fluorescence image acquisition without artefacts

**Goal:** images that faithfully represent the sample — no saturated pixels, no
channel bleed-through, enough resolution — acquired identically across conditions so
intensity comparisons mean something.

## 1. Set up the optics
- **Köhler illumination** for transmitted light (brightfield/phase/DIC): focus the
  sample, close the field diaphragm, focus its edges with the condenser, centre it, open
  until just outside the field of view; set the aperture diaphragm to ~70–80 % of the
  objective's NA. This gives even illumination and correct contrast.
- **Objective:** resolution and brightness scale with **numerical aperture (NA)**, not
  magnification. Lateral resolution ≈ 0.61 λ / NA (e.g. ~0.22 µm at 510 nm with NA 1.4).
  Brightness in epifluorescence scales roughly with NA⁴/M², so a 40×/1.3 oil can be
  brighter than a 63×/1.4 for the same field.
- **Coverslips:** most high-NA objectives are corrected for **#1.5 (0.17 mm)**. Wrong
  thickness causes spherical aberration (dim, blurred, asymmetric in z). Use the correct
  immersion medium; match its refractive index to the mounting medium where possible.

## 2. Sampling
Pixel size in the sample should be **≤ about half the resolution** (Nyquist): for
0.22 µm resolution, pixels ≲ 0.1 µm. On a confocal, set zoom/pixel count accordingly;
the software often has a "Nyquist" button. For z-stacks, step ≈ half the axial resolution.
Over-sampling wastes time and causes more bleaching; under-sampling loses detail.

Confocal pinhole: ~1 Airy unit is the usual compromise between sectioning and signal.

## 3. Exposure and gain
- Use the **histogram/range indicator LUT** (saturated pixels in one colour, zero in another).
  Set exposure or laser power/gain so the brightest real structure is just below
  saturation and the background is above zero.
- **No saturated pixels** in anything you intend to measure. Saturation clips data
  irrecoverably.
- Prefer longer exposure or higher detector gain over more excitation power when live
  imaging — excitation drives photobleaching and phototoxicity.
- Acquire at the camera's full bit depth (12/16-bit) and save in a lossless original
  format (vendor format, OME-TIFF). Never quantify JPEGs or screenshots.

## 4. Multi-channel: bleed-through
- Image **single-labelled controls** in every channel: signal in a channel where the dye
  shouldn't appear is bleed-through (emission) or cross-excitation.
- Fixes: narrower emission filters, dyes with more separated spectra, and on confocals
  **sequential (line/frame) acquisition** so only one laser is on per channel.
- Put the weakest signal on the brightest, most photostable dye.

## 5. Controls for interpretation
- Unstained (autofluorescence), **secondary-only** (non-specific secondary binding),
  and a biological negative (knockout/knockdown or untransfected).
- For any comparison of intensities between conditions: **identical** objective,
  exposure, gain, laser power, pinhole, binning and offset, set on the brightest
  condition and then locked. Image conditions in an interleaved order on the same day.

## 6. Corrections
- Uneven illumination (vignetting) biases intensity across the field: acquire a
  **flat-field** reference (uniform fluorescent slide) and dark frame and correct, or
  restrict measurement to the central region.
- Background subtract consistently (same method and parameters for all images).

## Gotchas
- Choosing "representative" fields after seeing them is selection bias: use predefined
  positions or random stage coordinates.
- Auto-exposure changes settings per image — turn it off for quantitative work.
- Mounting media with antifade differ in refractive index and can quench some dyes.
- Live cells: watch for blebbing and halted motility — signs of phototoxicity before
  bleaching is obvious.
- Display adjustments (brightness/contrast) are fine if applied equally to all compared
  images and stated; changing gamma or non-linear LUTs must be disclosed.

Uncertain here: brightness ∝ NA⁴/M² is the textbook epifluorescence approximation; real
systems vary with transmission and camera.

## Verify
- [ ] Objective NA, coverslip #1.5 and immersion medium appropriate.
- [ ] Pixel size at or below Nyquist for the resolution claimed.
- [ ] No saturated pixels in measured structures; raw files kept at full bit depth.
- [ ] Single-stain and secondary-only controls show no bleed-through or background issue.
- [ ] Identical settings across all compared conditions, recorded in metadata.
