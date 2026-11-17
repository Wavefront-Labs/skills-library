---
id: manufacturing-production.chemical-process-manufacturing.chemical-blending-formulation.weigh-up-addition-order-and-in-spec-adjustment
name: weigh-up-addition-order-and-in-spec-adjustment
category: manufacturing-production
field: chemical-process-manufacturing
product: chemical-blending-formulation
tags: [chemical-blending-formulation, blending, compounding, formulation, batch-blending, weigh-up, dispensing, load-cell, scale-calibration, addition-order, mixing, high-shear-mixer, disperser, agitator, tip-speed, mix-time, viscosity, ph-adjustment, specification, in-spec-adjustment, correction-calculation, rework, coatings, adhesives, detergents, lubricants, personal-care-manufacturing]
level: practitioner
status: draft
description: "Make a production blend to formula: accurate weigh-up, correct addition order, mixing parameters that actually disperse, QC sampling, and calculating a correction when a property is off spec."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Production blending: weigh-up, addition order and in-spec adjustment

**Goal:** turn a formula sheet into a blend that passes QC first time, and when it
doesn't, correct it by calculation rather than by guesswork.

## 1. Weigh-up
- **Scale fit for the charge:** weigh on a scale whose readability is ≤ about 0.1% of
  the charge (a 2 kg additive does not belong on a 3-tonne floor scale). Check the
  scale's daily check-weight record before use.
- **Tare properly** — container on, tare, then charge. Record gross/tare/net where the
  batch sheet asks.
- **Minor ingredients** (catalysts, biocides, dyes, fragrances) usually dominate
  property variation per kilogram; pre-weigh them in a controlled dispensing area into
  labelled containers and have them second-checked.
- **Correct material and lot:** scan or read code and lot against the batch sheet. Many
  materials look identical (white powders, clear liquids).
- **Bulk liquids by meter:** a meter total is only as good as its calibration and
  whether the line was full at start; confirm big charges with vessel load cells or
  level change.

## 2. Addition order (why the sheet says what it says)
The order is chemistry, not habit. Typical reasons:
- **Solubility/wetting:** dissolve or disperse solids in the phase that wets them,
  before adding components that would make them clump (e.g. thickeners into water
  before salts).
- **Heat of mixing:** acids/bases diluted by adding them to water slowly.
- **Reactivity and stability:** pH-sensitive or heat-sensitive components (fragrances,
  enzymes, some preservatives) go in late, after cooling or neutralising.
- **Viscosity build:** add thickener when the mixer can still turn the batch over;
  adding it too early can stall low-power agitators.
Never swap order without a formulation change approval: some sequences (e.g. adding
an electrolyte before a polymer has hydrated) give a batch that cannot be fixed.

## 3. Mixing parameters
- **Powder addition:** into the vortex, at a rate the surface can wet — dumping a bag
  makes "fish-eyes" (wet outside, dry core) that never disperse. Use an eductor or
  powder induction unit where fitted.
- **Dispersers:** effectiveness scales with tip speed (blade circumference × rpm);
  typical high-speed disperser practice is in the region of 18–25 m/s, but follow
  equipment guidance. Blade diameter and position relative to vessel diameter and fill
  level matter as much as speed.
- **Mix time** is a minimum, not a target. A blend is mixed when samples from top and
  bottom agree (density, viscosity, solids), which you should verify on new products
  or after equipment changes.
- **Air entrainment** from a vortex inflates viscosity and density readings; let
  samples de-aerate or use a vacuum step if the process has one.

## 4. Sampling and QC
- Sample after full mix time, from a representative point, into a clean labelled container.
- Measure at the specified temperature: viscosity and density vary strongly with it.
- Record result vs spec; if in spec, release per procedure.

## 5. Calculating an adjustment
Example: a batch of 5,000 kg is at 38.0% solids; target 40.0%; you can add a 60%
solids concentrate (C). Mass balance on solids:
0.38 × 5000 + 0.60 × C = 0.40 × (5000 + C) → 1900 + 0.6C = 2000 + 0.4C → C = 500 kg.
- Check the vessel has room for the addition.
- Add **about 80% of the calculated amount**, mix, re-test, then add the rest:
  property responses are rarely perfectly linear (pH and viscosity especially).
- pH adjustment: always titrate a small known sample in the lab first to estimate
  acid/base needed, then add stepwise; pH is logarithmic and buffered systems
  surprise people.
- Record every adjustment; repeated corrections of the same property point at a
  raw-material or weigh-up problem to fix upstream.

## Gotchas
- Dilution corrects concentration but also dilutes everything else — check all specs
  after.
- A "lost" ingredient (forgotten minor) often shows only in performance tests, not
  in routine QC. Use a tick-as-you-add batch sheet.
- Heel left in the vessel from the previous batch changes the formula.

## Verify
- [ ] Scale check-weight passed; minors second-checked.
- [ ] Addition order followed exactly; each addition ticked with time.
- [ ] Top/bottom samples agree before QC sample.
- [ ] Any correction calculated by mass balance, added in steps, re-tested.
- [ ] Batch record complete with actual weights and adjustments.

*Draft note:* tip-speed range and the 80% rule are common practice heuristics, not
universal values; formulation-specific guidance overrides them.
