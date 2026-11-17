---
id: engineering-technology.mining-geological-engineering.mineral-processing.comminution-circuit-sizing
name: comminution-circuit-sizing
category: engineering-technology
field: mining-geological-engineering
product: mineral-processing
tags: [mining-geological-engineering, mineral-processing, metallurgy, comminution, grinding, crushing, bond-work-index, bwi, rwi, f80, p80, ball-mill, sag-mill, ab-mill, hpgr, rowland-correction-factors, smc-test, axb, drop-weight-test, critical-speed, circulating-load, hydrocyclone, mass-balance, two-product-formula, jksimmet, moly-cop-tools, geometallurgy, specific-energy]
level: practitioner
status: draft
description: "Size a crushing-grinding circuit with Bond's work index: specific energy from F80/P80, correction factors, mill power, SAG/ball circuit choices and a mass-balance check."
sources:
  - "Bond (1961), Crushing and grinding calculations, British Chemical Engineering"
  - "Rowland and Kjos, Rod and ball mills, in Mineral Processing Plant Design (SME)"
  - "Wills and Finch, Wills' Mineral Processing Technology"
  - "Napier-Munn, Morrell, Morrison and Kojovic, Mineral Comminution Circuits (JKMRC)"
  - "Morrell (2004), An alternative energy-size relationship to that proposed by Bond"
  - "SME Mineral Processing and Extractive Metallurgy Handbook"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comminution circuit sizing — Bond energy, mill power and the mass balance

**Goal:** estimate the specific energy and installed power for a crushing and
grinding circuit from ore-hardness tests, choose a sensible circuit, and confirm it
with a closed mass balance.

## 1. Gather the design inputs
- Throughput (t/h) = annual tonnes ÷ (8760 h × availability; grinding often ~92–94%).
- Target **P80** from flotation/leach liberation testwork (often 75–212 µm).
- Hardness: Bond ball mill work index (BWi), rod mill (RWi), crushing (CWi), plus
  SAG tests (SMC Test A×b / Mia, JK drop-weight, or SPI). Test enough samples to see
  variability and design on the **75th–90th percentile**, not the mean.
- Typical BWi: soft 7–9, medium 10–14, hard 15–20+ kWh/t (check the units — US data
  are often kWh/short ton; multiply by 1.1023 for kWh/tonne).

## 2. Bond specific energy
```
W = 10 · Wi · (1/√P80 − 1/√F80)        W kWh/t, sizes in µm
```
Worked example: BWi 14, F80 2000 µm (ball-mill feed after SAG/crushing), P80 106 µm:
W = 10 × 14 × (0.0971 − 0.0224) ≈ 10.5 kWh/t. At 500 t/h → ~5.2 MW at the pinion,
before correction factors and drive losses.

## 3. Apply Rowland correction factors (EF1–EF8)
Bond's equation is calibrated to a wet, closed-circuit, 2.44 m (inside liners) ball
mill. Correct for differences:

| Factor | Applies when | Typical form |
|---|---|---|
| EF1 | dry grinding | × 1.3 |
| EF2 | open-circuit ball milling | 1.035–1.7, grows with product control demand |
| EF3 | mill diameter ≠ 2.44 m | (2.44/D)^0.2, floor 0.914 for D ≥ 3.81 m |
| EF4 | feed coarser than optimum | depends on Wi and reduction ratio |
| EF5 | fine grind, P80 < 75 µm | (P80 + 10.3)/(1.145·P80) |
| EF6–EF8 | rod-mill reduction ratio and rod-mill circuits | see Rowland tables |

For the example, a large ball mill gets EF3 = 0.914 → ~9.6 kWh/t. Divide pinion
power by drive efficiency (~0.93–0.97) for motor power and leave a margin (often 5–15%).

## 4. Choose the circuit
- **SABC** (SAG, ball mill, pebble crusher) is common for large tonnage; Bond alone
  does not size SAG mills well — use SMC/JK-based methods (e.g. Morrell's
  `W = Mi·4·(x2^f(x2) − x1^f(x1))`, f(x) = −(0.295 + x/10⁶), x in µm) or vendor
  pilot/simulation work.
- **Crush + HPGR + ball** suits hard, competent ore and lowers specific energy, at the
  cost of more materials handling and dust control.
- Ball mill setting: speed 65–80% of critical, `Nc = 42.3/√(D − d)` rpm (D mill, d ball
  diameter, m); ball load commonly ~30–40% of mill volume; cyclone closing with
  circulating load ~200–350%.

## 5. Close the mass balance
- **Circulating load** from cyclone size fractions (f feed, u underflow, o overflow,
  % passing a chosen size): `U/O = (o − f)/(f − u)`; check across several sizes and
  reconcile (least squares — tools like JKSimMet, Moly-Cop Tools, HSC Sim, METSIM).
- **Two-product formula** for concentrator recovery downstream:
  `R = c(f − t) / (f(c − t))` (grades of feed f, concentrate c, tails t).
- Balance water as well as solids; cyclone feed density drives classification.

## Gotchas
- The Bond test closing screen must match the target P80; a BWi run at a coarser
  screen understates fine-grind energy.
- F80 after a SAG mill with pebble crushing is bimodal; one F80 number misleads.
  Use simulation for SAG-ball transfer size.
- Variability matters more than the average: a hard domain later in the mine plan can
  cut throughput by 20% or more. Feed geometallurgical hardness into the mine schedule.
- Comparing work indices across labs: confirm test procedure and units.
- Over-grinding wastes energy and can hurt flotation (slimes); confirm the P80 target.

## Verify
- [ ] Hardness tested on enough samples; design percentile stated.
- [ ] Specific energy computed and Rowland factors applied with each one justified.
- [ ] SAG/HPGR sized with an appropriate (non-Bond) method or vendor simulation.
- [ ] Circulating load reconciles across at least three size classes.
- [ ] Installed motor power includes drive losses and stated margin.
