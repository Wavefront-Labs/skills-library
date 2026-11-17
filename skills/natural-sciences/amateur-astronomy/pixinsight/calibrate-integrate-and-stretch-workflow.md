---
id: natural-sciences.amateur-astronomy.pixinsight.calibrate-integrate-and-stretch-workflow
name: calibrate-integrate-and-stretch-workflow
category: natural-sciences
field: amateur-astronomy
product: pixinsight
tags: [pixinsight, astrophotography, image-processing, wbpp, weighted-batch-preprocessing, calibration, image-integration, subframe-selector, dynamic-background-extraction, dbe, abe, graxpert, color-calibration, spcc, spectrophotometric-color-calibration, linear-processing, noise-reduction, noisexterminator, blurxterminator, starxterminator, histogram-transformation, generalized-hyperbolic-stretch, ghs, screen-transfer-function, stf, narrowband, hoo, sho]
level: practitioner
status: draft
description: "A dependable PixInsight workflow: WBPP calibration and integration, background extraction, SPCC colour, linear deconvolution and noise reduction, then a controlled stretch — in the right order."
sources: ["PixInsight reference documentation (pixinsight.com)", "WBPP script documentation", "Russell Croman's RC-Astro tool documentation (BlurXTerminator, NoiseXTerminator, StarXTerminator)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PixInsight: calibrate, integrate and stretch

**Goal:** turn a night's subs and calibration frames into a clean, colour-calibrated,
stretched image — doing linear-stage steps while the data are still linear, which is the
single rule most beginners break.

## 0. Know the STF trap
Linear data look black. The **ScreenTransferFunction** (STF, Ctrl+A auto-stretch) only
changes the *display*. Your image is still linear until you apply a real stretch. Keep STF
on while working linear; the title bar/indicator shows when STF is active.

## 1. Calibrate and integrate: WBPP
Script › Batch Preprocessing › **WeightedBatchPreprocessing**.
1. Add lights, darks, flats, dark-flats (or bias). WBPP groups by keywords (filter,
   exposure, binning, temperature) read from FITS headers — check grouping in the
   Calibration tab; mis-grouped flats are the commonest silent failure.
2. Options: cosmetic correction (hot/cold pixels) on; **debayer** for OSC (one-shot colour)
   cameras with the correct Bayer pattern; **subframe weighting** (PSF signal weight is a
   good default); registration reference auto or chosen manually from a sharp, low-noise sub.
3. Integration rejection: Generalized ESD or Winsorized sigma clipping for ~15+ frames;
   linear fit clipping for many frames with gradients. *Defaults are good starting points.*
4. Run, then **inspect the master**: no dust donuts (flats worked), no vignetting
   gradients, no amp glow, satellite trails rejected.
Optional before WBPP: **SubframeSelector** to cull subs by FWHM, eccentricity, star count.

## 2. Linear processing (in this order)
1. **Crop** stacking edges (DynamicCrop) — ragged borders confuse later tools.
2. **Background extraction**: DynamicBackgroundExtraction (place samples on true
   background, avoiding nebulosity and stars; Subtraction for light-pollution gradients,
   Division for vignetting residuals) or ABE, or GraXpert. Check the extracted background
   model looks smooth.
3. **Colour calibration**: **SPCC** (SpectrophotometricColorCalibration) — needs a plate
   solution (ImageSolver) and your camera/filter curves; also neutralises background.
   For narrowband palettes (SHO/HOO), colour calibration is an aesthetic choice; combine
   channels with PixelMath or ChannelCombination.
4. **Deconvolution**: BlurXTerminator (commercial, widely used) or classic Deconvolution
   with a PSF model and star mask — must be done on linear data.
5. **Noise reduction**: NoiseXTerminator (commercial) or MultiscaleLinearTransform /
   TGVDenoise with masks. Light-handed in linear; can add a little more after stretch.
6. Optional: **StarXTerminator** to separate stars and nebula for independent stretching.

## 3. Stretch (non-linear)
- **HistogramTransformation**: drag the STF settings onto the HT bar (or use the STF
  auto-stretch as a starting point), apply, then refine; avoid clipping blacks (watch the
  clipped-pixel count).
- **GeneralizedHyperbolicStretch (GHS)**: more control — stretch faint regions while
  protecting highlights; multiple gentle passes beat one hard one.
- Stretch stars separately (gentler) if separated, then recombine with PixelMath (e.g.
  screen blend `~((~starless)*(~stars))`).

## 4. Finishing
CurvesTransformation for contrast and saturation (with masks), LocalHistogramEqualization
for structure (sparingly), small-scale sharpening only if deconvolution didn't suffice.
Save a master as XISF or 32-bit TIFF; export JPG/PNG for sharing.

## Gotchas
- Doing background extraction or SPCC after a stretch — both assume linear data.
- Forgetting STF is on and thinking the image is "already stretched".
- Over-aggressive noise reduction: plastic, blotchy backgrounds.
- DBE samples on faint nebulosity, subtracting real signal.
- Version drift: process names and defaults change between PixInsight releases.

## Verify
- [ ] WBPP groups correct; master shows no dust donuts or gradients from calibration.
- [ ] Background extracted, background model smooth, image neutral grey background.
- [ ] Colour calibration (SPCC) done on linear data after plate solving.
- [ ] Deconvolution and first noise reduction done before the stretch.
- [ ] Final histogram has no clipped blacks; stars not bloated.
