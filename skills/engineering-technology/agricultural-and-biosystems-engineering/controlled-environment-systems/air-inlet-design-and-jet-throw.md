---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.air-inlet-design-and-jet-throw
name: air-inlet-design-and-jet-throw
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, inlet-design, ventilation-design, natural-ventilation, air-inlet, jet-throw, coanda-effect, negative-pressure]
level: practitioner
status: draft
description: "Design ventilation inlets: area from static pressure and velocity, jet throw to carry cold air along the ceiling, baffle and slot settings, and negative-pressure control."
sources:
  - "Albright, Environmental Control for Animals and Plants (ASAE)"
  - "MWPS Midwest Plan Service, Structures and Environment Handbook"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Air inlet design and jet throw

**Goal:** fresh air that mixes with warm air before it falls on animals or plants.

## Principle
Inlet velocity is set by the pressure difference across the opening: `v = sqrt(2 dP / rho)`. For a pressure difference of 10 Pa the velocity is about 4 m/s; for 20 Pa about 5.8 m/s. In cold weather minimum ventilation, a jet velocity of about 4-5 m/s (or per the handbook) is needed so that the jet clings to the ceiling (Coanda effect) and travels some distance before dropping.

## Design
1. Inlet area: `A = Q / v`; choose the stage-specific flow and the pressure, then size slot height and length to obtain the design velocity at minimum ventilation.
2. Control the pressure difference with a controller that modulates inlet openings via actuators or weights so velocity stays constant as fans stage in.
3. Place slots at the ceiling or along the wall; choose baffles and deflectors to direct the jet along the ceiling; avoid gaps and leaks elsewhere (see the infiltration skill).
4. Throw distance depends on inlet velocity, height and temperature difference; if the jet drops early, reduce opening size.
5. In winter use ceiling inlets or attic inlets for pre-warming; in summer open more inlets (side curtains or tunnel inlets).

## Gotchas
- Too much leakage in the building makes inlets ineffective.
- Inlets facing the wind direction need protection.

## Verify
- [ ] Smoke test shows the jet following the ceiling a design distance; the static pressure sensor reads the target.
