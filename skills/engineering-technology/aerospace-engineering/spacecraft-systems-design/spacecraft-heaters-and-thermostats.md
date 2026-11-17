---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.spacecraft-heaters-and-thermostats
name: spacecraft-heaters-and-thermostats
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [heaters, thermostats, survival-heaters, heater-sizing, thermal-control, thermistors]
level: practitioner
status: draft
description: "Design spacecraft heater circuits: operational and survival heaters, thermostat or software control, power budgets, redundancy and failure protection."
sources:
  - "Gilmore, Spacecraft Thermal Control Handbook"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Heaters and thermostats

**Goal:** keep hardware above its minimum temperature in the cold case without wasting power.

## Types
- **Operational heaters**: control a unit to its operating range during use.
- **Survival heaters**: keep the spacecraft above non-operating limits when in safe mode or off; must work without flight software.
- **Control methods**: mechanical thermostats (hard-wired, no software) or software control with thermistors and a deadband.

## Sizing
1. Cold case heat balance: required heater power `P = Q_loss - Q_dissipated` at the minimum temperature setpoint, with end-of-life MLI and the coldest environment.
2. Apply the duty cycle (power average) and the margin the programme requires (commonly a margin of at least 25 percent on heater power in the budget; use your programme's rule).
3. Set setpoints with a deadband (a few degrees) to avoid chatter, and survival setpoints below the operational ones.
4. Choose redundant circuits for critical items: separate thermostats and heater elements, one failed-on or failed-off should not kill the unit.

## Protections
- A thermostat failing closed may overheat hardware; add a second (series) overtemperature thermostat or software monitor.
- Fuse or current-limit each circuit through the power bus (see power-bus-architecture).
- Place sensors where the heater is controlling, not at a distance.

## Gotchas
- Heater power in eclipse competes with battery energy; include it in the eclipse budget.
- Thermostat tolerance (several degrees) must be included in the hot and cold cases.
- Test the heater circuits at cold temperature in thermal vacuum.

## Verify
- [ ] Cold-case thermal analysis with heater duty cycle holds all units above the survival and operating limits.
