---
id: engineering-technology.chemical-engineering.heat-exchanger-design.shell-and-tube-thermal-design
name: shell-and-tube-thermal-design
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, shell-and-tube, sthe, heat-exchanger, lmtd, f-factor, correction-factor, overall-heat-transfer-coefficient, fouling, fouling-factor, tema, aes, bem, aeu, fluid-allocation, tube-side, shell-side, kern, bell-delaware, pressure-drop, tube-vibration, overdesign, rating, htri, hysys, aspen-edr, exchanger-sizing]
level: practitioner
status: draft
description: "Thermally design a shell-and-tube exchanger: duty, LMTD and F-factor, TEMA type, fluid allocation, U and fouling, area, velocities, pressure drop and margins."
sources:
  - "TEMA Standards (current edition), for type designations and fouling guidance"
  - "Kern, Process Heat Transfer; Bell-Delaware method as summarised in standard design texts (method only)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shell-and-tube exchanger thermal design

**Goal:** from a duty and four terminal temperatures, get a TEMA type, a defensible area,
and a geometry whose velocities and pressure drops pass, ready for rating in HTRI or
Aspen EDR.

## 1. Duty and terminal temperatures
Q = m·Cp·ΔT on each side (or m·λ for phase change); the two must agree within 1–2%.
Set approach temperatures realistically: ≥ 10 K for liquid–liquid, 5 K only with
counter-current, 20 K+ for gas service as a screening start.

## 2. LMTD and F
LMTD = (ΔT₁ − ΔT₂)/ln(ΔT₁/ΔT₂), counter-current basis.
R = (T_h,in − T_h,out)/(t_c,out − t_c,in), P = (t_c,out − t_c,in)/(T_h,in − t_c,in).
Get F from the 1-2 (one shell, two or more tube passes) chart or formula. **Keep F ≥ 0.80**;
below that, and especially where the curve is steep, add shells in series or go to a
counter-current (F-type shell, or two shells). A temperature cross in a single 1-2 shell is
the classic error.

## 3. Choose TEMA type and allocate fluids
- **BEM** (fixed tubesheet): cheap, clean shell fluid, ΔT between shell and tubes modest
  (roughly < 50 K without an expansion joint; check differential expansion).
- **AES** (floating head): dirty shell side, large ΔT, bundle removable.
- **AEU** (U-tube): high pressure, clean tube side (U-bends are hard to clean mechanically).
Tube side gets: the fouling/corrosive fluid (cooling water), the higher-pressure fluid, the
fluid needing expensive alloy. Shell side gets: viscous fluids (baffles raise h), condensing
vapour, the fluid with low allowable ΔP.

## 4. U, fouling and area
1/U_o = 1/h_o + R_fo + (D_o ln(D_o/D_i))/(2k_w) + R_fi·(D_o/D_i) + (1/h_i)(D_o/D_i).
Start with a typical U (e.g. light oil/water ≈ 300–500 W/m²K, water/water ≈ 800–1,500,
condensing steam/water ≈ 1,500–3,000; ranges are indicative, refine once h is calculated).
Fouling: use the TEMA guidance or plant data; treated cooling water is typically on the
order of 0.0002–0.0004 m²K/W. Don't stack fouling on top of a large area margin; that's
double counting and causes low-velocity, faster fouling.
A = Q/(U·F·LMTD).

## Worked example
Cool 20 kg/s oil (Cp 2.5 kJ/kgK) 150 → 90 °C with cooling water 30 → 40 °C.
Q = 20·2.5·60 = 3,000 kW; water = 3,000/(4.18·10) ≈ 72 kg/s.
ΔT₁ = 110, ΔT₂ = 60 → LMTD ≈ 82.5 K. R = 6, P = 0.083 → F ≈ 0.98.
U = 400 W/m²K → A = 3.0e6/(400·0.98·82.5) ≈ 93 m².
¾-in (19.05 mm) OD tubes, 6.1 m: 0.365 m² each → ≈ 255 tubes. Water in tubes; choose passes
so tube velocity is 1.5–2.5 m/s (keep cooling water ≥ ~1 m/s to limit fouling).

## 5. Geometry and hydraulics
- Tubes: 19.05 or 25.4 mm OD, triangular pitch 1.25·D_o (square/rotated square if shell
  side needs mechanical cleaning).
- Baffle cut 20–30%; spacing 0.2–1.0 × shell ID (TEMA sets minimum and maximum unsupported
  span).
- Allowable ΔP: liquids commonly 0.35–0.7 bar per side, gases 0.05–0.2 bar; set by the
  process, not habit.
- Shell-side h and ΔP: Kern for quick estimates; Bell-Delaware or stream analysis (HTRI)
  for design, because bypass and leakage streams can cut h_o by 30–50%.
- Check **flow-induced tube vibration** and rho-v² at the inlet nozzle (impingement plate
  or entrance area per TEMA). This needs HTRI/EDR or an equivalent method; don't hand-wave it.

## 6. Margin and network context
Typical overdesign 10–20% on clean-to-dirty area after fouling, stated explicitly. Before
fixing duty, check the exchanger against the pinch: don't transfer heat across it.

## Verify
- [ ] Both sides' duties agree; LMTD and F computed; F ≥ 0.80, no temperature cross.
- [ ] TEMA type and fluid allocation justified in one line each.
- [ ] Fouling from TEMA/plant data; margin stated and not double counted.
- [ ] Velocities, ΔP within allowables on both sides.
- [ ] Rated in HTRI/EDR including vibration and nozzle checks.
