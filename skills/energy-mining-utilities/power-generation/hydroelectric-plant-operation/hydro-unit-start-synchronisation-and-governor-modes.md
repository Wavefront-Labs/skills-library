---
id: energy-mining-utilities.power-generation.hydroelectric-plant-operation.hydro-unit-start-synchronisation-and-governor-modes
name: hydro-unit-start-synchronisation-and-governor-modes
category: energy-mining-utilities
field: power-generation
product: hydroelectric-plant-operation
tags: [hydroelectric-plant-operation, power-generation, hydro, hydropower, francis-turbine, kaplan, pelton, wicket-gates, guide-vanes, penstock, intake-gate, governor, droop, isochronous, speed-no-load, excitation, synchronisation, synchroscope, sync-check, water-hammer, cavitation, rough-zone, rough-load-zone, tailwater, head]
level: practitioner
status: draft
description: "Start a hydro unit from standstill, synchronise it to the grid and pick the right governor mode: pre-start checks, wicket-gate opening, sync conditions, droop vs isochronous, rough zones."
sources: ["IEEE Std 1207 (hydro governor guidance, general principles)", "USBR Facilities Instructions FIST series (public, paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hydro unit start, synchronisation and governor modes

**Goal:** bring a hydro generating unit (Francis, Kaplan or Pelton) from standstill to
loaded on the grid smoothly and safely, and know which governor mode it should be in.
Most stations automate the start sequence; you still need to recognise each stage and
step in when it hangs. Numbers below are typical; your station's operating orders and
unit data rule.

## 1. Pre-start checks
- **Water path:** intake gate/penstock valve open and penstock filled (a filling or
  by-pass valve equalises pressure first — never open a main valve against a large
  differential). Trash rack differential acceptable.
- **Unit:** brakes released (and confirmed off — a dragging brake burns pads and
  can start a fire), jacking/lift oil pump running if fitted, guide and thrust bearing
  oil levels and cooling water flowing, governor oil pressure up (accumulator charged).
- **Electrical:** generator breaker open, excitation ready, protection healthy, no
  earth on stator.
- Permission from dispatch/control centre; reservoir and downstream flow constraints
  understood (minimum flow orders, ramping limits for fish or recreation).

## 2. Start to speed-no-load
1. Governor opens the **wicket gates** (guide vanes) to a start opening; the unit
   accelerates. Pelton units open needles/deflectors instead.
2. At around 90–95 % speed the governor switches to speed control and settles at
   rated speed, **speed-no-load (SNL)**.
3. Lift-oil pump stops above its cut-out speed; check bearing temperatures start to
   stabilise.
4. **Field flash / excitation on:** voltage builds to rated.
Watch for vibration through the speed range — a sudden rise near rated may be
imbalance or a rub; trip if it exceeds the alarm/trip limit.

## 3. Synchronising
Close the generator breaker only when the generator and grid match on:
- **Voltage:** within a few percent (generator slightly above grid is usual so the unit
  picks up a little reactive power, not absorbs it).
- **Frequency:** generator slightly fast (synchroscope rotating slowly "fast"), so it
  picks up real power rather than motoring.
- **Phase angle:** close as the synchroscope approaches 12 o'clock — breaker closing
  time means the command goes just before.
Auto-synchronisers do this; a **sync-check relay** blocks out-of-phase closure in
either mode. Manual sync is a trained skill — closing far out of phase can damage
the shaft and windings.

## 4. Governor modes
- **Droop** (typically 4–5 %): the normal grid-connected mode. Output changes in
  proportion to frequency deviation, so units share frequency response. Load is set
  by changing the speed reference / load set point.
- **Isochronous:** holds frequency exactly; for an islanded system or a unit black-
  starting a dead network. Two isochronous units on one system will fight — only one
  should be isochronous.
- **Power/gate-limit control:** many governors control MW directly or cap gate
  opening; know which loop is active before blaming the governor.

## 5. Loading
- Ramp at the allowed rate; rapid gate movement causes **water hammer** (pressure
  surges in the penstock) — gate timing is set to keep surge within design.
- Avoid the **rough zone** (often roughly 20–50 % output on Francis units) where
  draft-tube vortex rope causes vibration and pressure pulsation; pass through it
  quickly or run above it. Kaplan units adjust runner blades to stay efficient.
- Watch tailwater level: low tailwater raises cavitation risk.

## Gotchas
- Unit creeping at standstill with gates "closed": worn wicket-gate seals; brakes
  and/or a closed intake are what actually hold it.
- Load rejection drives the unit to overspeed; the governor and gate-closing time
  limit it, not the operator.
- Uncertain: speed thresholds, droop values and rough-zone bands are unit-specific —
  check the unit's commissioning data.

## Verify
- [ ] Penstock equalised before main valve opened; brakes confirmed released.
- [ ] Bearing oil, cooling water and governor pressure normal before rolling.
- [ ] Breaker closed with voltage, frequency and phase matched; sync-check in service.
- [ ] Governor in the mode the system needs (droop for grid, one isochronous unit if islanded).
- [ ] Unit not parked in its rough zone; vibration and bearing temps steady.
