---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.range-estimation-method
name: range-estimation-method
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [range-estimation, ev-range, usable-energy, range-prediction, consumption-correction, soc-window]
level: practitioner
status: gated
description: "Estimate and display EV range: usable energy, consumption model, corrections for temperature, speed and ageing, and the uncertainty and test-cycle basis."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "UN GTR No. 15 (WLTP), unece.org global technical regulations; confirm current text"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Range estimation method

1. Usable energy = nominal pack energy x usable SOC window x state of health (ageing) x temperature correction, not the headline gross capacity.
2. Consumption model: baseline Wh/km for a reference cycle, adjusted by speed distribution, temperature (HVAC and battery efficiency), route grade, payload, tyres.
3. Test-cycle range: regulatory cycles (WLTP in many regions, EPA in the US, others) produce certified range; the procedures differ and certified values are generally higher than mixed real-world use (gated: unconfirmed, source is paywalled or blocked). Confirm the cycle used in the target market.
4. Display range: use recent consumption averaged over a window blended with a baseline; avoid rapid swings; show a pessimistic bound at low SOC.
5. Navigation-aware prediction: add route elevation, speed limits and charging stops.
6. Validate: constant speed ranges (e.g. 90 and 120 km/h, illustrative), cold and hot, aged packs.

**Gotchas:** SOC non-linearity near empty; usable window shrinks in the cold.

## Verify
- [ ] Predicted vs measured range for at least three speed/temperature conditions.
- [ ] Error bound stated for the displayed range.
