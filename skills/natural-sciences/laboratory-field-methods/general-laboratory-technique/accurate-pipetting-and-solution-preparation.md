---
id: natural-sciences.laboratory-field-methods.general-laboratory-technique.accurate-pipetting-and-solution-preparation
name: accurate-pipetting-and-solution-preparation
category: natural-sciences
field: laboratory-field-methods
product: general-laboratory-technique
tags: [general-laboratory-technique, pipetting, micropipette, air-displacement-pipette, forward-pipetting, reverse-pipetting, viscous-liquids, pre-wetting, pipette-calibration, gravimetric-check, solution-preparation, molarity, c1v1-c2v2, dilutions, stock-solutions, volumetric-flask, buffer-preparation, ph-meter, ph-calibration, significant-figures, lab-notebook, labelling, glp, good-laboratory-practice]
level: intro
status: gated
description: "Pipette accurately (forward vs reverse, angle, pre-wet, right volume range), check a pipette gravimetrically, and make solutions and dilutions correctly with C1V1=C2V2 and proper labelling."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accurate pipetting and solution preparation

**Goal:** volumes and concentrations you can trust to a few percent, every time, so
that the errors in your experiment are biological rather than self-inflicted.

## 1. Pipetting technique (air-displacement micropipettes)
1. **Pick the right pipette:** use one whose range puts your volume in the upper part
   of its range. 10 µL on a P1000 is poor; use a P10/P20. Accuracy specs degrade
   sharply at the bottom ~10 % of the range (gated: unconfirmed, source is paywalled or blocked).
2. **Pre-wet** the tip: aspirate and dispense 2–3 times before the real draw. This
   saturates the air cushion with vapour and wets the tip wall — matters most for
   volatile or larger volumes.
3. **Hold vertical** (within ~20° (gated: unconfirmed, source is paywalled or blocked)) while aspirating; immerse the tip only a few mm
   (deeper picks up liquid on the outside; shallower sucks air).
4. **Release the plunger slowly**; wait ~1 s after it stops before withdrawing.
5. **Dispense** against the vessel wall at an angle, press to the first stop, pause, then
   to the second (blow-out) stop, and slide the tip up the wall.
6. New tip for every reagent and every sample unless deliberately serial.

**Reverse pipetting** (press to the second stop to aspirate, dispense only to the first
stop, discard the remainder) is better for viscous liquids (glycerol, enzyme stocks),
foaming liquids (detergents, protein solutions) and very small volumes. Forward pipetting
is standard for aqueous solutions.

Temperature matters: pipetting cold reagents with a room-temperature pipette (or holding
the pipette in a warm hand for long periods) shifts volumes. Volatile organics (ethanol,
chloroform) drip — use positive-displacement pipettes for them.

## 2. Quick gravimetric check
Water at 20 °C is 0.9982 g/mL and at 22 °C 0.9978 g/mL (computed from the Kell/Tanaka density formula); ISO 8655 instead converts mass to volume with a Z factor that also corrects for air buoyancy (about 1.0029 µL/mg at 20 °C, 101.3 kPa, per a manufacturer ISO table). Dispense the nominal volume 10 times onto a
tared analytical balance (in a small weighing vessel, with a lid for small volumes to cut
evaporation). Mean × Z (or ÷ 0.998 as a rough check) = delivered volume; compare with the spec (ISO 8655 lists
maximum permissible errors per nominal volume). The CV of the 10 weighings shows your
**precision**; the mean offset shows **accuracy**. Do this when a pipette is dropped or
results look off; send for service if out of spec.

## 3. Solution maths
- **Mass for a molar solution:** mass (g) = molarity (mol/L) × volume (L) × molar mass (g/mol).
  Use the formula weight on **your bottle**, including waters of hydration
  (CaCl₂·2H₂O ≠ anhydrous CaCl₂).
- **Dilution:** C₁V₁ = C₂V₂. To make 50 mL of 1× from 10× stock: V₁ = 1 × 50 ÷ 10 = 5 mL
  stock + 45 mL water.
- **Serial dilutions** for large factors (1:10,000) rather than one tiny volume.
- Percent solutions: say which — w/v (g per 100 mL), v/v, or w/w.

## 4. Making a buffer properly
1. Dissolve solids in ~80 % of the final volume.
2. Calibrate the pH meter that day with two or three standard buffers bracketing the
   target (e.g. 7 and 10 for pH 8); check the slope is within the meter's acceptable range.
3. Adjust pH **at the temperature of use** — Tris pH falls by roughly 0.028 units per °C rise (Fisher technical sheet; Sigma gives 0.03 for 5-25 °C and 0.025 for 25-37 °C).
4. Bring to final volume in a **volumetric flask** or measuring cylinder (not the beaker
   graduations — they are often ±5 % or worse).
5. Filter or autoclave as required; note that autoclaving can change pH of some buffers.

## 5. Labels and records
Every container: contents, concentration, solvent, date, your initials, hazard info, and
expiry where relevant. In the notebook: lot numbers, masses actually weighed, final pH,
and any deviation. A solution that is not traceable to a notebook entry should be discarded.

## Gotchas
- Adding acid/base past the target and back-titrating changes ionic strength — go slowly.
- Hygroscopic solids (NaOH, CaCl₂) weigh heavy after exposure to air; weigh quickly and
  keep lids closed.
- Always add acid to water, not water to concentrated acid.

The 10-weighing count and ISO 8655 tolerances are (gated: unconfirmed, source is paywalled or blocked); check the standard or the
pipette manufacturer's spec sheet for each model.

## Verify
- [ ] Each volume pipetted with a pipette in the upper part of its range, technique as above.
- [ ] Gravimetric check of critical pipettes within spec and logged.
- [ ] Calculations written out with the bottle's formula weight and hydration state.
- [ ] pH meter calibrated the same day; buffer pH set at the use temperature.
- [ ] All containers fully labelled and traceable to the notebook.
