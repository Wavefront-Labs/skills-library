---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.current-limit-and-power-derating
name: current-limit-and-power-derating
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [power-derating, current-limit, peak-power, soc-limit, temperature-derating, charge-limit]
level: practitioner
status: draft
description: "Calculate and communicate battery charge and discharge current limits across temperature, SOC and voltage, including peak durations and derating curves."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Current limit and derating

1. Limits come from several constraints and the final limit is the **minimum**: cell voltage limits (using the ECM: `I_max = (Vmax - OCV - V_rc)/R0`), cell current ratings by temperature, SOC window, temperature limits, plating protection (charge), busbar/fuse/contactor ratings, ageing policy.
2. Time windows: provide continuous, 10 s, and 30 s style limits (check the vehicle control's needs), recomputed every cycle.
3. Temperature derating: taper smoothly toward zero outside the permitted window; avoid abrupt steps that cause torque jerks.
4. SOC derating: reduce discharge at low SOC and charge at high SOC so the voltage limit is not hit.
5. Interface: send the limits to the vehicle controller over the network; the controller restricts motor power and regen accordingly; confirm update rate and signal validity.
6. Test: climate chamber at low and high temperature, drive profiles with pulse loads.
7. Ageing: scale limits with resistance growth, otherwise voltage cut-offs trigger.

**Gotchas:** inconsistent sign conventions between charge and discharge signals.

## Verify
- [ ] Voltage never crosses cell limits during limit-testing.
- [ ] Derating curves documented and smooth at boundaries.
