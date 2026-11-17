---
id: engineering-technology.aerospace-engineering.aerodynamics.wind-tunnel-wall-corrections
name: wind-tunnel-wall-corrections
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, wind-tunnel, aero-testing, wall-corrections, blockage-correction, lift-interference, tunnel-corrections, model-size]
level: advanced
status: verified
description: "Apply solid and wake blockage and lift-interference corrections to wind-tunnel data, and know when model size makes the data unusable."
sources:
  - "Barlow, Rae and Pope, Low-Speed Wind Tunnel Testing"
  - "AGARD AG-336, Wind Tunnel Wall Corrections"
  - "Ewald (ed.), Wind Tunnel Wall Corrections"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wind-tunnel wall corrections

**Goal:** data close to free-air conditions.

## Interference types
- **Solid blockage:** the model displaces flow and raises tunnel velocity at the model.
- **Wake blockage:** the model wake in a closed tunnel increases local velocity, depending on drag.
- **Lift interference:** walls change downwash: affects angle of attack, drag and pitching moment.
- **Buoyancy:** static pressure gradient along the test section.

## Procedure (closed tunnel, low speed)
Forms follow Pope, Rae and Pope, Low-Speed Wind Tunnel Testing (gated: unconfirmed, source is paywalled or blocked).
1. Compute blockage: `epsilon = epsilon_sb + epsilon_wb`, with the Rae and Pope forms (solid blockage proportional to model volume over test section area to the 3/2 power; wake blockage about `(S/4C) CD0`, S model area, C tunnel cross-section area; constants depend on the tunnel shape).
2. Correct velocity and dynamic pressure: `V_c = V (1 + epsilon)`, `q_c = q (1 + 2 epsilon)`.
3. Correct angle and drag for lift interference: `Delta alpha = delta (S/C) CL` (in radians, delta from boundary-factor tables) and corresponding drag increment `Delta CD = delta (S/C) CL^2`.
4. Recompute coefficients on corrected q.

## Practice
- Keep model frontal area under roughly 7-10% of the test section (rule of thumb for closed sections), and span below about 0.8 of tunnel width (gated: unconfirmed, source is paywalled or blocked).
- Transonic: use slotted or porous walls and wall-pressure-signature methods; the Prandtl-Glauert form is insufficient.

## Gotchas
- Large models at high lift can have corrections that dwarf the signal.
- Support (sting, strut) interference is separate and needs its own tare.

## Verify
- [ ] Corrections applied and the values recorded in the report.
- [ ] Repeat data in two tunnels or sizes agree after corrections.
