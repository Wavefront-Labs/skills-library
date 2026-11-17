---
id: energy-mining-utilities.water-treatment-supply.desalination-plant-operation.ro-train-normalised-performance-and-membrane-cip
name: ro-train-normalised-performance-and-membrane-cip
category: energy-mining-utilities
field: water-treatment-supply
product: desalination-plant-operation
tags: [water-treatment-supply, desalination-plant-operation, reverse-osmosis, ro, swro, bwro, desalination, normalised-permeate-flow, normalized-flow, salt-passage, differential-pressure, delta-p, membrane-fouling, scaling, biofouling, cip, clean-in-place, antiscalant, sdi, silt-density-index, cartridge-filter, recovery, brine, concentrate, energy-recovery-device, membrane-autopsy]
level: advanced
status: draft
description: "Operate a seawater or brackish RO train by its normalised data: when permeate flow, salt passage or differential pressure say clean, and how to run a membrane CIP."
sources:
  - "ASTM D4516 (Standardizing RO performance data), concepts paraphrased"
  - "Membrane manufacturers' technical manuals (cleaning guidelines), general practice paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RO train normalised performance and membrane CIP

**Goal:** know which problem your reverse-osmosis train has (fouling, scaling, damage, or
just colder water) and clean it at the right time with the right chemistry.

## 1. Normalise or you'll chase the weather
Raw permeate flow and conductivity move with feed temperature, salinity and pressure.
Normalise daily (ASTM D4516 method, or your vendor's software) to a reference condition:
- **Normalised permeate flow (NPF)** — corrected for temperature and net driving pressure.
- **Normalised salt passage (NSP)** — corrected salt passage.
- **Differential pressure (ΔP)** across each stage (feed minus concentrate pressure).
Establish a baseline in the first days after commissioning or after a good clean.

## 2. Reading the trend
| Symptom | Usual cause |
|---|---|
| NPF down, ΔP up in **first** stage | particulate/colloidal or biofouling |
| NPF down, NSP up in **last** stage | mineral scaling (CaCO3, CaSO4, silica) — check antiscalant and recovery |
| NSP up suddenly, NPF up | O-ring/interconnector leak or membrane damage (oxidation from chlorine breakthrough) |
| ΔP up, NPF steady | debris on lead element face, feed spacer blockage |

Common cleaning triggers (manufacturer guidance typically): NPF down **10–15%**, NSP up
**5–10%**, or ΔP up **10–15%** from baseline. Cleaning later than that recovers less.

## 3. Pre-treatment is where most fouling starts
- SDI (silt density index) at RO feed — many manufacturers want SDI15 < 3–5.
- Cartridge filter ΔP; change at the vendor's limit and look at what's on them.
- Free chlorine/ORP after dechlorination — must be zero for polyamide membranes.
- Antiscalant dosing proven by drawdown; scaling calculations redone if recovery or feed
  water changes.

## 4. Running a CIP (clean-in-place)
1. Flush the train with permeate (or RO-quality water) to displace feed/brine.
2. **High-pH clean first** for organic/bio-fouling (typically NaOH-based to pH ~11–12
   within the membrane's temperature limit, often 30–35 °C) unless scaling is clearly the
   only problem. Then **low-pH clean** (citric/HCl, pH ~2) for scale and metals. Acid first
   on organics can set foulants harder.
3. Circulate at low pressure and the vendor's flow per vessel, stage by stage; soak
   (1–several hours), re-circulate. Watch colour and pH — re-adjust pH as it drifts.
4. Flush to drain until pH and conductivity are back to normal; send first permeate to
   waste.
5. Record post-clean NPF/NSP/ΔP; compare recovery to the last cleans.

## 5. Brine and energy
Brine must meet discharge permit (salinity, temperature, residual chemicals — CIP waste is
usually neutralised and sent separately). Check energy recovery device (pressure exchanger
or turbine) efficiency and mixing/leakage — a rising specific energy (kWh/m³) is often the
ERD, not the membranes.

## Gotchas
- Exceeding pH/temperature limits together (high pH + hot) damages polyamide permanently.
- Cleaning stages in series sends first-stage foulant into the second stage; clean
  separately where the skid allows.
- Repeated cleans with poor recovery → do a membrane autopsy on a lead element rather than
  keep cleaning.

## Verify
- [ ] Daily normalised data plotted against post-clean baseline.
- [ ] Trigger and stage location identified before choosing chemistry.
- [ ] CIP within the membrane's pH/temperature limits; flushed before return to service.
- [ ] Post-clean NPF recovered; pre-treatment cause investigated.
- [ ] Brine and CIP waste within permit.

*Uncertain:* cleaning triggers, chemistry and limits are manufacturer-specific; always use
the element maker's current cleaning guide.
