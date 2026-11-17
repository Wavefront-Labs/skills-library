---
id: energy-mining-utilities.energy-storage-operations.battery-management-systems.triaging-bms-alarms-and-cell-imbalance
name: triaging-bms-alarms-and-cell-imbalance
category: energy-mining-utilities
field: energy-storage-operations
product: battery-management-systems
tags: [battery-management-systems, bms, ems, energy-management-system, cell-voltage, cell-temperature, voltage-spread, delta-v, cell-imbalance, balancing, passive-balancing, active-balancing, soc-estimation, coulomb-counting, ocv, soh, state-of-health, alarm-triage, warning, alarm, fault, protection-trip, derating, current-limit, insulation-monitoring, firmware, rack, module, lfp, nmc, lithium-ion]
level: practitioner
status: draft
description: "Read BMS and EMS data: cell voltage and temperature spreads, alarm levels and what each implies, balancing diagnostics, SOC/SOH estimates, and why the system derated."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Triaging BMS alarms and cell imbalance

**Goal:** use battery management system (BMS) and site EMS data to decide which alarms
matter, why capacity or power is being limited, and when a module needs replacing.

> Status: draft. Hierarchy names (cell/module/rack/bank), alarm levels and thresholds
> come from your integrator. LFP and NMC chemistries behave differently in voltage —
> LFP's flat voltage curve in particular makes SOC from voltage unreliable.

## 1. The data hierarchy
- **Cell** voltages and temperatures (sometimes per cell, sometimes per group of
  parallel cells), aggregated to **module**, **rack** (series string) and **bank/
  container**. The site **EMS** sits above the BMS and talks to the PCS and SCADA.
- Read the rack summary: max/min/avg cell voltage, max/min temperature, SOC, SOH,
  current, insulation resistance, and the current/power limits the BMS is publishing.

## 2. Alarm levels
Most BMSs use three tiers (names vary):
- **Warning:** approaching a limit — investigate, no action forced.
- **Alarm:** limit reached — BMS reduces allowed current (derate).
- **Fault / protection:** contactors open; rack goes offline. Usually needs a manual
  reset after the cause is understood.
Triage questions: which rack/module/cell? Is it one cell or the whole rack? Is it
temperature, voltage, current, insulation or communication? Is it new or recurring?

## 3. Cell imbalance
- **Voltage spread (ΔV)** = max − min cell voltage in a rack. Compare at **rest**
  (after an hour or so without current) and at the ends of charge/discharge, where
  differences show most clearly. In LFP, the mid-SOC plateau hides imbalance; look at
  the top of charge.
- One cell consistently **high at top of charge** and **low at bottom of discharge**:
  likely lower capacity (ageing or defect) — it limits the whole series string.
- One cell low at all SOCs and drifting lower at rest: possible **self-discharge /
  internal short** — a safety concern; escalate.
- **Balancing:** passive balancing bleeds energy from high cells through resistors,
  usually near top of charge, at low current — it can take many cycles to correct a big
  imbalance. Check balancing is enabled and active on the affected rack; a balancing
  circuit fault looks like a stuck imbalance.

## 4. Temperature
- Hot spots in one module: check cooling airflow/coolant to that module, connector
  resistance (a loose busbar heats locally), and cell condition.
- Rack-wide high temperature: HVAC issue, high C-rate dispatch, or ambient conditions.

## 5. Why did it derate?
The BMS publishes charge/discharge current limits; the EMS and PCS follow them. Common
causes: temperature too high or too low, SOC near the ends, a cell voltage limit,
insulation fault, communication loss to a module, or a **firmware rule** (e.g. reduced
limits at low SOH). Read the limit reason codes; compare with the integrator's
derating tables.

## 6. SOC and SOH
- SOC is usually estimated by **coulomb counting** corrected by voltage/OCV at rest.
  Errors accumulate; periodic full charges recalibrate.
- SOH from capacity tests or BMS models trends ageing; compare racks — an outlier rack
  points at a specific problem rather than normal ageing.

## Gotchas
- Communication loss can look like a cell fault; check comms first.
- Don't reset protection faults repeatedly to restore availability.
- Firmware updates change limits and alarm behaviour — record versions.

## Verify
- [ ] Alarm located to cell/module/rack and classified by type and tier.
- [ ] ΔV judged at rest and at end of charge, not mid-plateau.
- [ ] Balancing confirmed active where imbalance exists.
- [ ] Derate reason code identified.
- [ ] Self-discharge suspects escalated as safety issues.
