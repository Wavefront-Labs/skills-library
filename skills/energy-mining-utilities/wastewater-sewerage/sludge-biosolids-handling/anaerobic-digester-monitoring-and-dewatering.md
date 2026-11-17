---
id: energy-mining-utilities.wastewater-sewerage.sludge-biosolids-handling.anaerobic-digester-monitoring-and-dewatering
name: anaerobic-digester-monitoring-and-dewatering
category: energy-mining-utilities
field: wastewater-sewerage
product: sludge-biosolids-handling
tags: [wastewater-sewerage, sludge-biosolids-handling, anaerobic-digestion, mesophilic-digester, vfa, volatile-fatty-acids, alkalinity, vfa-alkalinity-ratio, fos-tac, organic-loading-rate, hrt, digester-foaming, biogas, methane, h2s, sludge-thickening, dewatering, centrifuge, belt-press, polymer-dosing, cake-solids, centrate, filtrate, biosolids, sludge-cake, ds-percent]
level: practitioner
status: draft
description: "Keep a mesophilic anaerobic digester stable (VFA/alkalinity, temperature, loading, gas) and dewater digested sludge with polymer on a centrifuge or belt press."
sources:
  - "WEF MOP 8/MOP 11 sludge treatment chapters, paraphrased"
  - "US EPA Process Design Manual for Sludge Treatment and Disposal, concepts paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anaerobic digester monitoring and dewatering

**Goal:** turn thickened sludge into stable digested sludge and biogas without souring the
digester, then dewater it to a cake that's cheap to transport and meets biosolids rules.

## 1. Feed the digester steadily
- Feed little and often (ideally continuously or many small feeds per day), not one big
  slug — methanogens are slow and dislike shocks.
- Feed sludge solids typically 4–7% DS after thickening; thinner feed shortens HRT.
- **Hydraulic retention time** for mesophilic digesters is commonly ≥ 15–20 days.
- Track **organic loading rate** (kg VS/m³·d); sudden increases (e.g. imported sludge,
  fats/oils/grease) are the classic route to failure.

## 2. Daily/weekly stability checks
- **Temperature:** mesophilic ~35–37 °C; hold within about ±1 °C/day. Drift sours digesters.
- **VFA/alkalinity ratio** (also FOS/TAC): commonly stable below ~0.3 (method-dependent);
  a *rising trend* matters more than one value. Rising ratio → reduce feed now.
- **pH:** lagging indicator; by the time pH drops (< ~6.8) you're already in trouble.
- **Gas production and composition:** CH4 typically 60–65%, CO2 35–40%. Falling methane %
  and gas volume with rising CO2 = stress.
- **Volatile solids destruction** (VSD) monthly: 40–60% typical.
- **Foaming and level** — foaming lifts into gas lines; check level indicators and sight glasses.

## 3. Responding to a souring digester
1. Cut or stop feed.
2. Confirm temperature and mixing working.
3. Add alkalinity (sodium bicarbonate is common, it doesn't overshoot) if pH is falling.
4. Recover slowly — resume feed at reduced rate as VFA/alk falls.
5. Find the cause: toxic discharge, grease slug, temperature loss, mixer failure.

## 4. Gas safety
Biogas is flammable and contains H2S (toxic). Work under permit, use gas detectors
(LEL, H2S, O2), keep flame traps and pressure/vacuum relief valves maintained, and never
let air into the digester gas space (explosive mixture).

## 5. Dewatering
**Polymer:** make down at the supplier's concentration (often 0.1–0.5% solution), age as
recommended (~30–60 min for powder), dose in kg active per tonne DS. Jar/beaker test when
sludge changes: look for clear water and firm floc.
**Centrifuge:** tune feed rate, polymer dose, differential speed (scroll vs bowl) and pond
depth. Lower differential → drier cake but higher torque; watch torque and centrate solids.
**Belt press:** set belt speed and tension, check gravity zone drainage, keep wash sprays clear.
Measure **cake DS%** (often 18–30% for digested sludge) and **capture** (centrate/filtrate
solids low). Centrate is high in ammonia — return it to works steadily, not in slugs.

## Gotchas
- Overdosing polymer gives slimy cake and sticky belts and wastes money.
- Digested sludge struvite scales pipes and centrifuges; watch for narrowing pipes.
- Grit and rags wear centrifuge scrolls — screen upstream.

## Verify
- [ ] Feed regular; HRT and OLR within design.
- [ ] Temperature, VFA/alkalinity, gas volume and CH4% trended.
- [ ] Gas safety permits, detectors and relief valves in order.
- [ ] Cake DS% and centrate quality tested; polymer use per tonne DS tracked.
- [ ] Biosolids treatment/storage meets local land-application or disposal rules.

*Uncertain:* VFA/alk thresholds depend on the titration method; temperature and retention
targets vary with design and regulation (e.g. pathogen-reduction classes).
