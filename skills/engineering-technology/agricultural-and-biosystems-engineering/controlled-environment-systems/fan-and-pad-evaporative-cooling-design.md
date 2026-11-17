---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.fan-and-pad-evaporative-cooling-design
name: fan-and-pad-evaporative-cooling-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, fan-pad-cooling, greenhouse-heating, greenhouse-cooling, evaporative-cooling, pad-area, saturation-efficiency, wet-bulb]
level: practitioner
status: docs-checked
description: "Design fan-and-pad evaporative cooling: required airflow, pad area and face velocity, pad saturation efficiency, achievable temperature drop, water supply and maintenance."
sources:
  - "https://en.wikipedia.org/wiki/Evaporative_cooler"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Fan-and-pad evaporative cooling design

**Goal:** cool incoming air to near wet-bulb temperature at the required airflow.

## Performance
Air leaving the pad: `T_out = T_db - eta (T_db - T_wb)`, where eta is the pad saturation efficiency (take it from the pad maker's data; efficiency falls as velocity rises). The temperature drop is limited by the outdoor wet-bulb depression, so evaporative cooling works best in dry climates and less well in humid weather.

## Sizing steps
1. **Airflow**: size fans to deliver the design ventilation rate. Compute the required flow from the sensible heat balance (see the heat-balance skill) for your allowed temperature rise across the house.
2. **Pad area** `A_pad = Q / v_face`; take the face velocity from the pad maker's data.
3. **Pad thickness**: thicker gives higher efficiency but more pressure drop.
4. **Static pressure**: the pad adds loss (maker's curve), so add it to the fan static pressure.
5. **Fan-to-pad distance**: keep runs short (the maker or handbook sets the limit); longer runs produce a larger temperature gradient; use cross-ventilation or staged systems for large houses.
6. **Water**: recirculating pump and distribution header; a bleed-off keeps dissolved solids from accumulating; supply water per metre of pad as set by the maker's data; sump size; algae control.
7. **Controls**: stage fans, run pad pump with fans; shut pads off at low humidity temperatures and drain in winter.

## Gotchas
- Poor water quality (hardness) scales pads.
- Combined with CO2 enrichment, large venting conflicts.

## Verify
- [ ] Measure dry bulb and wet bulb at pad inlet and outlet; compute eta and compare with the pad specification.

## Checked
2026-11-01. The saturation-efficiency relation and A_pad = Q / v_face are definitions and were checked by derivation. Removed all quoted efficiency ranges, study results, face velocities, pad thicknesses, static pressure, water-rate and air-change figures (no readable source fetched); take them from the pad and fan makers.
Method: documentation only; no commands were run.
