---
id: natural-sciences.environmental-science.biogeochemistry.static-chamber-soil-ghg-flux-measurement
name: static-chamber-soil-ghg-flux-measurement
category: natural-sciences
field: environmental-science
product: biogeochemistry
tags: [biogeochemistry, greenhouse-gas, ghg-flux, soil-flux, static-chamber, closed-chamber, non-steady-state, nitrous-oxide, n2o, methane, ch4, carbon-dioxide, co2, soil-respiration, gas-chromatography, laser-analyser, picarro, li-cor, hutchinson-mosier, linear-regression, flux-calculation, ideal-gas-law, carbon-cycling, nitrogen-cycling, emission-factor, cumulative-flux]
level: practitioner
status: gated
description: "Measure soil CO2, N2O and CH4 fluxes with static chambers: collar install, vent and seal, sampling schedule, linear vs non-linear flux fits, unit conversion, and cumulative emission gap-filling."
sources: [Global Research Alliance N2O Chamber Methodology Guidelines (de Klein & Harvey, 2012/2015), Hutchinson & Mosier 1981 SSSAJ, USDA-ARS GRACEnet chamber protocol, Pedersen et al. 2010 HMR method]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static-chamber soil greenhouse-gas flux measurement

**Goal:** quantify how much CO2, N2O and CH4 a soil emits (or takes up) per area per
time, and scale point measurements to a seasonal budget, using closed (non-steady-state)
chambers.

## 1. Chamber and collar
- **Collar (base):** stainless steel or PVC, inserted 5–10 cm into soil, ideally
  **≥24 h before** the first measurement so the root/soil disturbance pulse passes.
  Leave in place all season; note any plants inside.
- **Lid:** opaque or reflective (to limit heating), with a **vent tube** to equalise
  pressure, a septum sampling port, and a gas-tight seal (water channel or gasket).
  Height ~10–20 cm; a larger volume/area ratio slows the concentration rise and reduces
  feedback on the diffusion gradient.
- Record headspace height inside each collar (several points) to compute volume.

## 2. Sampling
- **Manual (GC):** close lid, withdraw samples with a gas-tight syringe at e.g. 0, 15,
  30, 45 (60) min into pre-evacuated vials (overpressurise to protect against air
  ingress). Analyse on a GC with ECD (N2O) and FID (CH4, CO2 via methaniser), with
  standards bracketing the expected range in every run.
- **Automated / laser analyser** (e.g. cavity ring-down or OF-CEAS units): connect in a
  closed loop and record continuously for a few minutes; much better precision for N2O.
- **Timing:** sample mid-morning to approximate daily mean soil temperature (a common
  convention; verify for your site with a diel campaign). Intensify after rain,
  fertiliser, tillage or thaw — N2O is notoriously **episodic**, and most of the annual
  total can come from a few pulses.
- Log soil temperature and moisture (WFPS) at every measurement.

## 3. Calculate flux
Flux = (dC/dt) × (V/A) × (P / (R·T)) × molar mass.
- `dC/dt` in ppm (µmol/mol) per hour from the regression of concentration on time.
- `V/A` = headspace height (m).
- `P/(R·T)` converts µmol/mol to µmol/m³ using chamber air temperature (K) and
  pressure (Pa); R = 8.314 J/(mol·K).
- Report N2O commonly as µg N2O-N m⁻² h⁻¹ (multiply by 28 g N per mol N2O, not 44).
Worked check (computed): dC/dt = 0.05 ppm/h, headspace 0.15 m, 20 °C, 101325 Pa gives 0.312 µmol m⁻² h⁻¹ = 8.7 µg N2O-N m⁻² h⁻¹ (13.7 µg as N2O).
**Linear vs non-linear:** concentration rise saturates as the gradient weakens, so
linear regression underestimates flux. The Hutchinson–Mosier or HMR approach fits a
non-linear model; use it when curvature is significant, otherwise linear. The R
package `HMR` (or `gasfluxes`) automates the choice (gated: unconfirmed, source is paywalled or blocked), not run here — run it consistently across
the dataset rather than picking per flux by eye.

## 4. Quality control
- Reject or flag fits with poor R² **only** if CO2 (a co-measured, usually strong
  signal) also shows leaks; low-R² N2O fluxes near zero are real data. Discarding them
  biases emissions upward.
- Compute a minimum detectable flux from analyser precision and chamber geometry, and
  report how many fluxes fell below it. Keep negative values.
- Ambient blank samples each run.

## 5. Scale up
Cumulative emission = trapezoidal integration between sampling dates (or gap-filling
with a temperature/moisture model). Report the sampling frequency; weekly sampling can
miss pulses and the uncertainty should say so. Emission factor (fertiliser-induced) =
(N2O-N treated − N2O-N control) / N applied.

## Gotchas
- Stepping near the collar pumps gas out of soil — use boardwalks.
- Chamber heating in sun inflates CO2 and alters N2O; keep closure short and lids insulated.
- Wrong molar-mass basis (N2O vs N2O-N) is a factor of 1.57 error.
- Spatial variability is huge (CV >100%); replicate chambers (≥3–4 per treatment) matter
  more than more time points per chamber.

## Verify
- [ ] Collars installed ahead of time; headspace volume measured per collar.
- [ ] ≥4 time points or continuous record; standards in each GC run.
- [ ] Linear/non-linear choice made by a consistent, documented rule.
- [ ] Units and N-basis stated; negative and below-detection fluxes retained.
- [ ] Cumulative flux method and sampling frequency reported with uncertainty.
