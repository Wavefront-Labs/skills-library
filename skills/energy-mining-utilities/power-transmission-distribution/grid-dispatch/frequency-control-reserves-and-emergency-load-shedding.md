---
id: energy-mining-utilities.power-transmission-distribution.grid-dispatch.frequency-control-reserves-and-emergency-load-shedding
name: frequency-control-reserves-and-emergency-load-shedding
category: energy-mining-utilities
field: power-transmission-distribution
product: grid-dispatch
tags: [grid-dispatch, system-operation, control-room, system-operator, dispatcher, balancing-authority, frequency-control, load-frequency-control, agc, automatic-generation-control, ace, area-control-error, primary-response, governor-droop, secondary-reserve, tertiary-reserve, spinning-reserve, contingency, n-1, inertia, rocof, ufls, under-frequency-load-shedding, manual-load-shedding, rotational-load-shedding, rolling-blackouts, interconnector, nerc, entso-e]
level: advanced
status: draft
description: "Keep grid frequency in band from the control room: how primary, secondary and tertiary reserves layer, reading ACE, responding to a large generator trip, and running manual load shedding."
sources:
  - "NERC balancing standards (ACE definition) and ENTSO-E/other operator handbooks on frequency containment and restoration reserves, summarised in general terms"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frequency control, reserves and emergency load shedding

**Goal:** hold system frequency near nominal (50 or 60 Hz) by matching generation to
demand second by second, recover cleanly after a big loss of generation, and — if
that fails — shed load in a controlled way before protection does it chaotically.
Your grid code, operating procedures and reserve rules set the actual numbers; values
below are illustrative.

## 1. The mental model
Frequency is the system's balance gauge: **generation > demand → frequency rises;
demand > generation → it falls.** The speed of the fall right after a loss depends
on system inertia (spinning mass); the depth depends on how fast reserves respond.
Low-inertia periods (light load, lots of inverter-based generation) mean faster
rate of change of frequency (RoCoF) and less time.

## 2. Reserve layers (names vary by region)
| Layer | Acts in | Mechanism | Your role |
|---|---|---|---|
| Primary / frequency containment | seconds | Governor droop, fast batteries, automatic | Make sure enough is online and enabled |
| Secondary / restoration (AGC) | ~30 s – 15 min | AGC adjusts unit setpoints to drive ACE to zero | Monitor AGC, units on control, limits |
| Tertiary / replacement | 15 min + | Dispatcher instructions, fast-start units | Call units to restore secondary margin |

**Area control error (ACE)** in NERC form is roughly
`ACE = (actual net interchange − scheduled) − 10·B·(actual f − scheduled f)`, with
B the area's frequency bias (MW per 0.1 Hz, negative). Positive ACE = you're over-
generating for your area. Watch its trend, not each tick.

## 3. Responding to a large generator trip
1. **Confirm it's real:** frequency dip, the unit's MW to zero, breaker status changed,
   interconnector flows jumping. Don't react to one bad telemetry point.
2. Let primary response arrest the fall; check frequency nadir vs. under-frequency
   load-shedding thresholds.
3. Check AGC is ramping secondary units; if AGC is out or saturated, dispatch manually.
4. **Restore reserve:** the trip just consumed your contingency reserve. Commit or
   call tertiary/fast-start units so the system is again secure for the *next* worst
   loss (N-1). Many rules give a fixed time to do this.
5. Watch interconnector limits; a neighbouring area may be supplying the deficit
   through a line now near its rating.
6. Log times, values, actions and who you spoke to.

## 4. Under-frequency load shedding (automatic)
UFLS relays at substations drop blocks of feeders in stages as frequency falls
(stage settings set by the grid code). You don't operate it, but you must know:
which feeders are in which stage, that the stage amounts are still realistic
(rooftop solar can turn a "load" feeder into a generator, so shedding it makes
things worse), and how to restore shed feeders in an order that doesn't trigger a
second dip.

## 5. Manual / rotational load shedding
Used when supply can't meet demand over hours (generation shortfall) or to relieve
an overloaded corridor.
- Use the **pre-agreed list**: exclude priority loads (hospitals, water pumping,
  critical telecoms) — but check they really are on separate feeders.
- Shed in **blocks and rotate** them (e.g. hourly) so no area is off for too long;
  publish the schedule to field and customer teams.
- Restore gradually; reconnecting a cold area produces cold-load pickup well above its
  normal demand.

## Gotchas
- Telemetry freezes look like stable values. Check timestamps.
- Shedding by distribution feeder now removes embedded generation too.
- Fatigue: emergencies happen late at night. Use checklists and second operators.

## Verify
- [ ] Contingency reserve after every event is recalculated and restored.
- [ ] ACE and frequency recovery within the region's recovery time.
- [ ] Load-shed lists current, with priority customers truly protected.
- [ ] Restoration staged; events logged with times and values.
