---
id: natural-sciences.laboratory-field-methods.imagej.particle-analysis-and-batch-macros
name: particle-analysis-and-batch-macros
category: natural-sciences
field: laboratory-field-methods
product: imagej
tags: [imagej, fiji, image-analysis, particle-analysis, analyze-particles, thresholding, auto-threshold, otsu, huang, binary-mask, watershed, set-scale, set-measurements, roi-manager, background-subtraction, rolling-ball, cell-counting, nuclei-counting, macro, ijm, macro-recorder, batch-processing, bio-formats, headless, scientific-image-analysis, reproducibility]
level: practitioner
status: docs-checked
description: "Count and measure objects in Fiji/ImageJ: set scale, subtract background, threshold with a named method, watershed, Analyze Particles, then batch a folder."
sources: [https://imagej.net/ij/docs/menus/analyze.html, https://imagej.net/ij/docs/menus/process.html, https://imagej.net/plugins/auto-threshold]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Particle analysis and batch macros in Fiji/ImageJ

**Goal:** count and measure objects (nuclei, colonies, particles, cells) across a whole
folder of images with **one fixed, recorded procedure**, so results are reproducible
and not the product of hand-tuning each image.

## 1. Open and check the image
- Use **Fiji** (ImageJ bundled with plugins). Open vendor files through Bio-Formats so
  the metadata, including pixel size, is kept.
- Confirm the pixel size in calibrated units. If missing, use **Analyze › Set Scale**
  with a known distance (scale bar or stage micrometer); setting Distance in Pixels to
  zero reverts to pixel measurements.
- Work on a duplicate; never overwrite the raw file.
- Measure on the raw intensities, not on a contrast-enhanced or RGB-converted copy.

## 2. Pre-process (same for every image)
- **Process › Subtract Background** for uneven illumination. For 8-bit or RGB images the
  rolling ball radius should be at least as large as the largest object that is not part
  of the background.
- Optional light smoothing: **Process › Filters › Gaussian Blur** (Sigma is the standard
  deviation of the Gaussian) to reduce noise before thresholding.
- Pick the channel of interest (Image › Color › Split Channels).

## 3. Threshold
- **Image › Adjust › Auto Threshold** (the Auto Threshold plugin, installed in Fiji; run
  Help › Update Menus after installing). Use the "Try all" option once for a montage of
  every method, then choose one named method (Otsu, Huang, Li, Triangle...) that works
  across your images. Record it.
- Avoid dragging the manual threshold slider per image: that is subjective and
  irreproducible. If one fixed method fails on some images, the acquisition or
  pre-processing needs fixing.
- **Process › Binary › Convert to Mask** converts the image to black and white from the
  current threshold (it computes one from the histogram if none is set).

## 4. Separate touching objects
**Process › Binary › Watershed** separates touching particles using a distance map. It
suits roundish objects; inspect the result for over-splitting of elongated or irregular
shapes.

## 5. Measure
1. **Analyze › Set Measurements**: tick Area, Mean gray value, Shape descriptors, etc.;
   set **Redirect to:** the original image to measure intensities from the raw data using
   the outlines made on the mask.
2. **Analyze › Analyze Particles**: Size range in calibrated units (particles outside it
   are ignored) to exclude debris; Circularity range if useful (1.0 is a perfect circle);
   tick **Exclude on edges**, **Display results**, **Summarize** (count, total area,
   average size, area fraction) and **Add to Manager**. Show: Outlines gives numbered
   outlines for a QC overlay.
3. Save the ROI set and the outlines image for each input.

## 6. Record and batch
1. Use the macro recorder: perform the steps once on one image and it writes the macro
   commands.
2. Edit the recorded commands into a macro that loops over a folder with the same fixed
   threshold method and parameters for every file, and saves the results table and the
   outlines per image. Check the macro-language reference for the folder-loop functions.
3. Save the macro with the data and note the Fiji version.

## Gotchas
- Subtract Background and some filters change the image: keep raw images separate.
- "Exclude on edges" biases against large objects; acceptable for counts per field, note it.
- Recorded commands depend on the exact menu labels of the installed version.
- Validate once against manual counts on a few images (aim for agreement within your tolerance).

## Verify
- [ ] Scale set from metadata or a calibration image; units shown in results.
- [ ] One named threshold method used for all images.
- [ ] Outline overlays reviewed for over/under-segmentation.
- [ ] Macro, Fiji version and ROI sets saved alongside results.
- [ ] Automated counts agree with manual counts on a validation subset.

## Checked
2026-11-01. Confirmed against the ImageJ Analyze and Process menu documentation (Analyze Particles options, Set
Measurements Redirect To and Shape Descriptors, Set Scale, Subtract Background radius guidance, Convert to Mask,
Watershed, Gaussian Blur sigma) and the Auto Threshold plugin page (method names, Try all, menu path). Removed: example
radius and sigma values, Enhance Contrast normalise warning, the example macro code and its option strings, headless
flags, StarDist/Cellpose comparison, 8-bit conversion claim, Dark background tip, several menu paths no page stated.
Method: documentation only; no commands were run.
