---
id: energy-mining-utilities.energy-storage-operations.battery-storage-operation.running-a-grid-battery-plant-shift
name: running-a-grid-battery-plant-shift
category: energy-mining-utilities
field: energy-storage-operations
product: battery-storage-operation
tags: [battery-storage-operation, bess, battery-energy-storage-system, grid-scale-battery, utility-scale-storage, state-of-charge, soc, soc-headroom, soh, state-of-health, pcs, power-conversion-system, inverter, inverter-fault, container, enclosure, hvac, thermal-management, liquid-cooling, frequency-response, ffr, fcas, ancillary-services, scada, ems, poi, point-of-interconnection, control-room-operator, lithium-ion, lfp]
level: practitioner
status: draft
description: "Operate a grid-scale BESS shift: SOC headroom for committed services, container thermal and HVAC watch, PCS/inverter fault response, frequency events, and the shift log."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a grid battery plant shift

**Goal:** keep the battery available to deliver what it has been committed to — energy,
frequency response, reserve — while staying inside thermal and electrical limits.

> Status: draft. Grid services, their names (FFR, FCAS, regulation, reserve) and their
> rules differ by market and system operator; plant limits come from the integrator's
> operating manual and warranty. Values below are illustrative.

## 1. Start of shift
- Read the **dispatch schedule** and service commitments for the shift (see
  energy-mining-utilities.energy-storage-operations.storage-dispatch.scheduling-battery-charge-discharge-and-services).
- Check the plant's **available power and energy** against what is committed. Any
  offline racks, containers or inverters reduce both; if it falls short, the trader or
  dispatcher must be told so availability can be re-declared.
- Review alarms carried over, equipment out of service, and permits/isolations in force
  (see energy-mining-utilities.energy-storage-operations.battery-plant-maintenance.isolating-and-swapping-a-battery-module).

## 2. State of charge management
- Services need **headroom**: frequency response needs room to both charge and
  discharge for the required duration; energy trading needs SOC at the right level
  by the right time.
- Know the **usable SOC window** (the EMS often maps a narrower band, e.g. 5–95%, onto
  "0–100% usable" — confirm how your plant displays it). Operating near the ends
  triggers derating.
- **SOC drift / calibration:** SOC estimates drift over time; plants do periodic full
  charges or balancing to recalibrate. A rack whose SOC differs from its neighbours
  limits the whole string.

## 3. Thermal watch
- Cells age fastest when hot. Watch **cell temperature spread** (max−min) and
  absolute maximum per container, HVAC or liquid-cooling unit status, and enclosure
  ambient temperature.
- Rising spread or one container running hotter: check its HVAC/chiller, door seals,
  and whether its racks are carrying more current (imbalance).
- Heatwaves reduce HVAC capacity just when grid demand is high; derating may follow
  — anticipate it in availability.

## 4. Inverter (PCS) and electrical faults
- PCS trips: read the fault code, check whether it's a grid event (voltage/frequency
  ride-through), a DC-side fault (insulation, ground fault), or an internal fault
  (IGBT, cooling fan, communication).
- **Insulation/ground fault alarms on the DC side** are taken seriously — they can
  indicate damaged cabling or water ingress. Don't simply reset repeatedly.
- Reset per procedure, and only after classification. Repeated identical trips →
  maintenance ticket and isolate the unit.

## 5. Frequency events
- When a frequency excursion occurs, confirm the plant responded (power vs frequency
  droop or the contracted response curve) and that data is logged at the required
  resolution — under-performance can lead to penalties or disqualification.
- Afterwards, restore SOC to the service window.

## 6. Off-normal: thermal runaway indicators
Off-gas detection (H₂, CO, VOC), smoke detection, rapid cell temperature rise or
voltage collapse in a module → follow the **emergency response plan**: do not open the
enclosure, keep people away, notify the fire service with the site's pre-incident
plan. Deflagration risk exists inside closed enclosures.

## Gotchas
- An "available" plant with stale SCADA data isn't available — check comms health.
- Auxiliary load (HVAC) draws grid energy even when idle; include it in losses.
- Firmware updates can change limits silently; check after any update.

## Verify
- [ ] Available MW/MWh compared with commitments; shortfalls declared.
- [ ] SOC inside the window needed for each service.
- [ ] Temperatures and spreads within limits; HVAC healthy.
- [ ] Faults classified before reset; repeats escalated.
- [ ] Frequency event performance recorded.
