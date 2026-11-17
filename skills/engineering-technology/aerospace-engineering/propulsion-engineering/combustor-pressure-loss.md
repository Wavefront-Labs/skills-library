---
id: engineering-technology.aerospace-engineering.propulsion-engineering.combustor-pressure-loss
name: combustor-pressure-loss
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [combustor-pressure-loss, combustor, pressure-drop, cold-loss, hot-loss, combustors-emissions]
level: practitioner
status: gated
description: "Estimate combustor total-pressure loss as cold flow loss plus the heat-addition (Rayleigh) loss, and see how liner pressure drop trades against mixing and cooling."
sources:
  - "Lefebvre and Ballal, Gas Turbine Combustion"
  - "Mattingly, Elements of Propulsion"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Combustor pressure loss

**Goal:** the total-pressure ratio `pi_b` used in cycle calculations, and what drives it.

## Components
- **Cold loss**: diffuser plus liner (dump, swirler, hole jets). Often expressed as `delta_p / q_ref` with `q_ref = 0.5 rho U_ref^2` at the reference (maximum casing section) area.
- **Hot loss**: from heat addition at constant area; for low Mach number approximately `delta_pt / pt = (gamma/2) * M_ref^2 * (T4/T3 - 1)`.
- Total loss is the sum. Typical combustor total-pressure losses are a few percent of compressor delivery pressure (commonly quoted around 4 to 7 percent for older, 3 to 6 percent for modern designs (gated: unconfirmed, source is paywalled or blocked)); engine data are the authority.

## Design interplay
- A higher liner pressure drop gives stronger jet penetration and mixing (better pattern factor and emissions control) and more cooling-film momentum, but costs thrust and specific fuel consumption.
- A lower `M_ref` (larger casing) reduces losses but adds weight and length.

## Procedure
1. Choose `M_ref` and the heat-release ratio `T4/T3` from the cycle.
2. Add a liner pressure-drop factor to reach the target mixing quality.
3. Compute `pi_b = 1 - (cold + hot loss)/pt3` and feed it to the cycle model.
4. Check sensitivity: 1 percentage point of `pi_b` is worth a measurable amount of thrust specific fuel consumption; run the cycle to quantify.

## Gotchas
- Quoting pressure drop at different reference stations makes numbers incomparable.
- Rig cold-flow data under-predict the loss at engine conditions unless hot loss is added.

## Verify
- [ ] Hot loss falls to zero when `T4 = T3`.
- Check (computed against the exact Rayleigh-flow total-pressure ratio, gamma 1.4): the low-Mach formula gives 0.35% at M_ref 0.05 and T4/T3 = 3 (exact 0.352%), 1.40% at M_ref 0.1 (exact 1.43%) and 2.1% at M_ref 0.1, T4/T3 = 4 (exact 2.16%); it is good to a few percent at M_ref <= 0.1.
