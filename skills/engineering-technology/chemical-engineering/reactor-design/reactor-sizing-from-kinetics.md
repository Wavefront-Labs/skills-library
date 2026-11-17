---
id: engineering-technology.chemical-engineering.reactor-design.reactor-sizing-from-kinetics
name: reactor-sizing-from-kinetics
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, cstr, pfr, batch-reactor, design-equation, rate-law, kinetics, arrhenius, levenspiel-plot, space-time, residence-time, conversion, damkohler, reactors-in-series, adiabatic-temperature-rise, heat-removal, runaway, scale-up, aspen-plus, rplug, rcstr]
level: practitioner
status: docs-checked
description: "Size CSTRs, PFRs and batch reactors from rate laws: design equations, Levenspiel plots, series/recycle choices, adiabatic temperature rise and heat-removal checks."
sources:
  - "https://en.wikipedia.org/wiki/Continuous_stirred-tank_reactor"
  - "https://en.wikipedia.org/wiki/Plug_flow_reactor_model"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sizing a reactor from kinetics

**Goal:** turn a rate law and a conversion target into a reactor type, volume and a
heat-removal duty that you have checked for thermal safety.

## 1. Get a usable rate law
-r_A = k(T)·f(C), with k = k0·exp(−Ea/RT). Fit from lab data at the planned T range, in the
regime that will exist at scale (check that mass transfer is not limiting in the lab: rate
must not change with stirring speed or particle size). A 10 °C rise roughly doubles k
only when Ea ≈ 50–60 kJ/mol near ambient; compute it from your Ea rather than assuming.

## 2. Design equations (constant density unless noted)
- **Batch:** t = C_A0 ∫₀^X dX/(−r_A)
- **CSTR:** V = F_A0·X/(−r_A) evaluated at **exit** conditions
- **PFR:** V = F_A0 ∫₀^X dX/(−r_A)
- Space time τ = V/v0. For gas-phase with mole change use C_A = C_A0(1−X)/(1+εX)·(T0/T)(P/P0).
First-order closed forms: CSTR τ = X/[k(1−X)]; PFR τ = −ln(1−X)/k.
Worked: k = 0.2 min⁻¹, X = 0.90: CSTR τ = 0.9/(0.2·0.1) = 45 min; PFR τ = ln10/0.2 = 11.5 min.
At v0 = 2 m³/min that is 90 m³ vs 23 m³. For N equal first-order CSTRs in series, per-tank
τ_i = [(1/(1−X))^(1/N) − 1]/k: for N = 2, (√10 − 1)/0.2 = 10.8 min each, 21.6 min total,
so 43 m³ instead of 90 m³.

## 3. Choose the type with a Levenspiel plot
Plot F_A0/(−r_A) vs X. CSTR volume = rectangle at exit X; PFR = area under the curve.
- Rate falls with conversion (positive order, isothermal): PFR smaller; CSTRs in series
  approach it.
- Autocatalytic or exothermic-adiabatic (rate rises then falls): CSTR to the curve minimum,
  then PFR.
- Selectivity: if the desired reaction has higher order in A than the side reaction, keep
  C_A high (PFR/batch); lower order → CSTR. Higher Ea for desired → run hot.

## 4. Heat management (do this before you fall in love with a size)
- Duty: Q = F_A0·X·(−ΔH_r).
- **Adiabatic temperature rise:** ΔT_ad = (−ΔH_r)·C_A0·X/(ρ·Cp). Worked: ΔH_r = −100 kJ/mol,
  C_A0 = 2,000 mol/m³, ρCp = 4,000 kJ/m³K → ΔT_ad = 50 K at full conversion. If ΔT_ad
  takes the mass to the onset of a decomposition or to the boiling point at relief set
  pressure, treat it as a process-safety scenario (see
  engineering-technology.chemical-engineering.process-safety.layer-of-protection-analysis);
  get calorimetry (DSC/ARC/RC1) data rather than literature values.
- Jacket capacity: Q = U·A·ΔT_lm. A ≈ scales with V^(2/3) for geometrically similar vessels, so
  area per volume falls on scale-up (10× volume → ~4.6× area). The lab vessel that "had no
  exotherm" may run away at 10 m³. Take U from vendor or measured data; add coils or external loops when the jacket can't cope.
- CSTR stability: plot heat generation vs heat removal against T; operate where removal slope
  exceeds generation slope, with margin. Semi-batch (dose-controlled) limits accumulation.

## 5. Scale-up and real flow
Real reactors deviate from ideal: check RTD (tanks-in-series N or dispersion number), mixing
time vs reaction time (Damköhler), and for heterogeneous catalysis pressure drop (Ergun) and
internal/external diffusion (Thiele modulus, effectiveness factor). Add and justify a design margin on
volume and on catalyst for deactivation.

## Verify
- [ ] Rate law fitted in the kinetic regime, valid over the operating T range.
- [ ] Hand calculation of τ/V matches the simulator within a few percent.
- [ ] Reactor type justified by Levenspiel plot and selectivity orders.
- [ ] ΔT_ad computed; worst case (cooling loss, overcharge) assessed with calorimetry data.
- [ ] Heat-removal capacity at full scale ≥ generation with margin; area/volume scale-up checked.

## Checked
2026-11-01. Re-computed with a short script: CSTR 45 min and PFR 11.5 min at k = 0.2 per min and X = 0.90 (90 m3 vs 23 m3 at 2 m3 per min); two equal CSTRs 10.8 min each, 21.6 min total, 43 m3; 10x volume gives 4.6x area (V to the 2/3); adiabatic rise 50 K; a 10 C rise roughly doubles k at Ea of about 53 kJ/mol near ambient. Removed: typical U range, 10-20 percent margin, the 3-4 tank claim and Aspen block claims (no readable source). The design equations are standard textbook forms; thermal-safety judgement stays with qualified process-safety engineers.
Method: documentation only; no commands were run.
