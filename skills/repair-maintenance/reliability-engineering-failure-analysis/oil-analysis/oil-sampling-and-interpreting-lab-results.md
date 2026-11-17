---
id: repair-maintenance.reliability-engineering-failure-analysis.oil-analysis.oil-sampling-and-interpreting-lab-results
name: oil-sampling-and-interpreting-lab-results
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: oil-analysis
tags: [oil-analysis, lubricant-analysis, condition-monitoring, predictive-maintenance, oil-sampling, sample-valve, minimess, vacuum-pump-sampling, wear-metals, icp, spectrometric-analysis, particle-count, iso-4406, viscosity, tan, tbn, water-content, karl-fischer, oxidation, ftir, ferrography, pq-index, contamination, silicon-dirt, gearbox, hydraulics, engine-oil]
level: practitioner
status: draft
description: "Take representative oil samples, choose the right test slate, and read wear metals, ISO 4406 particle counts, viscosity, water and acid numbers to decide what to do on the machine."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oil sampling and interpreting lab results

**Goal:** use lubricant analysis to catch wear, contamination and degraded oil
early — which starts with a sample that actually represents the oil in the machine.

> Draft: limits below are typical industrial starting points; OEM limits, lab
> flagging and your own trend data override them. Labs differ in methods and units.

## 1. Sample properly (most bad results are bad samples)
- **Location:** live zone — turbulent flow, **after** the components, **before** the
  filter: e.g. a sample valve (minimess-type with probe) on the return line of a
  hydraulic system, or a valve on the gearbox's circulating line. Second choice: a
  vacuum pump with a tube inserted to mid-depth of the sump, same depth every time,
  away from the bottom sludge.
- **Never from the drain plug** (water and debris settle there) except to look for
  free water specifically.
- **Running machine at operating temperature** or within ~30 min of stopping.
- **Flush** the valve/tube first: discard 5–10× the dead volume.
- Clean, lab-supplied bottles (particle count needs certified-clean bottles); fill
  ~75–80%; cap immediately.
- **Label completely:** asset ID, sample point, date, oil brand/grade, hours on oil and
  on machine, top-ups since last sample. Without hours, wear rates can't be read.
- **Same point, same method, same interval** — trends need consistency. Typical
  interval: monthly to quarterly for critical gearboxes/hydraulics, per oil change or
  250–500 h for engines.

## 2. Pick the test slate
| Machine | Core tests |
|---|---|
| Gearbox | ICP elements, viscosity @40 °C, water, PQ index/ferrous density, TAN |
| Hydraulic | particle count (ISO 4406), water (Karl Fischer, ppm), viscosity, ICP |
| Engine | ICP, viscosity @100 °C, fuel dilution, soot, TBN, glycol |
| Turbine | TAN, RPVOT/MPC (oxidation, varnish), water, particle count |
Add **analytical ferrography** when an abnormal wear result needs the wear mode
(cutting, fatigue, sliding).

## 3. Read the results
**Wear metals (ppm, ICP — detects particles < ~5–8 µm only):**
- Fe: gears, shafts, bearings, cylinders. Cu: bronze bushes, cages, coolers.
  Pb/Sn: babbitt bearings. Cr: rings, plated rods, some bearings. Al: pistons,
  housings, pump parts.
- Judge **rate of change** (ppm per 100 h) against the machine's own history, more
  than absolute value.
- **Large particles don't show in ICP** — a low Fe with high PQ index = severe wear
  making big particles. Act on that.

**Contamination:**
- **Si (silicon) + Al** rising together = dirt ingress (breathers, seals). Si alone can
  be anti-foam additive — compare with new oil.
- **Na, K, B** rising = coolant (glycol) or water with additives.
- **Water:** hydraulics/turbines often target < 200–500 ppm; gearboxes < 500–1000 ppm.
  Free water (cloudy) = act now.
- **ISO 4406 particle count** `21/19/16` = codes for ≥4/≥6/≥14 µm per mL. Each step of
  1 code ≈ doubling. Typical hydraulic targets 17/15/12 or cleaner for servo valves.

**Oil condition:**
- **Viscosity:** ±10% of new = caution, ±20% = change. Up = oxidation, contamination
  or wrong top-up; down = shear, fuel dilution, wrong oil.
- **TAN** (acid) rise of ~+1–2 mg KOH/g over new = oxidised; **TBN** (engines) below
  ~50% of new = reserve depleted.
- Additive elements (Zn, P, Ca, Mo) changing suddenly = wrong oil topped up.

## 4. Act
- Dirt → fix breathers (desiccant breathers), seals, top-up practice (filter cart).
- Water → find source (cooler leak, washdown, condensation), dry the oil or change.
- Abnormal wear rising → shorten sample interval, add vibration/inspection, plan
  intervention.
- Degraded oil → change, and ask why it degraded (temperature, contamination).
- Always **re-sample after corrective action** to confirm.

## Gotchas
- Top-ups dilute wear metals — record them or the trend lies.
- Sampling right after an oil change shows "great" results that mean nothing.
- Dirty sample valves or reused bottles give false high particle counts.
- One alarming sample: resample before tearing down a machine.

## Verify
- [ ] Sample point in live zone before filter, flushed, machine warm.
- [ ] Bottle labelled with asset, point, oil, hours on oil, top-ups.
- [ ] Tests match the machine type.
- [ ] Results judged on trend/rate, plus PQ for large particles.
- [ ] Action taken and confirmed by a follow-up sample.
