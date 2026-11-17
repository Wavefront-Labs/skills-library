---
id: energy-mining-utilities.renewable-energy-field-operations.wind-farm-scada.wind-farm-scada-alarm-triage-and-remote-reset
name: wind-farm-scada-alarm-triage-and-remote-reset
category: energy-mining-utilities
field: renewable-energy-field-operations
product: wind-farm-scada
tags: [renewable-energy-field-operations, wind-farm-scada, scada, wind-farm, roc, remote-operations-centre, alarm-triage, remote-reset, reset-policy, power-curve, availability, lost-production, cms, condition-monitoring, vibration-analysis, gearbox-bearing, temperature-trend, curtailment, grid-curtailment, setpoint, park-controller, ppc, shadow-flicker, bat-curtailment, ice-detection, 10-minute-data]
level: practitioner
status: draft
description: "Work a wind-farm SCADA desk: triage turbine alarms, decide when a remote reset is allowed, read power curve and CMS vibration trends, and handle grid curtailment."
sources:
  - "IEC 61400-25 (communications for monitoring and control of wind power plants) and IEC 61400-12-1 (power performance) concepts, paraphrased"
  - "Remote operations centre practice as described in industry O&M guidance, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wind-farm SCADA alarm triage and remote reset

**Goal:** maximise availability by resetting what is safe to reset, sending technicians to
what isn't, and spotting slow-developing failures in the data before they become big
component changes.

## 1. Know the reset policy before your first shift
Every owner/OEM has a **remote reset matrix**: which fault codes may be reset remotely,
how many times in what period (e.g. once, or max 2–3 per 24 h), and which require a site
visit. Typical "never remote reset" categories: safety chain/emergency stop, overspeed,
fire, vibration/shock sensor trips, brake faults, repeated pitch faults, any fault while
people are in the turbine.
Always check the **site personnel status** (who is on site, which turbines in service mode)
before any remote command.

## 2. Triage a stop
1. Read the **fault code and the surrounding event log** (what came before: grid event,
   temperature rise, pitch warnings).
2. Look at **10-minute (or faster) data** around the trip: wind speed, power, rotor speed,
   pitch angles, temperatures, grid voltage/frequency.
3. Classify: grid/external (many turbines tripped together on a grid dip), environmental
   (ice, high wind cut-out, cold-start), or turbine-specific (component).
4. If allowed by the matrix and the cause is understood → reset once and **watch it**
   restart and reach normal power. If it trips again → raise a job with your findings.

## 3. Trend reading
- **Power curve:** plot power vs nacelle-anemometer wind speed per turbine vs its
  neighbours. Under-performance at mid wind speeds can mean pitch/yaw misalignment,
  anemometer error, blade erosion or controller derating.
- **Temperatures:** gearbox bearing, oil, generator windings — compare to neighbours at
  the same power. A gradual rise ahead of the fleet suggests a developing bearing/cooling
  problem.
- **CMS vibration:** watch overall levels and frequency bands linked to specific gear stages
  and bearings; escalate to the vibration analyst when an alarm or a step change appears.
  Early bearing damage found by CMS can turn a crane job into an up-tower repair.

## 4. Curtailment and setpoints
- Grid operator instructions arrive via the park power controller or by phone/portal:
  active-power limit, ramp rates, reactive-power/voltage setpoints. Apply exactly, log the
  time and source of every instruction, and release only when instructed.
- Environmental curtailments run on schedules/sensors: shadow flicker, bats, birds, noise
  modes, ice. Confirm they are active as permitted — missing one is a permit breach.

## 5. Logging availability and lost production
Categorise every stop correctly (turbine fault, grid, scheduled maintenance, environment,
owner-requested). Availability guarantees in service contracts depend on these categories;
wrong labels cost money or start disputes.

## Gotchas
- Nacelle anemometers read the wake of the rotor; use transfer functions/neighbour
  comparison, not absolute numbers.
- Resetting a fault the matrix allows is still wrong if the data shows a real trend.
- Time zones: SCADA data often in UTC; grid instructions in local time.

## Verify
- [ ] Reset matrix and personnel status checked before every remote command.
- [ ] Each stop classified with data from before the trip.
- [ ] Repeat trips escalated with evidence, not reset again.
- [ ] Curtailment instructions applied, logged and released as instructed.
- [ ] Availability categories recorded correctly.

*Uncertain:* reset limits and categories differ by OEM contract and owner; follow yours.
