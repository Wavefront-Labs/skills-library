---
id: manufacturing-production.food-beverage-processing.thermal-processing.retort-operation-and-can-seam-checks
name: retort-operation-and-can-seam-checks
category: manufacturing-production
field: food-beverage-processing
product: thermal-processing
tags: [thermal-processing, canning, retort, retorting, steam-retort, water-immersion-retort, water-spray-retort, rotary-retort, scheduled-process, process-authority, initial-temperature, come-up-time, venting, mig, mercury-in-glass, reference-thermometer, tdt, f0, low-acid-canned-food, lacf, 21-cfr-113, acidified-foods, 21-cfr-114, double-seam, seam-teardown, countersink, overlap, body-hook, cover-hook, seam-tightness, pasteurisation, tunnel-pasteuriser, better-process-control-school, process-deviation, food-processing]
level: practitioner
status: verified
description: "Operate a retort to the scheduled process (venting, come-up, hold, cooling), keep records that satisfy LACF rules, handle process deviations, and run double-seam teardown checks on cans."
sources: ["21 CFR 113.10, 113.40, 113.60, 113.87 and 113.89 (eCFR, ecfr.gov)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retort operation and can seam checks

**Goal:** every container receives at least the lethality its **scheduled process**
specifies, and the seal holds afterwards. Underprocessing low-acid canned food risks
*Clostridium botulinum* — this is the one place on a food line where "close enough" can
kill someone. Process design (F0, heat penetration) is covered in
engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.thermal-process-lethality-design;
this skill is the floor operation.

## 1. The scheduled process
Set by a **process authority** for one product, container size, retort type and fill.
It specifies: minimum **initial temperature (IT)**, venting schedule (steam retorts),
**process time and temperature**, critical factors (fill weight, headspace, viscosity,
max solids, rotation speed for agitating retorts). You run it; you don't modify it. In
the US, LACF operators must be supervised by someone who completed an approved school
(Better Process Control School) under 21 CFR 113.10. Only the process authority sets or changes the scheduled process; US deviations follow 21 CFR 113.89 (fully reprocess, or set aside for evaluation by a competent processing authority).

## 2. Running a batch (still steam retort, typical)
1. Check critical factors on the batch: fill weight, headspace, IT of the **coldest**
   container going in.
2. Load baskets with the specified spacing/divider sheets; heat-sensitive indicator tape on each basket.
3. Close door, start the **vent**: vent open until **both** the specified time and
   temperature have been reached — air pockets are cold spots.
4. **Come-up** to process temperature; process timing starts only when the reference
   thermometer reads at or above process temperature (not at steam-on).
5. **Hold**: watch the reference thermometer (MIG or an approved RTD/temperature-indicating
   device) — that, not the recorder chart, is the official temperature (21 CFR 113.40: the temperature-indicating device, not the recording device, is the reference instrument). Read and record
   it at the start and at intervals; compare with the recorder.
6. **Cool** with pressure control so containers don't buckle or peak (overpressure
   with water/air; pouches and plastic containers are especially sensitive).
7. Record retort number, batch, times, temperatures, and initial the chart.

Water immersion, water spray and rotary retorts work differently (water level,
circulation, overpressure, rotation speed as a critical factor), but the record logic is the same.

## 3. Process deviations
If temperature drops below scheduled during hold, timing was wrong, or IT was low:
- Follow the written deviation procedure — often either **restart the full process** or
  apply an alternative process **filed with/approved by** the process authority.
- Otherwise **hold the lot** and get the process authority to evaluate. Never release
  underprocessed lots on judgement.
- Log the deviation, the action and the disposition.

## 4. Double-seam checks (metal cans)
- **Visual** checks at the seamer at frequent intervals (21 CFR 113.60 says intervals not to
  exceed 30 minutes, plus after any jam in the closing machine): look for droop, vee, sharp edges,
  cut-overs, false seams, wrinkles.
- **Teardown** by a qualified person at intervals not to exceed 4 hours (21 CFR 113.60) — measure:
  - seam thickness, width (length), countersink depth
  - after strip: body hook, cover hook, **overlap**, **tightness** (wrinkle rating)
  - optical seam projector/saw (e.g. Quality By Vision SEAMetal, CMC-Kuhnke) or micrometer
- Compare with the can maker's specification. Overlap and tightness are the main
  integrity indicators.
- Out of spec: stop the seamer head, hold product since the last good check, adjust (seaming rolls, chuck, pin height), re-check.

## Gotchas
- Starting the timer at steam-on instead of at temperature.
- Hot product sitting until cool before the retort → IT below scheduled.
- A blocked bleeder or vent valve on a steam retort.
- Chart recorder reading higher than the MIG — trust the MIG and investigate the recorder.
- Mixing processed and unprocessed baskets (that's what the heat-sensitive tape is for).

## Verify
- [ ] Scheduled process for this product/container is posted at the retort and matches the recipe.
- [ ] IT measured on the coldest container; venting met both time and temperature.
- [ ] Hold timed from reference thermometer reaching process temperature; readings logged.
- [ ] Any deviation held and evaluated by the process authority.
- [ ] Seam visuals and teardowns done at required frequency and in spec.
