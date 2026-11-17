---
id: natural-sciences.laboratory-field-methods.spectroscopy.uv-vis-quantitation-with-beer-lambert
name: uv-vis-quantitation-with-beer-lambert
category: natural-sciences
field: laboratory-field-methods
product: spectroscopy
tags: [spectroscopy, uv-vis, uv-visible, spectrophotometer, absorbance, beer-lambert, beer-lambert-law, molar-absorptivity, extinction-coefficient, calibration-curve, standard-curve, linear-range, blank, baseline-correction, cuvette, quartz-cuvette, path-length, stray-light, lambda-max, nanodrop, a260, a280, lod, loq, r-squared, quantitation]
level: practitioner
status: gated
description: "Quantify a compound by UV-Vis absorbance: choose wavelength and cuvette, blank correctly, build a calibration curve in the linear range (~0.1-1 AU), and calculate LOD/LOQ."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UV-Vis quantitation with Beer–Lambert

**Goal:** a concentration from an absorbance reading that is accurate, inside the
instrument's linear range, and backed by a calibration you can show.

## 1. The relationship
**A = ε · l · c** — absorbance (unitless, "AU") = molar absorptivity ε (L mol⁻¹ cm⁻¹)
× path length l (cm) × concentration c (mol/L). A = log₁₀(I₀/I), so A = 1 means 10 %
of light transmitted; A = 2 means 1 %.

If ε at your wavelength is known reliably (e.g. NADH at 340 nm, ε ≈ 6220 (gated: unconfirmed, source is paywalled or blocked), you can
calculate c directly. Otherwise — and for any assay with a colour reagent — build a
**calibration curve** with standards.

## 2. Set up
1. **Scan** a mid-range standard across the spectrum to find λmax. Measuring at the
   peak maximises sensitivity and minimises error from small wavelength drift.
2. **Cuvette:** quartz below ~320–340 nm (glass and most plastics absorb in the UV);
   UV-grade plastic is acceptable down to ~220–230 nm per manufacturer specs (gated: unconfirmed, source is paywalled or blocked).
   Check l (usually 1.00 cm). Clean, fingerprint-free optical faces, consistent orientation.
3. Warm up the lamp (deuterium lamps typically need ~15–30 min to stabilise (gated: unconfirmed, source is paywalled or blocked).
4. **Blank** with exactly the same matrix as the samples (buffer, reagent, solvent),
   in the same or matched cuvette.

## 3. Calibration curve
- 5–7 standards spanning the expected sample range, prepared independently or by
  serial dilution from a stock weighed on an analytical balance.
- Measure in triplicate; plot A vs c; fit a straight line. Check the residuals, not just
  R²: a curve with R² = 0.995 can still be systematically bent at the top.
- Keep standards and samples within the **linear range**, typically ~0.1–1.0 AU for
  many benchtop instruments; above ~1.5–2 AU, stray light makes the response flatten.
  Dilute samples into range rather than extrapolating.
- Do **not** force the line through zero unless you have shown the intercept is
  insignificant.
- Run a check standard (from a different stock) every batch; it should read within your
  tolerance (e.g. ±5 %).

## 4. LOD and LOQ
From the calibration: LOD ≈ 3.3 × σ ÷ slope, LOQ ≈ 10 × σ ÷ slope, where σ is the
standard deviation of the blank (≥ 7–10 replicates) or of the intercept (ICH Q2-style
approach). Report results below the LOQ as "< LOQ", not as numbers.

## 5. Nucleic acids and proteins (microvolume)
NanoDrop-type instruments use very short path lengths so concentrated samples stay in range.
- dsDNA: 1 A260 ≈ 50 µg/mL; RNA ≈ 40 µg/mL; ssDNA oligo ≈ 33 µg/mL (approx.).
- A260/A280 ~1.8 (DNA) and ~2.0 (RNA) suggest little protein; A260/A230 below ~1.8 suggests
  salt/guanidine/phenol carryover.
- Protein at A280 needs the protein's own ε (from its sequence); assuming 1 AU = 1 mg/mL is
  a rough generic.
These are purity indicators, not proof; fluorometric assays are more specific.

## Gotchas
- **Scattering** (turbid samples, bubbles, precipitates) raises apparent absorbance
  across all wavelengths. Centrifuge/filter; check a non-absorbing wavelength (e.g.
  baseline at 320–340 nm for nucleic acids) and correct if needed.
- Chemical deviations: concentration-dependent dimerisation or pH-dependent absorbance
  bend the curve. Buffer the samples.
- Coloured assay reagents fade or keep developing — read all samples at a fixed time.
- Photosensitive analytes degrade under the beam; minimise exposure.
- Plate readers have path length that depends on volume; correct or calibrate in the plate.

Uncertain here: linear-range limits and cuvette cut-offs are instrument- and
material-specific; check your spectrometer manual and cuvette spec.

## Verify
- [ ] Wavelength chosen at λmax from a scan, cuvette appropriate for the wavelength.
- [ ] Blank matches sample matrix.
- [ ] Calibration with ≥ 5 standards, residuals random, samples inside the standards' range.
- [ ] Independent check standard within tolerance.
- [ ] LOD/LOQ stated; sub-LOQ results reported as such.
