---
id: energy-mining-utilities.power-generation.power-plant-water-chemistry.cycle-chemistry-monitoring-and-action-levels
name: cycle-chemistry-monitoring-and-action-levels
category: energy-mining-utilities
field: power-generation
product: power-plant-water-chemistry
tags: [power-plant-water-chemistry, power-generation, cycle-chemistry, steam-chemistry, boiler-water, feedwater, condensate, cation-conductivity, acid-conductivity, specific-conductivity, degassed-conductivity, sodium, silica, dissolved-oxygen, ph, ammonia, avt, avt-r, avt-o, oxygenated-treatment, phosphate-treatment, condenser-leak, action-levels, iapws, epri, online-analysers, sample-panel, hrsg]
level: practitioner
status: draft
description: "Watch steam-cycle chemistry like a plant chemist: the core online parameters, what each one tells you, condenser leak signs, and how action levels turn an excursion into a timed response."
sources: ["IAPWS Technical Guidance Documents on cycle chemistry instrumentation and HRSG chemistry (public, paraphrased)", "EPRI cycle chemistry guidelines (concepts only)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cycle chemistry monitoring and action levels

**Goal:** keep feedwater, boiler water and steam within limits so that tubes don't
corrode or fail, and turbines don't collect deposits — and respond to an excursion
in proportion and on time. Your plant's chemistry manual sets the actual limits for
its treatment regime (AVT(R), AVT(O), oxygenated treatment, phosphate or caustic);
the figures here are typical guidance values only.

## 1. The core online parameters
A minimum sensible set (IAPWS calls these "key" instruments):
- **Cation (acid) conductivity** of condensate, feedwater and steam — the single most
  useful number. The sample passes through a cation-exchange resin that removes
  ammonia, so what's left reflects anions: chloride, sulphate, organic acids, CO2.
  Typical steam target is below about 0.2 µS/cm. It rises before anything else when
  a condenser leaks or contaminants enter.
- **Specific conductivity** — mostly reflects the treatment chemical (ammonia), so it
  tells you dosing level, not contamination.
- **pH** (often calculated from specific and cation conductivity, as direct pH
  measurement in pure water is unreliable).
- **Dissolved oxygen** at condensate pump discharge and economiser inlet — air
  in-leakage, deaerator performance, or the target for oxygenated treatment.
- **Sodium** in steam and condensate — the quick indicator of a seawater/cooling water
  condenser leak. Steam targets are a few µg/kg (ppb).
- **Silica** in steam — deposits on turbine blades; target commonly below ~10 µg/kg.
Degassed cation conductivity separates carbon dioxide (air in-leakage, common during
start-up) from true salt contamination.

## 2. Keep the samples honest
- Constant sample flow (often ~ 0.1–0.2 m/s velocity in the line or the panel's design
  flow) and cooled to ~25 °C; varying flow changes iron and silica readings.
- Cation resin columns exhaust: change when the colour front reaches the mark.
- Calibrate or verify analysers on schedule; compare with grab samples weekly.

## 3. Reading an excursion
- **Cation conductivity up + sodium up in condensate** → condenser tube leak. Confirm
  by hotwell sampling by section where possible; isolate the leaking half if the
  condenser is split.
- **Cation conductivity up, degassed normal** → CO2 from air in-leakage; check
  condenser vacuum and air removal.
- **Dissolved oxygen up** → air leak on the vacuum side, deaerator venting, or a
  condensate pump gland.
- **Silica up in steam** after start-up → carryover or makeup water problem;
  increase blowdown, check demineraliser output.

## 4. Action levels — making it time-bound
Many plants use a tiered scheme (EPRI/IAPWS style). The idea, with commonly cited
timings that you must confirm against your own manual:
- **Normal:** within limits.
- **Action level 1:** potential for contaminant build-up — return to normal within
  about a week.
- **Action level 2:** accumulation likely to cause damage — return within about a day.
- **Action level 3:** rapid corrosion likely — return within hours (often ~4), or
  shut the unit down.
Each excursion gets a time stamp; the clock decides escalation, not optimism.
Also note *how long* you spent outside limits — cumulative exposure is what damages
tubes.

## Gotchas
- A slow seawater leak at a once-through unit with no condensate polisher can do
  more damage in hours than a drum unit in days; know your plant's tolerance.
- Start-ups are when most chemistry damage happens; don't relax because "it's just
  start-up".
- Phosphate hideout: phosphate disappears from boiler water at high load and returns
  at low load — not a dosing error.
- Uncertain: exact limits and action-level timings vary by guideline edition and plant
  design; numbers here are indicative only.

## Verify
- [ ] Cation conductivity, sodium, DO and silica online and in calibration.
- [ ] Sample flows and temperatures within panel limits; resin not exhausted.
- [ ] Any excursion logged with start time, action level and cause.
- [ ] Condenser leak response (isolate, confirm, inform) drilled.
- [ ] Time spent outside limits reviewed monthly.
