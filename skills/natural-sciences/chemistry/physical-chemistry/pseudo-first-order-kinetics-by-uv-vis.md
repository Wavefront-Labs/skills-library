---
id: natural-sciences.chemistry.physical-chemistry.pseudo-first-order-kinetics-by-uv-vis
name: pseudo-first-order-kinetics-by-uv-vis
category: natural-sciences
field: chemistry
product: physical-chemistry
tags: [physical-chemistry, chemical-kinetics, reaction-kinetics, rate-constant, pseudo-first-order, kobs, second-order-rate-constant, uv-vis, spectrophotometry, absorbance, beer-lambert, isosbestic-point, stopped-flow, temperature-control, peltier, eyring, arrhenius, activation-energy, exponential-fit, nonlinear-regression, guggenheim, initial-rates, method-of-isolation, scipy, curve-fit]
level: practitioner
status: gated
description: "Measure a rate constant by UV-Vis under pseudo-first-order conditions: choosing wavelength, excess reagent, temperature control, fitting absorbance traces, kobs vs concentration."
sources: ["P. Atkins & J. de Paula, Physical Chemistry, chemical kinetics chapters", "J. H. Espenson, Chemical Kinetics and Reaction Mechanisms (2nd ed., 1995)", "IUPAC Gold Book: pseudo rate constant (P04933)", "https://goldbook.iupac.org/terms/view/P04933"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pseudo-first-order kinetics by UV-Vis

**Goal:** the second-order rate constant k for A + B → P (and ideally its temperature
dependence) from absorbance-vs-time traces, with a check that the mechanism is
what you assumed.

## 1. Design: isolate one reagent
- Keep **B in ≥ 10-fold excess** over A (20× is safer). Then [B] ≈ constant and
  rate = k[A][B] = k_obs[A], with k_obs = k[B].
- Plan 4–6 concentrations of B spanning at least a factor of ~5.
- Pick the reaction half-life for the instrument: a standard spectrometer with manual
  mixing handles t½ ≳ 10–20 s; faster needs stopped-flow (ms dead time).

## 2. Choose the wavelength
- Take spectra of A, B and P separately (and a full scan during a test run).
- Choose λ where the absorbance change is large and B (in excess!) absorbs little.
  An excess reagent with high absorbance pushes total A beyond the linear range
  (keep total absorbance ≲ 1–1.5).
- **Isosbestic points** in repeated scans indicate a clean A → P conversion without
  a long-lived intermediate; their absence is a warning.

## 3. Running it
- Thermostat the cell holder (Peltier or circulating bath) and pre-equilibrate both
  solutions at the run temperature ≥ 10 min. k typically changes several % per °C (gated: unconfirmed, source is paywalled or blocked).
- Blank with solvent + B at the right concentration (or account for B's absorbance).
- Mix quickly and reproducibly (e.g. add a small volume of concentrated A to B in the
  cell, invert with a stopper or stir); note the dead time.
- Record to ≥ 5 half-lives so the final absorbance A∞ is measured, not guessed.

## 4. Analysis
1. Fit each trace to A(t) = A∞ + (A₀ − A∞)·exp(−k_obs·t) by **nonlinear least
   squares** (e.g. `scipy.optimize.curve_fit`), with A₀, A∞, k_obs all free.
   Prefer this over plotting ln(A − A∞) vs t, which needs A∞ exactly and
   distorts error weighting.
2. Residuals should be random; systematic wiggles mean non-exponential behaviour
   (consecutive reactions, A not in deficit, mixing artefacts).
3. Plot k_obs vs [B]. A straight line through the origin: rate = k[A][B], slope = k.
   - Non-zero intercept → a parallel path independent of B (e.g. solvolysis).
   - Curvature that saturates → pre-equilibrium (complex formation) before the
     rate-determining step; fit to k_obs = k·K[B]/(1 + K[B]).
4. Temperature series (≥ 4 temperatures over ≥ 20–30 K): Eyring plot ln(k/T) vs 1/T
   gives ΔH‡ and ΔS‡; Arrhenius ln k vs 1/T gives E_a.

## Gotchas
- Photochemistry: the spectrometer's light can drive the reaction. Test by varying
  sampling frequency or using a shutter; rates shouldn't depend on it.
- Evaporation or temperature drift during long runs drifts A∞.
- Order in A is assumed to be 1; verify by checking that k_obs doesn't depend on [A]₀.
- Water/oxygen-sensitive chemistry needs sealed (septum/screw-cap) cuvettes.
- *Uncertainty note:* the 10× excess and timing guidelines are common rules of thumb;
  the excess actually needed depends on the precision you want (at 10× the error is ~5%: recomputed by fitting a single exponential to an exact second-order trace, k_obs/(k[B]₀) = 0.89 at 5×, 0.94 at 10×, 0.97 at 20×, always low).

## Verify
- [ ] [B]/[A]₀ ≥ 10 for every run; temperature recorded per run.
- [ ] Traces cover ≥ 5 half-lives; nonlinear fit residuals are random.
- [ ] k_obs independent of [A]₀ and of measurement light exposure.
- [ ] k_obs vs [B] plotted; intercept/curvature interpreted.
- [ ] Replicate runs agree within a few percent.
