---
id: energy-mining-utilities.power-generation.gas-turbine-plant-operation.gas-turbine-start-sequence-and-trip-diagnosis
name: gas-turbine-start-sequence-and-trip-diagnosis
category: energy-mining-utilities
field: power-generation
product: gas-turbine-plant-operation
tags: [gas-turbine-plant-operation, power-generation, gas-turbine, combustion-turbine, ccgt, combined-cycle, hrsg, start-sequence, purge, crank, ignition, flame-detection, lci, static-starter, self-sustaining-speed, fsnl, synchronisation, exhaust-temperature-spread, trip, failed-start, first-out, sequence-of-events, dln, combustion-dynamics, ge-mark-vie, siemens-t3000]
level: practitioner
status: draft
description: "Run a gas turbine start from ready-to-start to sync and diagnose a trip or failed start: purge, ignition, acceleration, exhaust spread, first-out alarms and when it is safe to restart."
sources: ["OEM operating manuals (general structure, paraphrased)", "NFPA 85 (HRSG purge principles)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gas turbine start sequence and trip diagnosis

**Goal:** know what the automatic start sequence is doing at each step, so you can
spot a start that is going wrong before it trips, and diagnose a trip from the
evidence rather than by pressing *Reset* and *Start* again. Modern units (GE Mark VIe,
Siemens T3000, Mitsubishi Diasys and others) automate the sequence; the operator's job is
permissives, watching and judgement. Step names and speeds below are typical of
heavy-duty frame units; your OEM's numbers rule.

## 1. Ready to start — permissives
- Lube oil and hydraulic/trip oil pressure up, oil temperature in range, turning gear
  engaged (a hot rotor that sat still will bow; most OEMs require hours on turning gear
  after a trip before restart).
- Fuel gas pressure and temperature at the skid within limits (dew-point superheat
  for gas, so liquids don't reach the nozzles).
- No active trips; protection tested where the procedure requires it; inlet guide
  vanes at start position; HRSG drums at start-up level, stack damper open.
- Grid/permission to start from dispatch.

## 2. The sequence and what to watch
1. **Crank / purge:** the static starter (LCI) or starting motor spins the rotor to purge
   speed (often ~20–25 % speed) and holds it to purge the turbine, HRSG and ductwork —
   typically several minutes, much longer with a big HRSG. Watch purge timer and airflow.
2. **Ignition / light-off:** speed drops to firing speed, igniters fire, fuel admitted.
   Flame detectors must confirm flame in the expected cans within a few seconds or the
   unit trips on *failure to ignite*.
3. **Warm-up:** a short hold at low fuel to soak the hot-gas path.
4. **Acceleration:** starter and fuel together accelerate the rotor; the starter drops
   out at self-sustaining speed (roughly 60–90 %, OEM-specific). Watch exhaust
   temperature and the **exhaust spread** (difference between highest and lowest
   exhaust thermocouples). A growing spread during acceleration means a can is not
   burning properly.
5. **Full speed no load (FSNL):** check vibration, bearing temperatures, exhaust spread.
6. **Synchronise and load:** auto-synchroniser matches voltage, frequency and phase;
   the unit picks up spinning reserve load, then ramps. On dry low NOx (DLN) units
   watch for combustion-mode transfers and combustion dynamics alarms as load rises.

## 3. Trip diagnosis — work the evidence
1. **Don't reset yet.** Note the **first-out** alarm: the first trip signal latched.
   Everything after it is often consequence.
2. Pull the **sequence of events (SOE)** and high-speed trends for the last few
   minutes: speed, fuel valve demand vs position, flame signals, exhaust temps,
   vibration, compressor discharge pressure.
3. Common first-outs and first checks:
   - *Loss of flame / failure to ignite:* igniter, flame detector (dirty lens, failed
     sensor), fuel valve not opening to stroke, low gas pressure, water in fuel.
   - *High exhaust spread:* one or more cans out, a failed thermocouple (compare
     neighbours — a single wild reading is usually the sensor), blocked nozzle.
   - *High vibration:* check whether it is real on more than one probe; rotor bow
     after a short turning-gear period is a common cause on restart.
   - *Compressor surge/stall:* inlet filter DP, IGV position, bleed valves.
   - *Overspeed / generator trip:* load rejection from the grid side; check the
     electrical protection relay targets.
4. Before restart: cause understood and fixed, turning-gear time satisfied, and the
   restart authorised per your plant's rules. Repeated failed starts heat the starter
   and fill the HRSG with unburnt fuel — a re-purge is mandatory.

## Gotchas
- A trip on a sensor fault still trips; fix or replace the sensor, don't defeat it.
- After a failed light-off, unburnt gas can sit in the HRSG; the purge is not optional
  even when "it was only a few seconds".
- Combined-cycle starts are often limited by the HRSG and steam turbine, not the GT —
  hold points for drum level and steam temperature matter (see
  energy-mining-utilities.power-generation.fossil-steam-plant-operation.cold-startup-of-a-drum-boiler-unit
  for the drum side).
- Uncertain: speeds, timings and DLN mode names vary by OEM and model; confirm locally.

## Verify
- [ ] All start permissives confirmed and logged, including turning-gear time.
- [ ] Purge completed for the full time (GT + HRSG).
- [ ] Flame confirmed in all expected cans; exhaust spread stayed in limits.
- [ ] For any trip: first-out recorded, SOE reviewed, root cause written before reset.
- [ ] Restart authorised per plant rules, not just "permissives green".
