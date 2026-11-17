---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.mechanical-vapour-recompression
name: mechanical-vapour-recompression
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, vapour-recompression, mvr, tvr, evaporator-energy, compressor, heat-pump-evaporation]
level: advanced
status: draft
description: "Assess mechanical or thermal vapour recompression for evaporators: temperature lift, compressor power, energy saving versus multi-effect and operating limits."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mechanical vapour recompression

**Goal:** reuse the evaporator's own vapour as the heating steam by raising its pressure, so very little live steam is needed.

## Principle
Mechanical vapour recompression (MVR) compresses the vapour leaving the evaporator by a small amount (the saturation temperature rises by a few kelvin to perhaps 10 K, set by the boiling point elevation and the heat transfer driving force) and sends it back to the heating side. The compressor is driven by an electric motor, so the process swaps live steam for electricity. Thermal vapour recompression (TVR) uses a steam jet ejector with live steam to recompress part of the vapour; it is cheaper and simpler but gives less saving.

## Energy view
The electricity needed per kg of water evaporated is small compared with the latent heat; a typical MVR evaporator needs a fraction of the energy of a single-effect unit, comparable to or better than a multi-effect evaporator with many effects. The saving depends on the temperature lift: smaller lift (low BPE, high U) gives lower power. Compare on primary energy and cost, since electricity and fuel prices differ.

## Limits
- High boiling point elevation (strong solutions) increases the lift and power.
- Compressors need clean vapour: entrainment control is vital (demisters) to avoid damage and product carryover.
- Start-up requires an external steam source or an electric heater until the compressor is running.
- Plant availability and maintenance of the compressor (large fans or roots blowers).

## Verify
- [ ] Specific energy per kg water evaporated measured.
- [ ] Entrainment check at the demister outlet.
- Unconfirmed: compressor types and lift limits by maker.
