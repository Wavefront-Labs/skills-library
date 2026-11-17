---
id: natural-sciences.physics.nuclear-physics.hpge-gamma-spectrometry-calibration
name: hpge-gamma-spectrometry-calibration
category: natural-sciences
field: physics
product: nuclear-physics
tags: [nuclear-physics, gamma-spectrometry, gamma-spectroscopy, hpge, germanium-detector, energy-calibration, efficiency-calibration, fwhm, resolution, full-energy-peak, eu-152, co-60, cs-137, am-241, mixed-gamma-source, dead-time, pile-up, true-coincidence-summing, background-subtraction, minimum-detectable-activity, mda, currie, genie-2000, gammavision, activity-measurement, radiation-detection]
level: practitioner
status: gated
description: "Calibrate an HPGe gamma spectrometer for energy, resolution and full-energy-peak efficiency; handle dead time, coincidence summing, geometry and background."
sources: ["G. F. Knoll, Radiation Detection and Measurement (4th ed.), ch. 12", "IAEA-TECDOC-1401 Quantifying uncertainty in nuclear analytical measurements", "L. A. Currie, Anal. Chem. 40 (1968) 586", "NNDC / DDEP recommended decay data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPGe gamma spectrometry: energy and efficiency calibration

**Goal:** turn peak areas in a high-purity germanium spectrum into activities (Bq)
with a defensible uncertainty, for a stated sample geometry.

## 1. Before calibrating
- Detector cooled and stable (LN₂ or electric cooler) for hours; bias at the
  manufacturer's recommended voltage, applied slowly.
- Set shaping time / digital filter for resolution vs. throughput (longer = better
  FWHM, more dead time). Adjust pole-zero so peaks have no low- or high-side tail.
- Take a long **background** spectrum (shield closed, empty sample holder) — at least
  as long as your longest sample count. Expect ⁴⁰K 1460.8 keV (line energies in this skill are recalled from decay-data evaluations and were not re-fetched (gated: unconfirmed, source is paywalled or blocked)), U/Th-chain lines
  (²¹⁴Bi 609, ²⁰⁸Tl 2614.5), 511 keV annihilation, and Pb X-rays.

## 2. Energy and resolution calibration
- Use a source with lines spanning your range: ¹⁵²Eu (122–1408 keV, many lines),
  plus ²⁴¹Am 59.5, ¹³⁷Cs 661.7, ⁶⁰Co 1173.2/1332.5 keV.
- Fit E(channel) as linear or quadratic; residuals should be ≲0.1 keV.
- Fit FWHM(E) (typical form FWHM = √(a + bE + cE²)); a coaxial detector is often
  ~1.8–2.0 keV at 1332 keV (check your detector's specification sheet). A sudden worsening = noise, warm-up, or neutron damage.

## 3. Efficiency calibration
- Use a **certified** standard (activity, reference date, uncertainty on the
  certificate) in the **same geometry, matrix density and fill height** as the
  samples. Efficiency for a 1 L Marinelli beaker of water is not that for a point
  source at 10 cm.
- Decay-correct: A(t) = A₀·exp(−ln2·Δt/T½) using recommended half-lives.
- ε(E) = N_net / (A · Iγ · t_live). Use Iγ (emission probability) from evaluated
  decay data, not a textbook rounding.
- Fit log ε vs. log E (polynomial, separately above and below the "knee" ~100–200 keV).
  Residuals should be within the source uncertainty (a few %).

## 4. Corrections that bite
- **Dead time:** use *live* time, not real time. Above ~10–20% dead time, pile-up
  losses aren't fully corrected by live-time alone — move the sample further away
  or use a pulser/LTC method.
- **True-coincidence summing:** cascade emitters (⁶⁰Co, ¹⁵²Eu, ¹³³Ba, ¹³⁴Cs) lose
  counts from peaks (and add sum peaks) in close geometries. A ¹⁵²Eu calibration at
  the detector face is biased unless corrected (software such as EFFTRAN, GESPECOR
  or vendor tools, or Monte Carlo). Single-line emitters (¹³⁷Cs, ⁵⁴Mn, ⁸⁵Sr) avoid this.
- **Self-attenuation:** a dense sample (soil, metal) attenuates low-energy gammas more
  than a water standard. Correct by transmission measurement or calculation.
- **Interferences:** e.g. ²²⁶Ra 186.2 keV sits on ²³⁵U 185.7 keV; check every line.

## 5. Activity, uncertainty, detection limits
A = N_net / (ε · Iγ · t_live) × decay/summing/attenuation corrections. Combine
counting, efficiency, Iγ and geometry uncertainties in quadrature (GUM style).
When no peak is seen, report a minimum detectable activity, e.g. Currie
L_D ≈ 2.71 + 4.65√B (counts; formula as in Currie 1968, arithmetic recomputed, 49.2 counts for B = 100; paired-blank form, confirm the variant in the paper), converted to Bq — not "zero".

## Gotchas
- Peak-search software misses small peaks on a high continuum and splits doublets;
  inspect fits by eye.
- Radon in the shield cavity varies with weather and ventilation — purge with
  LN₂ boil-off gas if low-level work matters.
- *Uncertainty note:* typical FWHM numbers vary with crystal type (coaxial,
  broad-energy, well); use your detector's specification sheet as the reference.

## Verify
- [ ] Energy residuals ≲0.1 keV, FWHM within detector specification.
- [ ] Efficiency standard matches sample geometry, density and fill height.
- [ ] Summing and dead-time corrections applied or shown negligible.
- [ ] A check source counted as an unknown reproduces its certified activity within uncertainty.
- [ ] Non-detects reported as MDA with the formula used.
