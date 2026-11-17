---
id: manufacturing-production.metal-plastics-fabrication-production.powder-coating-finishing.pretreatment-cure-and-film-thickness-control
name: pretreatment-cure-and-film-thickness-control
category: manufacturing-production
field: metal-plastics-fabrication-production
product: powder-coating-finishing
tags: [powder-coating-finishing, powder-coating, e-coat, electrocoat, finishing-line, pretreatment, iron-phosphate, zinc-phosphate, zirconium, conversion-coating, titration, conductivity, water-break-test, rinse, dry-off-oven, cure-oven, oven-profile, datapaq, cure-schedule, mek-rub-test, dft, dry-film-thickness, elcometer, adhesion, cross-hatch, iso-2409, astm-d3359, faraday-cage, gun-settings, grounding, hangers, outgassing, orange-peel, salt-spray]
level: practitioner
status: draft
description: "Run a powder or e-coat line to spec: pretreatment titrations and water-break test, grounding, oven cure profiling, DFT measurement, adhesion and cure tests, and common defect causes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pretreatment, cure and film thickness control

**Goal:** coated parts that pass adhesion, cure and corrosion requirements — not just
look right off the line. Most coating failures in the field trace back to
**pretreatment** or **under-cure**, both invisible at unload.

## 1. Pretreatment — the coating is only as good as this
A typical multi-stage washer: alkaline clean → rinse → conversion coat (iron phosphate,
zinc phosphate, or zirconium/thin-film) → rinses → (seal) → final DI rinse → dry-off oven.
Daily/shift control:
- **Titrations** for each chemical stage (free/total alkali, total acid, accelerator
  etc. per the chemical supplier's control sheet) and temperatures, pressures, pH.
- **Rinse conductivity**, especially the final DI rinse (supplier gives a limit) —
  dissolved salts left on the part cause blistering under the coating.
- **Water-break test** after cleaning: water should sheet off continuously; breaks
  mean oil remains. Simple and very telling.
- Nozzle condition: blocked or misaligned nozzles leave unclean zones on parts.
- Conversion coating weight check (coating weight test) on the supplier's schedule.
- Parts fully dry before powder: water in seams and lap joints bleeds out in the oven.

## 2. Grounding and application
- Powder relies on electrostatic charge; **grounding** through clean hooks is
  essential. Strip hangers regularly (burn-off oven, blasting, chemical strip) —
  measure resistance part-to-ground if your site specifies a limit.
- Gun settings (kV, µA, powder flow, air) per part recipe. Recesses and inside
  corners suffer **Faraday cage** effect: lower kV, use corner nozzles, manual touch-up.
- Powder supply: fluidisation, reclaim/virgin ratio, sieve, humidity in the booth.
- **E-coat**: bath solids, pH, conductivity, temperature, voltage and immersion time;
  ultrafiltrate rinse; anode condition. Throwpower test for recessed areas.

## 3. Cure: measure the part, not the oven
The powder datasheet gives a **cure schedule** as metal temperature vs time (e.g. a
given time at a given **part** temperature). Heavy parts lag the oven air badly.
- Run an **oven profile** (Datapaq-type datalogger with thermocouples clamped to the
  heaviest and lightest parts on the line) at production line speed.
- Compare each TC's time-at-temperature to the cure window.
- Re-profile after oven maintenance, line speed change or new heavy parts.
- **Cure test**: solvent rub (MEK or as specified by the powder supplier) on a cured
  part — softening/colour transfer beyond the spec → under-cure.

## 4. Film thickness
- Measure **DFT** with a calibrated magnetic/eddy-current gauge (Elcometer, PosiTector
  etc.) — verify zero and calibration foils on the same substrate at shift start.
- Measure per plan at specified points, including edges and recesses. Report min/max.
- Too thin → poor corrosion protection and hide; too thick → orange peel, cracking,
  poor fit of assemblies (threads, holes), wasted powder.

## 5. Adhesion and performance tests
- **Cross-hatch adhesion** (ISO 2409 / ASTM D3359) on test panels or parts.
- Impact, flexibility, gloss and colour per spec.
- **Salt spray** or cyclic corrosion test on the schedule the customer requires (lab).

## Defect → first suspects
| Defect | Check |
|---|---|
| Poor adhesion / peeling | Pretreatment (cleaning, conversion), under-cure |
| Blisters | Rinse conductivity, trapped moisture, outgassing |
| **Outgassing pinholes** (castings, galvanised) | Pre-bake parts; degassing powder |
| Orange peel | Too thick, oven ramp, powder particle size |
| Craters/fisheyes | Silicone/oil contamination (air supply, lubricants nearby) |
| Thin in recesses | Faraday cage — gun/kV technique |

## Verify
- [ ] Pretreatment titrations, temperatures and final rinse conductivity in range today.
- [ ] Water-break test passes.
- [ ] Oven profile shows every part TC within the cure schedule.
- [ ] DFT within spec at all checkpoints; gauge verified.
- [ ] Cross-hatch and solvent-rub pass on the sampling plan.

*Draft: chemical control ranges come from each chemical/powder supplier; the generic
process is described, not specific numbers.*
