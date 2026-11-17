---
id: engineering-technology.nuclear-engineering.reactor-physics.core-criticality-and-reactivity-coefficients
name: core-criticality-and-reactivity-coefficients
category: engineering-technology
field: nuclear-engineering
product: reactor-physics
tags: [reactor-physics, core-design, k-eff, criticality, six-factor-formula, reactivity, pcm, doppler-coefficient, fuel-temperature-coefficient, moderator-temperature-coefficient, mtc, void-coefficient, shutdown-margin, boron-worth, critical-boron-concentration, loading-pattern, burnable-absorber, casmo, simulate, serpent, openmc, scale-polaris, pwr, bwr, delayed-neutron-fraction]
level: advanced
status: gated
description: "Compute and check core k-eff, reactivity coefficients (Doppler, MTC, void), boron worth and shutdown margin for LWR cores using lattice/nodal or Monte Carlo codes."
sources:
  - "Duderstadt & Hamilton, Nuclear Reactor Analysis"
  - "Lamarsh & Baratta, Introduction to Nuclear Engineering"
  - "NUREG-1431 Standard Technical Specifications, Westinghouse Plants"
  - "NUREG-0800 Standard Review Plan, Section 4.3 Nuclear Design"
  - "Studsvik CASMO5 and SIMULATE5 user documentation"
  - "Serpent 2 and OpenMC user manuals"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core criticality and reactivity coefficients — the numbers a reload design must defend

**Goal:** calculate k-eff, critical boron, reactivity coefficients and shutdown margin for a light-water core, and check them against the plant's limits before a loading pattern is accepted.

Engineering guidance only. Licensed reload analyses must use the plant's approved methodology, its Core Operating Limits Report (COLR) and Technical Specifications, and independent review.

## Core quantities

- **Multiplication:** k-eff = k-inf · P_FNL · P_TNL. Six-factor form: k-eff = η · f · p · ε · P_FNL · P_TNL (reproduction factor, thermal utilisation, resonance escape, fast fission, non-leakage probabilities). Use it to reason about *why* reactivity moves.
- **Reactivity:** ρ = (k − 1)/k. 1 pcm = 10^-5 Δk/k. Differences between two states: Δρ = ρ2 − ρ1 = (k2 − k1)/(k1·k2) exactly, and ln(k2/k1) is the close approximation (k1 = 0.99, k2 = 1.01: 0.020002 exact vs 0.020001 from the log; computed).
- **Delayed neutron fraction:** β-eff ≈ 650-720 pcm for fresh UO2 cores, falling toward ~500 pcm at end of cycle as Pu-239 fissions grow (gated: unconfirmed, source is paywalled or blocked). 1 dollar = β-eff; prompt critical at ρ = 1 $.

## Workflow (two-step lattice/nodal)

1. **Lattice:** CASMO5, SCALE/Polaris, or Serpent 2 for each assembly type: depletion with branch cases (fuel temperature, moderator density/temperature, boron, control rods) to build few-group cross-section tables.
2. **Core:** SIMULATE5, PARCS or equivalent nodal code: depletion of the loading pattern with critical boron search (PWR) or control-rod/flow search (BWR).
3. **Reference checks:** full-core continuous-energy Monte Carlo (Serpent, OpenMC, MCNP — see engineering-technology.nuclear-engineering.mcnp.building-an-mcnp-input-deck) at a few statepoints to confirm pin-power and k-eff trends.
4. Validate against start-up physics tests: HZP critical boron typically within ±50 ppm, rod bank worths within ~10% (bothgated: unconfirmed, source is paywalled or blocked; use the plant's acceptance criteria), isothermal temperature coefficient.

## Coefficients: definitions and typical PWR values

Calculate each as a two-state perturbation, holding everything else fixed.

| Coefficient | Definition | Typical sign / magnitude |
|---|---|---|
| Doppler / fuel temperature (FTC) | ∂ρ/∂T_fuel | −1.5 to −4 pcm/K; always negative (gated: unconfirmed, source is paywalled or blocked) |
| Moderator temperature (MTC) | ∂ρ/∂T_mod | near 0 or slightly positive at BOC HZP with high boron; about −50 to −80 pcm/K at EOC HFP (gated: unconfirmed, source is paywalled or blocked) |
| Power coefficient | ∂ρ/∂P | negative; defect HZP→HFP ~1000-2000 pcm (gated: unconfirmed, source is paywalled or blocked) |
| Boron worth (differential) | ∂ρ/∂C_B | about −6 to −10 pcm/ppm; magnitude falls with higher boron and burnup (gated: unconfirmed, source is paywalled or blocked) |
| BWR void coefficient | ∂ρ/∂α | negative, order −50 to −150 pcm per % void (unconfirmed generic range; burnup dependentgated: unconfirmed, source is paywalled or blocked) |

Tech Specs typically cap the MTC at a small positive value at low power ramping to ≤0 at full power, and set a most-negative EOC limit used in steam-line-break analysis. Exact limits are plant-specific — read them from the COLR.

The **isothermal temperature coefficient** measured at startup = MTC + FTC at uniform temperature; subtract the calculated FTC to infer MTC.

## Shutdown margin

SDM = amount by which the core would be subcritical with all rods inserted **except the single highest-worth rod stuck out**, no xenon credit, at the most reactive temperature. Calculation:

SDM = (total rod worth × (1 − uncertainty allowance, often 10%)) − stuck-rod worth penalty − power defect − redistribution/void allowances.

The Standard Technical Specifications (NUREG-1431 LCO 3.1.1) do not fix a universal number: the LCO says SDM shall be within the limits specified in the COLR, applies in MODE 2 with k-eff < 1.0 and MODES 3, 4 and 5, and in MODES 1 and 2 SDM is ensured by the shutdown and control bank insertion limits (LCO 3.1.5, 3.1.6) (read in NRC search extracts; full NUREG PDF returned 403, gated: unconfirmed). One plant COLR extract showed 1.77% Δk/k. A previous version of this skill claimed 1.3% for Modes 1-2 per NUREG-1431; that is not supported and was removed. BWR values: read your plant's Tech Spec and COLR. Evaluate at the limiting burnup — often EOC for PWRs (most negative MTC, largest cooldown insertion) and BOC/peak-reactivity for BWRs.

## Loading pattern basics

- **Low-leakage pattern:** feed assemblies inboard, burned assemblies on the periphery; saves neutron economy and vessel fluence but drives up power peaking, controlled with burnable absorbers (IFBA, Gd2O3, WABA).
- Check limits each statepoint: FΔH (nuclear enthalpy rise, typical limit ~1.55-1.65 (gated: unconfirmed, source is paywalled or blocked)), FQ (total peaking, typical ~2.5 incl. uncertainty (gated: unconfirmed, source is paywalled or blocked)), MTC, SDM, rod insertion limits, cycle length in EFPD. The thermal margin side is in engineering-technology.nuclear-engineering.thermal-hydraulics.critical-heat-flux-margin-analysis.
- Gadolinia depletes in a non-linear way: reactivity peaks mid-cycle when Gd burns out; check peaking there, not just BOC/EOC.

## Gotchas

- Doppler needs the fuel temperature model consistent with the thermal code (effective fuel temperature, not centreline).
- Comparing two Monte Carlo k-eff values for a coefficient: the statistical uncertainty of the difference is √(σ1² + σ2²). A 5 pcm/K coefficient from 30 K perturbations is a 150 pcm signal; σ of the difference should be a small fraction of that (sqrt(2) x 10 pcm = 14 pcm is about 10% of it, computed).
- Positive MTC early in a high-boron cycle is the classic loading-pattern failure; fix with more burnable absorber, not by lowering boron assumptions.

## Verify

- [ ] HZP critical boron and rod worths predicted within the start-up test acceptance criteria.
- [ ] FTC negative at all statepoints; MTC within COLR limits at BOC HZP and EOC HFP.
- [ ] SDM computed with the highest-worth rod stuck out and uncertainty allowance, at the limiting burnup, meets the Tech Spec value.
- [ ] FΔH and FQ within limits at every depletion step including the burnable-absorber reactivity peak.
- [ ] Monte Carlo reference agrees with nodal k-eff within a few hundred pcm and pin powers within a few percent.
