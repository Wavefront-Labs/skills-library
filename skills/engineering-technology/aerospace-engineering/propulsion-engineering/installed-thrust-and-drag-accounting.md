---
id: engineering-technology.aerospace-engineering.propulsion-engineering.installed-thrust-and-drag-accounting
name: installed-thrust-and-drag-accounting
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [installed-thrust, thrust-drag-bookkeeping, net-thrust, ram-drag, spillage-drag, engine-installation]
level: practitioner
status: draft
description: "Account installed thrust as uninstalled net thrust less inlet, nacelle and afterbody drag and bleed penalties, without double counting airframe drag."
sources:
  - "Mattingly, Elements of Propulsion"
  - "Seddon and Goldsmith, Intake Aerodynamics"
  - "Raymer, Aircraft Design: A Conceptual Approach"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Installed thrust and drag accounting

**Goal:** the thrust the airframe actually receives, with an unambiguous thrust-drag boundary.

## Terms
- Gross thrust `Fg = mdot_e Ve + (pe - p0) Ae`; ram drag `mdot_0 V0`; uninstalled net thrust `Fn = Fg - ram drag`.
- Installation losses: inlet spillage (additive) drag, boundary-layer diverter or bleed drag, nacelle friction and form drag, nozzle boattail and interference drag, pylon interference, bleed and power-extraction penalties (they lower fuel efficiency and thrust).
- Installed thrust `F_inst = Fn - (installation drags charged to the propulsion system)`.

## Bookkeeping rule
Draw a control surface that separates "propulsion" from "airframe". Any force on the nacelle outside that surface is airframe drag, and any force inside is part of thrust. Define it once and use it in the performance model, wind tunnel data and flight test. Industry bookkeeping standards exist (SAE documents on thrust and drag definitions); consult your programme's definition.

## Procedure
1. Take uninstalled thrust from the engine deck at the flight condition, with declared bleed and power extraction.
2. Compute inlet spillage and nacelle drags from CFD, wind-tunnel data or empirical methods.
3. Subtract per the control-surface definition; do not also include the same drag in the aircraft drag polar.
4. Re-run climb, cruise and one-engine-out performance with installed thrust.

## Gotchas
- Double counting nacelle drag in both the polar and the thrust decrement is a common error.
- Power-off and idle installed drag matter for descent and engine-out.

## Verify
- [ ] A written statement defines the thrust-drag boundary and every term is on exactly one side.
