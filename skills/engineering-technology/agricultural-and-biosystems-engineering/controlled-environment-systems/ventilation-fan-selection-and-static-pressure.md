---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.ventilation-fan-selection-and-static-pressure
name: ventilation-fan-selection-and-static-pressure
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, ventilation-fan-selection, ventilation-design, natural-ventilation, fan-curve, static-pressure, fan-efficiency, variable-speed]
level: practitioner
status: draft
description: "Choose mechanical ventilation fans from the required airflow and system static pressure, using certified fan curves, staging, variable speed and energy efficiency ratios."
sources:
  - "Albright, Environmental Control for Animals and Plants (ASAE)"
  - "MWPS Midwest Plan Service, Structures and Environment Handbook"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ventilation fan selection and static pressure

**Goal:** fans that deliver the design airflow at the actual static pressure with good efficiency.

## Steps
1. **Airflow per stage**: from the heat and moisture balances (minimum, intermediate, maximum). Maximum ventilation is often set to hold the temperature rise at 2-3 K for animals or about 4-6 K in a greenhouse.
2. **System static pressure**: inlets, pads, screens, louvres, guards and ducts. For tunnel or cooled buildings, a design static pressure of about 25-50 Pa is common; check by calculation, and design for a safety margin because dirty shutters and screens add resistance.
3. **Fan data**: use performance curves from independent tests (for example the BESS Laboratory in the US, or maker's certificates under AMCA 210, ISO 5801 or ANSI/ASHRAE 51); read airflow at the design pressure rather than at free air; compare efficiency as airflow per watt (m3/h per W) at that pressure.
4. **Number and size of fans**: split capacity into stages: several fans with at least one on variable speed for smooth control; place fans to avoid short circuiting and so that stopped fans have backdraft shutters.
5. **Motors and controls**: choose EC or VFD-controlled motors for better efficiency at partial load; size electrical supply.
6. **Installation**: avoid obstructions within a fan diameter on the inlet side, keep clearance around shutters; guard fans for safety.

## Gotchas
- Selecting fans from nominal free-air flow causes under-ventilation.
- Dust-clogged shutters and belts reduce flow by large percentages; maintenance plan needed.

## Verify
- [ ] Measure actual system flow with an in-situ fan tester or traverse and compare with the design.
