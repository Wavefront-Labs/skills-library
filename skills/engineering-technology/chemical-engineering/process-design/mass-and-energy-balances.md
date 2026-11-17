---
id: engineering-technology.chemical-engineering.process-design.mass-and-energy-balances
name: mass-and-energy-balances
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, mass-balance, material-balance, energy-balance, heat-balance, degrees-of-freedom, recycle, purge, bypass, conversion, selectivity, yield, enthalpy, heat-of-reaction, reference-state, utilities, design-basis, stream-table, pfd, spreadsheet, aspen-plus, hysys, dwsim]
level: practitioner
status: verified
description: "Close plant-wide mass and energy balances: basis, degrees of freedom, recycle/purge arithmetic, enthalpy reference states, utility loads and closure checks."
sources:
  - "Felder and Rousseau, Elementary Principles of Chemical Processes (textbook, method only)"
  - "Towler and Sinnott, Chemical Engineering Design (textbook, method only)"
  - "Worked numbers recomputed in Python (Q = 755 kW, 1,294 kg/h steam at 2,100 kJ/kg, 65 m3/h cooling water at 10 K, purge 5 kmol/h); steam latent heat from the iapws package"
  - "https://dwsim.org/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mass and energy balances for a process flowsheet

**Goal:** a stream table that closes on mass, on each element and on energy, built from a
written design basis, so every downstream sizing step starts from numbers you trust.

## 1. Fix the basis before any arithmetic
Write down: product rate and spec, **operating hours** (state yours, for example 8,000 h/y is 91% on-stream), feed compositions, conversion/selectivity
sources, utility conditions (steam levels, cooling-water supply/return, e.g. 30 → 40 °C),
and ambient. Pick a calculation basis (e.g. 100 kmol/h fresh feed) and scale at the end.

## 2. Degrees of freedom per unit
DOF = unknowns − independent equations (component balances + specified relations). Count
it for each unit and the overall plant. DOF > 0: you are missing a spec; DOF < 0: you have
over-specified and will get contradictions. Solve the unit with DOF = 0 first, then
march outwards.

## 3. Reaction terms
Use extent of reaction ξ: n_i,out = n_i,in + Σ ν_ij ξ_j. Define clearly:
- conversion X = reacted / fed (per pass vs overall — say which),
- selectivity S = desired product / undesired product (or per key reactant consumed),
- yield Y = desired formed / reactant fed (× stoichiometric ratio).
Do an **atom balance** check (C, H, O, N) on the reactor; it catches stoichiometry typos.

## 4. Recycle and purge arithmetic
Solve the overall balance first (recycle is internal and cancels), then the reactor and
splitter. For an inert I entering with fresh feed at F·z_I and leaving only via purge P at
mole fraction y_I: F·z_I = P·y_I. Worked mini-example: fresh feed 100 kmol/h with 0.5% argon,
and you want ≤ 10% argon in the loop: P = 100·0.005/0.10 = 5 kmol/h of purge, and the purge
also carries reactant you lose. That trade (purge loss vs recycle compressor size) is a
design decision; plot it.
Single-pass conversion X_pass and overall conversion relate as X_overall ≈ 1 if recycle is
complete; low X_pass means large recycle: recycle ≈ F·(1 − X_pass)/X_pass per unit fresh
reactant when nothing is purged.

## 5. Energy balance
Steady flow: Q − W_s = Σ n·h_out − Σ n·h_in (kinetic/potential terms negligible for most
process units). Choose one **reference state** and keep it: either elements at 25 °C
(heat of formation method, reaction heat comes out automatically) or compounds at 25 °C
(add ξ·ΔH_r° explicitly). Mixing the two double-counts the heat of reaction.
Sensible heat: ∫Cp dT; latent heat at the actual phase-change temperature (adjust with
Watson's correlation if far from the normal boiling point).
Worked: heating 10,000 kg/h of water from 25 to 90 °C: Q = 10,000·4.18·65 ≈ 2.72 GJ/h ≈
755 kW. With 4 barg steam (latent heat 2,085 kJ/kg at 5 bar absolute, computed from IAPWS-97) that is about
1,300 kg/h of steam.

## 6. Utilities
Convert every duty to utility flow: cooling water m = Q/(Cp·ΔT) (755 kW at 10 K rise →
≈ 65 m³/h), steam by latent heat, refrigeration by COP, electricity from shaft work/η.
Sum per utility; this list becomes the utility design basis and the opex screen.

## 7. Tools
Spreadsheet first for insight (one sheet per unit, a stream table sheet), then a simulator
(Aspen Plus/HYSYS, DWSIM) for rigorous properties. When they disagree by more than a few
percent, find out why; don't just take the simulator's number.

## Gotchas
- Mass is conserved, moles are not when reactions occur. Check closure in kg.
- Water of reaction, dissolved gases and entrained solids are the usual "missing" streams.
- Volumetric flows depend on T, P; tabulate at actual and standard conditions and label which.
- Rounding: carry 4+ significant figures in the table, round only in the report.

## Verify
- [ ] Written design basis with operating hours, specs and utility conditions.
- [ ] DOF = 0 for every unit and overall.
- [ ] Overall and per-unit mass closure < 0.1% in kg; atom balances close.
- [ ] Purge/recycle trade-off justified with numbers.
- [ ] One consistent enthalpy reference; energy balance closes; ΔH_r sign checked (exothermic negative).
- [ ] Utility summary derived from duties, units stated.
