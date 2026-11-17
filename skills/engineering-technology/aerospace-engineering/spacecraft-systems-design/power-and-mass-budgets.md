---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.power-and-mass-budgets
name: power-and-mass-budgets
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, systems-engineering, satellite-design, mass-budget, power-budget, margins, mass-growth-allowance, solar-array-sizing, battery-sizing, depth-of-discharge, eclipse, eps, link-budget, eb-n0, thermal-balance, adcs, smad, ecss, aiaa-s-120, cubesat, smallsat, phase-a, concurrent-engineering]
level: practitioner
status: draft
description: "Size a spacecraft bus: mass and power budgets with maturity margins, solar array and battery sizing over eclipse, link budget and thermal sanity checks."
sources:
  - "Wertz and Larson (eds.), Space Mission Analysis and Design (SMAD); Wertz et al., Space Mission Engineering: The New SMAD"
  - "Fortescue, Swinerd and Stark, Spacecraft Systems Engineering"
  - "AIAA S-120A, Mass Properties Control for Space Systems"
  - "ESA, Margin Philosophy for Science Assessment Studies"
  - "ECSS-E-ST-20C, Electrical and Electronic (space engineering)"
  - "Gilmore (ed.), Spacecraft Thermal Control Handbook"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Spacecraft power and mass budgets — the trade space every subsystem lives in

**Goal:** Phase A/B budgets for mass, power, link and thermal that close with
maturity-appropriate margins, and that update cleanly as the design matures.

## 1. Mass budget
- Structure the budget by subsystem → unit, with for each line: current best estimate
  (CBE), maturity (off-the-shelf / modified / new), margin, and source.
- Unit-level margins (a common pattern, e.g. ESA assessment-study practice):
  **5%** off-the-shelf, **10%** modified, **20%** new design. AIAA S-120A gives a more
  detailed mass-growth-allowance table by maturity and subsystem; use whichever your
  programme mandates.
- Add a **system margin** (often ~20% of dry mass at early phases) on top of unit margins.
  Keep margin owned by systems, not distributed.
- Dry-mass sanity split for a conventional bus (very approximate): payload ~25–40%,
  structure ~15–25%, power ~15–30%, thermal ~3–6%, ADCS ~5–10%, TT&C ~3–5%,
  propulsion (dry) ~3–8%, harness ~3–6% (harness is the one people forget).
- Then add propellant from the delta-v budget (orbital-mechanics delta-v skill) to the
  margined dry mass, and check against the launcher capability for the target orbit.

## 2. Power budget and solar array sizing
1. Tabulate each unit's power per **mode** (safe, nominal, payload-on, downlink, eclipse)
   with duty cycles. Apply unit margins as for mass; add system margin.
2. Required array power at end of life (SMAD-style):
   `P_sa = (P_e T_e / X_e + P_d T_d / X_d) / T_d`
   with path efficiencies X_e ≈ 0.60 / X_d ≈ 0.80 for direct energy transfer, or
   ≈ 0.65 / 0.85 for peak-power tracking.
3. Array area: `P_BOL/A = S · η_cell · I_d · cos θ` with `S ≈ 1361 W/m²`, triple-junction
   cells ~28–32% BOL, inherent degradation I_d (packing, wiring, temperature) often ~0.7–0.8,
   and worst-case sun angle θ. Then `P_EOL = P_BOL (1 − d)^years`; degradation depends on
   radiation environment and cell type, so take it from the cell vendor's fluence data
   rather than a generic percent.
4. Orbit numbers: 500 km LEO period ~95 min, max eclipse ~35–36 min; GEO eclipse seasons
   around the equinoxes with a maximum of ~72 min/day.

## 3. Battery sizing
`C_Wh = P_e T_e / (DoD · n · η_discharge)` (n = number of batteries, if redundant).
- Li-ion DoD for LEO (≈ 5,500 cycles/year) is typically limited to ~20–40% to reach
  multi-year lives; GEO (~90 cycles/year) tolerates ~60–80%. Use the cell supplier's
  cycle-life curves at your temperature; these figures are indicative.
- Size for the worst eclipse **plus** any eclipse-time payload operation, and for a
  safe-mode case where attitude is lost and arrays are off-sun.

## 4. Link budget (downlink sanity)
```
Eb/N0 [dB] = EIRP + G/T − L_fs − L_atm − L_pointing − L_pol − L_impl − 10 log10(R) + 228.6
L_fs = 20 log10(4 π d / λ)
```
(228.6 is −k in dBW/(K·Hz).) Compare with the required Eb/N0 for the modulation and
coding at the target BER/FER; keep ≥ 3 dB link margin at worst-case range and elevation
(5–10°). Check the downlink data volume per day against passes actually available.

## 5. Thermal sanity
Single-node balance: `α S A_proj + Q_albedo + Q_IR + Q_internal = ε σ A_rad T⁴`. Solve for hot
case (max sun, max dissipation, EOL coatings) and cold case (eclipse, min dissipation,
BOL coatings). Typical electronics operating range ~−20 to +50 °C, batteries much
narrower (~0–30 °C). Radiator area and heater power fall out of this before any detailed
thermal model; heater power goes back into the power budget.

## 6. ADCS quick checks
Disturbance torques (gravity gradient, solar pressure, aero drag, residual dipole) set
wheel momentum storage and magnetorquer/thruster unloading; slew requirements set wheel
torque. Feed actuator power and mass back into the budgets.

## Gotchas
- Budgets drift because each subsystem holds private margin; make CBE + margin visible.
- Peak power (simultaneous payload + transmitter + heaters) can exceed orbit-average sizing.
- Harness and brackets are routinely 5–10% of dry mass that early estimates omit.

## Verify
- [ ] Every mass and power line has CBE, maturity, margin and a source.
- [ ] System margin held centrally and above programme minimum.
- [ ] Energy balance positive in every mode across worst orbit and EOL.
- [ ] Battery DoD within cycle-life limits for the mission duration.
- [ ] Link margin ≥ 3 dB at worst case; daily data volume closes.
- [ ] Hot and cold single-node cases keep units within limits, heater power budgeted.
