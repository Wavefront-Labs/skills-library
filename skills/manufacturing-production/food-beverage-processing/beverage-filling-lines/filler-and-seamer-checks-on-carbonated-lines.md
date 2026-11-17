---
id: manufacturing-production.food-beverage-processing.beverage-filling-lines.filler-and-seamer-checks-on-carbonated-lines
name: filler-and-seamer-checks-on-carbonated-lines
category: manufacturing-production
field: food-beverage-processing
product: beverage-filling-lines
tags: [beverage-filling-lines, bottling, canning-line, filler, counter-pressure-filler, isobaric-filling, carbonation, co2-volumes, carbo-qc, zahm-nagel, fill-level, fill-height, underfill, foaming, fobbing, capper, cap-torque, removal-torque, secure-seal, seamer, can-seam, double-seam, dissolved-oxygen, tpo, liquid-nitrogen-dosing, krones, khs, sidel, ferrum, oee, line-efficiency, v-graph, beer, soft-drinks, csd, sparkling-water, food-processing]
level: practitioner
status: draft
description: "Run a carbonated bottling or canning line: cold low-foam filling, CO2 volume checks, fill level, cap torque and seam checks, TPO control, and keeping the filler the bottleneck."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filler and seamer checks on carbonated lines

**Goal:** every bottle or can leaves at the right fill, carbonation and closure
integrity, at the speed the line was designed for. Covers soft drinks, sparkling water
and beer; still-drink lines drop the carbonation parts.

## 1. Product into the filler
- **Temperature**: carbonated product fills best cold (commonly ~1–4 °C for beer/CSD on
  counter-pressure fillers; warm-fill lines exist but need different settings). Warmer
  product holds less CO2 and **fobs** (foams out).
- **Carbonation**: measure CO2 volumes (or g/L) at the carbo-cooler/blender and in finished
  packs with a Zahm-Nagel-type shake test, Anton Paar CboxQC or Haffmans unit.
  1 volume ≈ 1.96–1.98 g/L. Targets e.g. ~2.5–2.8 vol beer, 3.5–4 vol cola (brand-specific).
- Bowl level and counter-pressure stable; a fluctuating bowl gives fill-height variation.

## 2. Filler (counter-pressure / isobaric)
Cycle: evacuate (on some fillers, to cut air pickup) → CO2 flush → pressurise to bowl
pressure → fill → snift (controlled pressure release) → transfer to capper/seamer.
- **Snift too fast** = foaming and low fills. **Transfer too long** = CO2 loss and foaming before the closure.
- Watch individual valves: a consistent low-fill valve usually has a worn seal, blocked
  vent tube or damaged centring bell. Tag it by number.
- Electronic fill-level inspection (X-ray/gamma or HF) after the closure rejects under/over fills; check its reject with test containers at start of shift.

## 3. Fill level and content
- Check fill height or net content per the sample plan (e.g. one container per valve
  at start, then a rotation). Regulations: average content ≥ nominal and limits on
  individual shortfalls (e.g. EU ℮ mark rules / US NIST Handbook 133 — confirm which applies).
- Over-filling is lost money; under-filling is a legal problem.

## 4. Closures
- **Crowns** (glass): crimp diameter with a crown gauge (e.g. ~28.6–28.9 mm; spec-specific).
- **Plastic screw caps (PET)**: application torque on the capper, **removal torque** measured
  on a torque tester after a set settling time, and secure-seal test (pressurised) per
  frequency. Bridges on tamper bands intact, no cocked caps.
- **Cans**: double seam visual checks and teardowns per head — same principle as
  manufacturing-production.food-beverage-processing.thermal-processing.retort-operation-and-can-seam-checks.
  Undercover gassing / liquid nitrogen dosing at the seamer reduces headspace oxygen.

## 5. Oxygen pickup (beer, juices)
Measure **TPO** (total package oxygen) periodically. Rising TPO = poor evacuation/CO2
flushing, fobbing too little before seaming (beer lines often deliberately fob with a
high-pressure water jet to push air out), or seamer gassing problems. Beer targets are
often < 100–150 ppb TPO (brewery-specific).

## 6. Line efficiency
- The **filler should be the bottleneck**, with upstream/downstream machines rated
  faster (the "V-graph"). If the filler is starved or blocked, the problem is elsewhere —
  look at accumulation tables, labeller jams, or depalletiser.
- Track OEE losses by cause (stops, speed, rejects) on the shift log rather than by memory.

## Gotchas
- Warm product after a long stop → foaming on restart; re-chill or run slower.
- Adjusting the whole filler for one bad valve.
- Testing removal torque straight off the capper (it relaxes over minutes; use the stated settling time).
- Bypassing a fill-level inspector reject to "keep the line running".
- Changeover parts (starwheels, guides) mixed between bottle sizes, causing knocked bottles and glass.

## Verify
- [ ] Product temperature and CO2 volumes within spec at start and per frequency.
- [ ] Fill level/content checks pass on every valve sampled; inspector reject challenged.
- [ ] Cap torque/secure-seal or seam checks in spec at required frequency.
- [ ] TPO measured where required and within target.
- [ ] Downtime logged with causes for the shift.
