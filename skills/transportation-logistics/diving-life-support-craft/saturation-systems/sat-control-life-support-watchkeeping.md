---
id: transportation-logistics.diving-life-support-craft.saturation-systems.sat-control-life-support-watchkeeping
name: sat-control-life-support-watchkeeping
category: transportation-logistics
field: diving-life-support-craft
product: saturation-systems
tags: [diving-life-support-craft, saturation-systems, saturation-diving-system, sat-system, sat-control, life-support-technician, lst, life-support-supervisor, lss, heliox, ppo2, oxygen-make-up, co2-scrubbing, scrubber, environmental-control, temperature, humidity, habitat, living-chamber, transfer-under-pressure, tup, hyperbaric-evacuation, hrc, shl, hyperbaric-lifeboat, gas-reclaim, sat-decompression, storage-depth, imca, watchkeeping, log]
level: advanced
status: draft
description: "Keep a saturation habitat alive on watch: ppO2 make-up, CO2 scrubbing, heliox temperature and humidity, gas and contamination checks, logs, and evacuation readiness."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sat control life-support watchkeeping

**Goal:** the divers in the habitat breathe the right ppO₂, low CO₂, at a comfortable
temperature, 24 hours a day, for weeks — and the system can be evacuated at any moment.

> Draft: general saturation practice (IMCA-style roles: Life Support Technician (LST) /
> Life Support Supervisor (LSS)). **Parameters below are typical ranges to orient a
> reader, not limits** — use your company's saturation procedures and the system's
> operating manual.

## 1. What you control, and typical targets
| Parameter | Typical working target (verify locally) | Why |
|---|---|---|
| **ppO₂** in living chambers | ~0.4–0.5 bar (some companies up to ~0.6) | Enough to avoid hypoxia, low enough to avoid pulmonary O₂ toxicity over weeks |
| **ppCO₂** | below ~5 mbar (0.5 kPa), lower is better | CO₂ effects are amplified at depth |
| **Temperature** | ~27–32 °C, rising with depth | Helium conducts heat away fast; divers chill at "normal" temperatures |
| **Relative humidity** | ~50–70% | Too high → ear and skin infections; too low → discomfort |
| **Contaminants** | below limits for CO, hydrocarbons, etc. | Closed loop concentrates them |
Remember: at depth, small % changes are large partial-pressure changes. Always think
in **partial pressure**, not percent.

## 2. Oxygen make-up
- Divers consume O₂ continuously (~0.5 L/min per person at rest, surface-equivalent,
  roughly — consumption rises with activity).
- Add O₂ in **small, logged increments** via the make-up system; never large bolus adds.
- Two independent analysers; **cross-check** them each watch and calibrate per
  schedule. If they disagree, stop and investigate before adding gas.
- Fire risk grows with O₂ **percentage**; at storage depth the % is low, but near the
  end of decompression it rises — watch it.

## 3. CO₂ scrubbing
- Scrubbers (e.g. soda-lime canisters in the environmental control loop): track CO₂
  trend, **change canisters** before the absorbent is exhausted (by trend and schedule,
  not only at alarm).
- Log canister changes, absorbent batch and hours.

## 4. Temperature and humidity
- Respond to diver requests quickly — a cold sat diver is a sick sat diver.
- Heating/cooling via the environmental control unit; dehumidify via the ECU's cooling
  coil.
- Bell runs: heating via hot water suit and bell heaters; check before each run.

## 5. Watch routine (each hour or per procedure)
1. Read and log: depth (two gauges), ppO₂ (two analysers), ppCO₂, temperature,
   humidity, gas bank pressures, scrubber status.
2. Gas reserves: confirm **mix and O₂ reserves** cover the planned operation plus
   emergency (treatment, bail-out of the bell, evacuation).
3. Talk to the divers — symptoms (headache, rash, ear pain, breathing) are early
   warnings.
4. Sanitation: toilets, showers (flushing under pressure follows strict valve sequence —
   never flush without the procedure; there have been fatal accidents), food/medical
   lock transfers per procedure.
5. Handover: trends, anything outstanding, upcoming bell runs or decompression.

## 6. Evacuation readiness
- **Hyperbaric rescue craft / SPHL** (self-propelled hyperbaric lifeboat): life support
  checked, mate-up path clear, crew assigned.
- Know the **transfer under pressure (TUP)** sequence to move divers into it.
- Drill regularly; a sat system that can't be evacuated in a fire or sinking is not safe.

## 7. Decompression from saturation
- Follows the company's sat decompression schedule — slow (on the order of tens of
  metres per day), with ppO₂ raised during deco per the table and rest stops.
- No bell runs once decompression starts (excursion limits apply before).

## Gotchas
- Analyser drift is the classic silent failure: two analysers, cross-checked.
- Gas reserves count only gas you can actually deliver at depth.
- Temperature comfort at 150 m is not comfort at 50 m — set by depth and diver feedback.

## Verify
- [ ] Hourly log covers depth, ppO₂, ppCO₂, temperature, humidity and reserves.
- [ ] Two analysers agree; any disagreement was resolved before adding gas.
- [ ] Scrubbers changed on trend/schedule, not just on alarm.
- [ ] Gas reserves cover operations plus emergencies.
- [ ] Hyperbaric evacuation system checked and TUP sequence known.
