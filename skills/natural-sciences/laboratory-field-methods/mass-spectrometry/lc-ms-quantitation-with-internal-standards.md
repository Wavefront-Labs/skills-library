---
id: natural-sciences.laboratory-field-methods.mass-spectrometry.lc-ms-quantitation-with-internal-standards
name: lc-ms-quantitation-with-internal-standards
category: natural-sciences
field: laboratory-field-methods
product: mass-spectrometry
tags: [mass-spectrometry, lc-ms, lc-ms-ms, tandem-ms, triple-quadrupole, mrm, srm, esi, electrospray, ionisation-mode, quantitation, internal-standard, stable-isotope-labelled, sil-is, deuterated-standard, matrix-effects, ion-suppression, post-column-infusion, calibration-curve, weighting, 1-over-x-squared, qualifier-ion, ion-ratio, carryover, lloq, bioanalytical-validation]
level: advanced
status: draft
description: "Quantify analytes by LC-MS/MS with MRM: choose ionisation and transitions, use stable-isotope internal standards, test matrix effects, build weighted calibrations, and check ion ratios and carryover."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LC-MS/MS quantitation with internal standards

**Goal:** accurate concentrations of target analytes in a complex matrix (plasma,
tissue, water, food) by triple-quadrupole LC-MS/MS, robust to the run-to-run and
sample-to-sample variation in ionisation that makes raw MS signals unreliable.

## 1. Tune the analyte
1. Infuse a ~0.1–1 µg/mL standard and pick the **ionisation mode**: ESI positive for
   bases/amines (protonated [M+H]⁺), ESI negative for acids ([M−H]⁻). APCI for less polar,
   neutral compounds. Watch for adducts ([M+Na]⁺, [M+NH₄]⁺) — sodium adducts fragment
   poorly and vary with glassware/mobile phase.
2. Optimise precursor, then collision energy for **two product ions**: the most intense
   is the **quantifier**, the second the **qualifier**.
3. Avoid non-specific transitions (water/CO₂ losses) when a structural fragment exists.

## 2. Internal standards
- Best: **stable-isotope-labelled (SIL) analogue** of each analyte (¹³C/¹⁵N preferred;
  deuterated is cheaper but can elute slightly earlier and sometimes exchange
  deuterium). It co-elutes and experiences the same ion suppression, so the
  analyte/IS **area ratio** cancels it.
- Mass difference ≥ ~3 Da to avoid isotopic overlap from the analyte's natural isotopes;
  check the SIL standard for unlabelled impurity contributing to the analyte channel.
- Add the IS **as early as possible** (before extraction) at a fixed concentration, so it
  also corrects recovery losses.
- A structural analogue IS is a compromise; validate it more carefully.

## 3. Matrix effects
Co-eluting matrix components suppress (or enhance) ionisation, invisibly.
- **Post-column infusion:** infuse analyte continuously while injecting extracted blank
  matrix; dips in the signal show where suppression zones elute. Move the analyte
  away from them chromatographically.
- **Post-extraction spike:** matrix effect (%) = (response in spiked extract ÷ response in
  neat solvent) × 100. Test several independent matrix lots (common guidance: ≥ 6).
- Reduce by better clean-up (SPE, phospholipid removal), dilution, or chromatography.
  Phospholipids in plasma are a notorious late-eluting suppressor.

## 4. Calibration
- Prepare calibrators in **matching blank matrix** (or a validated surrogate), plus QC
  samples at low/mid/high concentrations made from a separate stock.
- Plot area ratio vs concentration; MS response typically spans orders of magnitude, so
  variance grows with concentration — use **1/x or 1/x² weighting**. Unweighted fits make
  low-end accuracy terrible.
- Common bioanalytical acceptance (FDA/ICH M10-style): back-calculated calibrators and
  QCs within ±15 % (±20 % at the LLOQ). Check what your field/regulator requires.
- LLOQ: lowest calibrator with acceptable accuracy/precision and signal-to-noise
  (often ≥ 5–10).

## 5. Run-time checks
- **Ion ratio** (qualifier/quantifier) within tolerance of standards (e.g. ±20–30 %
  depending on guideline) — confirms identity and flags interferences.
- **Retention time** within a tight window of standards.
- **IS response** plotted across the run: a sample with IS area far below the others
  signals suppression or an extraction failure — re-run it.
- **Carryover:** inject a blank after the top calibrator; analyte in the blank should be
  ≤ ~20 % of LLOQ response.
- Bracket samples with QCs throughout long batches.

## Gotchas
- Isobaric compounds (same mass and fragment) need chromatographic separation; MS/MS does
  not distinguish them.
- In-source fragmentation of conjugates (glucuronides) can produce the parent analyte's
  ions; separate them by LC.
- Non-volatile buffers (phosphate) contaminate the source; use formate/acetate/ammonium.
- Saturation at the top of the range bends the curve; detune or use a less intense transition.

Uncertain here: acceptance limits are paraphrased from bioanalytical guidelines and differ
for environmental, food and clinical methods.

## Verify
- [ ] Quantifier and qualifier transitions selected; ion ratios stable in standards.
- [ ] SIL internal standard added before extraction; IS response consistent across run.
- [ ] Matrix effect measured in multiple matrix lots and acceptable or corrected.
- [ ] Weighted calibration; calibrators and QCs within acceptance limits.
- [ ] Carryover blank below threshold.
