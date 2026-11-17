---
id: energy-mining-utilities.power-generation.fossil-steam-plant-operation.cold-startup-of-a-drum-boiler-unit
name: cold-startup-of-a-drum-boiler-unit
category: energy-mining-utilities
field: power-generation
product: fossil-steam-plant-operation
tags: [fossil-steam-plant-operation, power-generation, boiler, drum-boiler, cold-start, startup, purge, furnace-purge, light-off, drum-level, shrink-and-swell, three-element-control, firing-rate, saturation-temperature, drum-metal-differential, turbine-roll, synchronisation, coal-fired, gas-fired, oil-fired, steam-cycle, nfpa-85, bms, burner-management-system]
level: practitioner
status: draft
description: "Bring a drum-type fossil boiler from cold to turbine roll: pre-start checks, furnace purge, light-off, controlled pressure raising, drum-level shrink/swell, and the hold points that matter."
sources: ["NFPA 85 Boiler and Combustion Systems Hazards Code (purge and light-off principles)", "Steam: Its Generation and Use (Babcock & Wilcox), startup chapters"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cold startup of a drum boiler unit

**Goal:** take a drum-type coal-, oil- or gas-fired unit from cold, depressurised and
drained to steam conditions fit for turbine roll — without a furnace explosion, a
drum-level trip or cracked thick-walled parts. Your plant's own operating procedure
and its limits (ramp rates, metal-temperature differentials) always override the
typical numbers below; treat them as orders of magnitude.

## 1. Before anything lights
- **Permits cleared and isolations removed:** every lock-out from the outage is signed
  off, manholes and access doors closed, scaffolding out of the furnace.
- **Valve line-up per checklist:** drum vents and superheater drains/vents **open**,
  start-up (bypass) drains open, main steam stop closed, blowdown closed, chemical
  feed and sampling lined up.
- **Fill** the boiler with deaerated, chemistry-conditioned water to the start-up
  level — usually *below* normal working level (often around −100 to −200 mm on the
  gauge, plant-specific) because the water swells as it heats. Fill slowly when the
  drum is cold to limit thermal stress; confirm fill-water temperature limits.
- **Prove level indication:** compare the direct gauge glass against the DP transmitters.
  Remote level reads differently at low pressure (density compensation), so the gauge
  glass is the reference during start-up.
- Start air heaters, ID and FD fans (ID first, to keep the furnace under draught),
  establish furnace pressure slightly negative.

## 2. Purge and light-off
- The **burner management system (BMS)** enforces the purge: typically at least
  25–30 % of full-load airflow for at least five volume changes or five minutes, whichever
  is longer (NFPA 85 principle). Never bypass or shorten it. A failed light-off
  means re-purge before the next attempt.
- Light igniters, then the first burner or oil gun at minimum fire. Watch the flame
  scanners; on loss of flame the BMS trips fuel — find the cause, don't just retry.
- Coal units usually start on oil or gas and only bring in mills once furnace and
  air-heater temperatures allow stable pulverised-coal ignition.

## 3. Raising pressure — slowly
- The limit is usually **drum metal temperature**, not pressure. Watch top-to-bottom
  drum differential (a common limit is around 50–60 °C / 90–110 °F; check yours) and the
  rate of saturation-temperature rise (often ~55–110 °C per hour for thick drums).
- Steam the superheater through its drains/vents so tubes are cooled by flow; keep
  furnace exit gas temperature below the limit for unprotected superheater/reheater
  tubes (a probe or thermocouple reading) until there is steam flow.
- Close the drum vents once steady steam issues (commonly around 1–2 bar / 15–30 psig);
  close superheater drains progressively as superheat develops.
- Hold points: pressure where you check chemistry (silica, conductivity), blowdown to
  clean up, and warm the main steam lines through their drains.

## 4. Drum level — the trap
- **Swell:** raising firing or dropping pressure makes the water level rise on the glass
  even though mass is leaving. **Shrink:** the opposite. The instinctive correction
  (less feed on swell) is wrong and leads to a low-level trip seconds later.
- At low load, run feed on **single-element** (level only) control; switch to
  **three-element** (level + steam flow + feed flow) only above the minimum flow where the
  flow transmitters are trustworthy — commonly 20–30 % load. Make that switch with
  level steady.
- Make firing changes in small steps and wait for level to settle.

## 5. Ready for turbine roll
Steam temperature should be well above saturation (a common rule is 50 °C+ of superheat)
and matched to turbine metal temperature per the turbine manufacturer's start curve.
Roll, synchronise, pick up block load, then load at the boiler's permitted ramp.

## Gotchas
- A boiler "lit" with a missed purge is the classic furnace explosion. If the trip
  record is unclear, purge again.
- Chemistry cleanup can take longer than the pressure raise; turbines reject steam
  with high silica or sodium (see the power-plant-water-chemistry skills).
- Gauge-glass faults: a blocked steam leg reads high. Blow down the glass if in doubt.
- Uncertain here: exact ramp rates, purge flow and level set points vary by OEM and
  jurisdiction — not confirmed against a single plant.

## Verify
- [ ] All permits cleared and the valve line-up signed before fans start.
- [ ] BMS purge completed and logged before first light-off.
- [ ] Drum metal differential and pressure-rise rate stayed inside the plant limit.
- [ ] Gauge glass and remote level agreed (within the expected low-pressure offset).
- [ ] Single-to-three-element changeover made above the flow threshold, level steady.
- [ ] Steam chemistry within turbine limits before roll.
