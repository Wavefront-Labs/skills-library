---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.infiltration-and-air-tightness-of-enclosures
name: infiltration-and-air-tightness-of-enclosures
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, infiltration-loss, enclosure-heat-balance, ce-psychrometrics, air-changes-per-hour, tracer-gas, blower-door, air-tightness]
level: practitioner
status: draft
description: "Estimate and measure infiltration in greenhouses and buildings using air changes per hour, the 0.34 factor, tracer-gas decay and pressurisation tests, and set sealing priorities."
sources:
  - "Albright, Environmental Control for Animals and Plants (ASAE)"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Infiltration and air-tightness of enclosures

**Goal:** the air leakage heat load and a plan to cut it.

## Estimate
`Q_inf (W) = 0.34 x n x V_house x (T_in - T_out)` where n is air changes per hour and V_house the interior volume (m3); the constant 0.34 is air density times specific heat divided by 3600 (computed: 1.2 x 1005 / 3600 = 0.335). Typical n values depend on cover, age and wind (figures of about 0.5-1 per hour for new film houses and 1-2 or more for old glass houses are practice values not confirmed from a free source; measure with the tracer method). Wind and temperature difference increase it.

## Measurement
1. **Tracer-gas decay**: release CO2 or another safe tracer, mix, then record the decay; `n = (1/t) ln (C0 / Ct)`. Keep vents closed and the system in the condition being evaluated.
2. **Fan pressurisation** (blower door style): measure airflow at a set pressure difference to compare houses (leakage rate at 50 Pa for buildings, or lower pressures for greenhouses with film).
3. **Smoke or thermal imaging** to locate leaks.

## Sealing priorities
Vent seals and rack gaskets, end walls and doors, film tears, gutter joints, penetrations for pipes, curtain seals, and in livestock buildings inlets and doors not designed for ventilation.

## Gotchas
- A tight house needs ventilation controlled by design, not by leakage.
- Combustion heaters need air supply; sealing the house can cause backdrafting or incomplete combustion if combustion air is not provided.

## Verify
- [ ] Repeat the test after sealing and compare n.
