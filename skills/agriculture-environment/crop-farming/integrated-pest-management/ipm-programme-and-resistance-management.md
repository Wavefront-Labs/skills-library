---
id: agriculture-environment.crop-farming.integrated-pest-management.ipm-programme-and-resistance-management
name: ipm-programme-and-resistance-management
category: agriculture-environment
field: crop-farming
product: integrated-pest-management
tags: [integrated-pest-management, ipm, iwm, integrated-weed-management, resistance-management, herbicide-resistance, insecticide-resistance, fungicide-resistance, mode-of-action, moa-groups, hrac, wssa, irac, frac, herbicide-groups, mixtures, double-knock, harvest-weed-seed-control, chaff-lining, narrow-windrow-burning, seed-destructor, crop-competition, biological-control, beneficial-insects, refuges, bt-crops, resistance-testing]
level: practitioner
status: gated
description: "Build an IPM programme for weeds, insects and diseases: layer cultural, biological and chemical tactics, rotate and mix modes of action (HRAC/IRAC/FRAC), and test for and contain resistance."
sources: ["https://ipm.ifas.ufl.edu/pdfs/Appendix6-FRAC.pdf", "https://www.frac.info/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPM programme and resistance management

**Goal:** keep weeds, insects and diseases below economic damage for many seasons,
not just this one. Every pesticide use selects for resistance; IPM keeps the selection
pressure low by never relying on one tactic.

## 1. The layers (use several on every problem)
1. **Prevention / cultural:** rotation (see crop-rotation-planning), clean seed,
   machinery hygiene between fields, resistant varieties, sowing time, residue
   management, removing green bridges.
2. **Crop competition:** higher seeding rates, narrower rows, competitive varieties,
   early vigour, good nutrition — a competitive crop suppresses weeds measurably.
3. **Monitoring + thresholds:** treat only when scouting says it pays (see
   crop-scouting).
4. **Biological:** conserve beneficials (avoid broad-spectrum insecticides early in the
   season; selective products; field margins and habitat), released biocontrol agents.
5. **Chemical**, used to support the above — with mode-of-action discipline.

## 2. Mode-of-action discipline
Classification schemes put products into groups by target site:
- Herbicides: **HRAC/WSSA** groups (numbering now aligned to numeric groups globally;
  older letter codes still appear on some labels).
- Insecticides: **IRAC** groups.
- Fungicides: **FRAC** codes (e.g. 3 = DMIs/"azoles", 7 = SDHIs, 11 = QoIs/strobilurins).
The group is on the label. Products with different trade names and active ingredients
can share a group — **rotate groups, not brands.**

Rules of thumb:
- Don't use the same group on the same pest generation/weed cohort twice in a row
  where alternatives exist; follow label limits on number of applications per season.
- **Mixtures** of effective groups (both active alone on the target at full rate)
  delay resistance better than alternating in many cases — especially for herbicides
  and high-risk fungicides (single-site FRAC groups usually partnered with a different
  group or a multi-site).
- **Full label rates** on the right stage. Under-dosing selects for partial resistance
  (especially documented for some grass weeds).
- High-risk groups (e.g. FRAC 11, many Group 1/A and 2/B herbicides for some weeds (gated: unconfirmed, source is paywalled or blocked))
  need the strictest limits.

## 3. Weeds specifically
- **Double knock:** two different groups (or herbicide then tillage) close together
  so survivors of the first are killed by the second — e.g. glyphosate followed some
  days later by a paraquat-based product (check label intervals and local practice).
- **Pre-emergent residuals** of different groups at sowing to cut the seedbank cohort.
- **Harvest weed seed control (HWSC):** chaff carts, chaff lining/decks, narrow windrow
  burning, or impact mills (seed destructors) to remove weed seed retained on the plant
  at harvest. Works on weeds that hold seed until harvest (e.g. annual ryegrass,
  wild radish); less on early shedders.
- **Crop topping / hay freezing / brown manuring** to stop seed set.
- Aim at the **seed bank**: zero seed set from survivors; patrol and hand-rogue escapes.

## 4. Insects and diseases
- Insects: spray only above threshold, prefer selective chemistry, respect
  **refuge requirements** for Bt crops, and rotate IRAC groups between generations.
- Diseases: resistant varieties first; fungicides timed to key leaf stages; FRAC
  limits per season; seed treatment for seedborne disease.

## 5. Test and contain resistance
Suspect resistance when a correctly applied product at the right rate and stage fails
on one species while others die, in patches that grow year to year.
1. Rule out application error (rate, coverage, water quality, weather, stage).
2. Collect seed (weeds) or samples (insects/pathogen) and send for a **resistance
   test** (university/commercial labs). Some offer quick tests on live plants.
3. Contain: stop the failing group on that population, prevent seed set, clean
   machinery leaving the patch, map it.

## 6. Keep records
Per field per year: products, groups, rates, timing, target, efficacy notes. Without
this you can't see a group being overused.

## Gotchas
- A tank mix with one ineffective partner is effectively a single group.
- Glyphosate-resistant weeds now exist in many cropping regions; relying on it alone
  for fallow control is a known path to resistance.
- Spraying beneficials out early often causes the secondary pest outbreak you then pay
  to fix.

## Verify
- [ ] Each target problem has at least two non-chemical tactics in the plan.
- [ ] Spray records show group codes; no group used repeatedly on the same target without alternation/mixture.
- [ ] Full label rates applied at the labelled stage.
- [ ] Weed seed set from survivors prevented (HWSC or other).
- [ ] Suspected failures sent for resistance testing before re-spraying the same group.

## Checked

- Date: 2026-10-25. Jurisdiction: international classification schemes (FRAC, HRAC, IRAC); no single jurisdiction.
- Confirmed against: FRAC codes 3 (DMI), 7 (SDHI) and 11 (QoI/strobilurin) and FRAC 11 as a high resistance risk (UF IFAS and university extension FRAC lists; FRAC revises its list yearly, so check frac.info for current codes).
- Not confirmed: the herbicide group numbers and letters named as high resistance risk (HRAC pages were not fetched).

Method: documentation only; no commands were run.
