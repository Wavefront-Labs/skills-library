---
id: health-medicine.nursing.infusion-pumps-and-bedside-devices.programming-smart-pumps-and-managing-alarms
name: programming-smart-pumps-and-managing-alarms
category: health-medicine
field: nursing
product: infusion-pumps-and-bedside-devices
tags: [nursing, infusion-pumps-and-bedside-devices, infusion-pump, smart-pump, syringe-driver, syringe-pump, volumetric-pump, drug-library, dose-error-reduction-software, ders, guardrails, occlusion-alarm, free-flow, anti-siphon, alarm-fatigue, bedside-monitor, secondary-infusion, piggyback]
level: practitioner
status: draft
description: "Program volumetric and syringe smart pumps via the drug library, trace lines, avoid free-flow and secondary-infusion errors, handle occlusion alarms, and cut monitor alarm fatigue."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Programming smart pumps and managing alarms

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** program infusions so the pump's safety software actually protects the
patient, and keep alarms meaningful so real ones get answered.

## 1. Choose the device
- **Volumetric pump:** larger volumes (fluids, antibiotics, blood per policy), mL/h.
- **Syringe pump/driver:** small volumes at precise or low rates (inotropes,
  sedation, insulin, opioid infusions, neonatal).
- Ambulatory/PCA pumps for specific uses with their own protocols.
Use only devices you've been trained on, with an in-date service label.

## 2. Programming with the drug library (DERS)
1. Select the correct **care area/profile** (adult ICU vs paediatrics vs maternity — limits differ).
2. Select the **drug from the library**, not "basic infusion"/"no drug selected" —
   bypassing the library removes dose limits; audit data show bypass is a major
   source of unprotected infusions.
3. Confirm concentration matches the bag/syringe label.
4. Enter **weight** (kg, measured) for weight-based drugs, dose or rate, and **VTBI**
   (volume to be infused).
5. Respond to limit alerts: **soft limit** = stop and re-check the prescription and
   your entry before overriding with a reason; **hard limit** = cannot proceed — the
   entry or prescription is wrong.
6. Independent double check for high-alert infusions before pressing start.
7. Many errors are decimal or unit slips (mL/h vs mg/h, 1.0 vs 10) — read the
   summary screen aloud.

## 3. Line safety
- **Trace every line** from bag to pump channel to patient port at start, after
  changes and at handover. Label lines near the connection.
- Load the administration set correctly; close the roller clamp before removing a
  set — **free-flow** of a drug like insulin or potassium can be fatal. Use sets with
  anti-free-flow protection.
- Syringe pumps: ensure the plunger and barrel are seated in the clamps; prime and
  remove slack (otherwise a delay before delivery, then a bolus); keep the pump at
  patient height — raising/lowering can cause siphoning or bolus.
- **Secondary (piggyback) infusions:** the secondary bag must hang higher than the
  primary and the correct clamp must be open, otherwise the primary runs at the
  secondary rate or the secondary doesn't run.
- Critical infusions (vasopressors): dedicated lumen, no bolus flushing through it;
  prepare the next syringe before the current one runs out (double-pumping per policy).

## 4. Alarms
- **Occlusion downstream:** check clamps, kinks, the cannula site (infiltration?),
  limb position. Don't simply raise the pressure limit.
- **Air in line:** remove air properly per device instructions.
- **Near-end/VTBI complete:** plan replacement in advance.
- Monitor alarms (ECG, SpO₂): customise limits to the patient within policy, change
  ECG electrodes daily, fix poor SpO₂ probe placement — most alarms are non-actionable,
  and **alarm fatigue** leads to missed real events. Never disable alarms, and don't
  leave a monitor in "silence" indefinitely.

## Gotchas
- Pump channels and drug names on screen can differ from the bag — the bag, the
  prescription and the screen must all agree.
- Changing a concentration without changing the library entry gives the wrong dose.
- Report device faults and remove the pump from use with a label; don't reuse.

Uncertainty note: alert behaviour and terms (Guardrails, DERS, soft/hard limits) vary
by manufacturer; follow device-specific training.

## Verify
- [ ] Correct profile and library drug used; concentration matches.
- [ ] Weight, rate and VTBI read back; high-alert drug double-checked.
- [ ] Every line traced and labelled.
- [ ] Secondary bag height and clamps correct.
- [ ] Alarm limits appropriate and audible.
