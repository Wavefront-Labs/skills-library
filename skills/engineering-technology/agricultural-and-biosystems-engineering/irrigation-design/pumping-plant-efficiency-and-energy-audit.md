---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.pumping-plant-efficiency-and-energy-audit
name: pumping-plant-efficiency-and-energy-audit
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, pumping-plant-efficiency, irrigation-pumping, pump-selection, energy-audit, kwh-per-m3, pump-testing, irrigation-energy]
level: practitioner
status: verified
description: "Measure overall pumping plant efficiency from flow, lift and kilowatts, compute kWh per cubic metre and cost, and decide on pump or motor repair, replacement or resizing."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pumping plant efficiency and energy audit

**Goal:** show how much energy is wasted and whether a fix is cost-effective.

## Measurements
1. Flow: ultrasonic or propeller meter on a straight pipe run (follow the maker's straight-run requirements).
2. Total head: discharge pressure (gauge) converted to metres, plus the pumping water level (drawdown for wells) and velocity head corrections.
3. Input power: kWh meter pulses, or clamp meter power measurement (three-phase power).

## Calculations
- Water power `P_w (kW) = 9.81 Q (m3/s) H (m)`.
- Overall pumping plant efficiency `OPPE = P_w / P_input`.
- Energy per volume: `kWh/m3 = 0.002725 H (m) / OPPE` (the constant is 9.81 x 1000 / 3.6e6 = 0.002725, computed).
- Annual energy cost = volume x kWh/m3 x tariff.

## Interpret
Compare OPPE to regional pumping-plant performance guidelines (for example, state performance criteria used in U.S. irrigation programs) and the pump's own efficiency curve. Low efficiency can be pump wear, wrong duty point, throttling, motor sizing or the suction-side limits. Savings = (kWh/m3 current - kWh/m3 target) x annual volume x tariff; compare to repair or replacement cost for a payback period.

## Gotchas
- Peak-demand charges and time-of-use tariffs change the economics.
- Flow measurement error dominates; check against a second method.
- Well drawdown varies over the season.

## Verify
- [ ] Efficiency computed at three operating points; duty point recorded.
