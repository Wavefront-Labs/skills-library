---
id: manufacturing-production.chemical-process-manufacturing.continuous-process-operation.startup-rate-changes-and-upset-recovery
name: startup-rate-changes-and-upset-recovery
category: manufacturing-production
field: chemical-process-manufacturing
product: continuous-process-operation
tags: [continuous-process-operation, continuous-plant, plant-startup, startup-procedure, shutdown, rate-change, throughput, ramp-rate, steady-state, upset-recovery, trip, interlock, process-operator, operating-envelope, integrity-operating-window, iow, hold-point, time-constant, dead-time, cascade, feed-forward, recycle, snowball-effect, refinery, petrochemical, chemical-plant]
level: practitioner
status: draft
description: "Start up, change rate on and recover a continuous process unit: staged startup with hold points, ramping in step with the slowest loop, and bringing a tripped or upset unit back to steady state."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous plant: startup, rate changes and upset recovery

**Goal:** move a continuous unit between states — cold to running, one rate to
another, upset back to steady — without tripping it, damaging equipment or making a
lot of off-spec product.

## 1. Principles that apply to every transition
- **Mass balance first, energy second, quality third.** Get levels and pressures
  stable (inventory under control), then temperatures, then compositions.
- **Respect time constants.** A level responds in minutes; a distillation column
  composition in tens of minutes to hours; a recycle loop can take several residence
  times. Change, wait, observe, then change again.
- **One change at a time** where you can, so you know what caused what.
- **Know the envelope:** safe operating limits (trip points) and integrity operating
  windows (IOWs — e.g. max temperature for a material, max ramp rate for a vessel).
  Plan the transition to stay well inside both.

## 2. Startup (from a written procedure, always)
Typical shape — your procedure governs:
1. **Pre-start checks:** permits closed, isolations removed, blinds swung, instruments
   and trips tested/proved, utilities (steam, cooling water, nitrogen, instrument
   air, power) available.
2. **Inerting/purging** where flammables are involved, verified by O₂ measurement.
3. **Establish circulation** on solvent or inert fluid where the design allows
   (e.g. cold or hot circulation before feed). Get pumps, levels and flows stable.
4. **Heat up at the allowed ramp rate** (thermal stress on vessels and exchangers).
5. **Introduce feed at minimum stable rate**, put loops in AUTO in the right order
   (inner/secondary loops first, then cascade primaries).
6. **Line out at low rate**, get on-spec, then ramp.
Each numbered stage ends at a **hold point**: a defined condition checked and signed
before moving on. Startups are high-risk because many systems are being changed
quickly; resist pressure to skip holds.

## 3. Rate changes
- Ramp feed in small steps (e.g. a few % of design per step — site-specific) and let
  the downstream units follow. Ratio and feed-forward controls help; if absent, move
  utilities (steam, reflux, cooling) ahead of or with the feed.
- Watch for the constraint that appears first at the new rate: a valve approaching
  fully open, a column approaching flood, a compressor approaching surge, a heater at
  max firing. That constraint sets your maximum.
- **Recycle loops** can amplify a small change (the "snowball" effect): watch recycle
  flows and inventories during and after the ramp.
- Rate cuts are not automatically safe: low rates can cause weeping in columns, low
  flow trips on pumps and heaters, and minimum-turndown problems on burners.

## 4. Upset and trip recovery
1. **Make safe:** confirm the trip actions happened (valves to fail positions, pumps
   stopped, heaters out). Do not assume — check on the board and in the field.
2. **Find the cause** before restarting: first-out indication, event log, field report.
   Restarting into the same fault produces a second, often worse, trip.
3. **Stabilise the inventory:** levels and pressures under control, flaring or
   venting stopped where possible.
4. **Restart from the appropriate stage** of the startup procedure, not from where you
   were. A hot restart has its own procedure for good reason.
5. **Route off-spec** to slop/recycle until analysers and lab confirm quality.
6. Record the event; feed it into the incident or near-miss system.

## Gotchas
- Bypassing a trip "just for the startup" is a leading cause of major incidents; use
  only authorised, documented startup overrides that remove themselves.
- Analysers lag; a line-out "on spec" by the analyser may already be drifting off.
- Liquid in a gas line or a level transmitter reading wrong on a cold start (density
  compensation set for operating conditions) can fool you badly.

## Verify
- [ ] Every hold point in the procedure confirmed and signed.
- [ ] Ramp steps sized to the slowest-responding loop; waited for line-out between steps.
- [ ] Identified the binding constraint at the new rate.
- [ ] After a trip, cause found and trip actions confirmed before restart.
- [ ] Off-spec routed and quantified; event recorded.

*Draft note:* step sizes and ramp rates are deliberately not given as numbers; they
are unit- and equipment-specific and come from your operating procedures.
