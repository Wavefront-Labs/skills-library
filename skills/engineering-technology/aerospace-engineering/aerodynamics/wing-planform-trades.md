---
id: engineering-technology.aerospace-engineering.aerodynamics.wing-planform-trades
name: wing-planform-trades
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, finite-wing, wing-planform-design, aspect-ratio, taper-ratio, sweep, conceptual-design, wing-weight]
level: practitioner
status: gated
description: "Trade aspect ratio, taper and sweep for induced drag, weight, stall behaviour and transonic performance when choosing a wing planform."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
  - "Anderson, Aircraft Performance and Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wing planform trades

**Goal:** a defensible planform (AR, taper, sweep, t/c) from competing requirements.

## Levers
- **Aspect ratio:** raises CL slope and cuts induced drag (`CDi = CL^2/(pi AR e)`), but wing weight, flutter margin and span limits (airport gate boxes) push back. Transports sit around 8-10, gliders far higher, fighters low (gated: unconfirmed, source is paywalled or blocked).
- **Taper:** about 0.4-0.5 gives near-elliptic loading for an unswept wing and lighter structure (more root chord, deeper root spar); Glauert lifting-line recomputed gives span efficiency e = 0.99 at taper 0.4-0.5 for AR 6, versus 0.95 rectangular and 0.89 for a pointed tip. Swept wings typically use a lower taper (around 0.2-0.4) to limit tip loading (gated: unconfirmed, source is paywalled or blocked).
- **Sweep:** delays drag divergence (effective Mach `M cos(Lambda)`), allows thicker sections, but lowers CL slope and CLmax, shifts load outboard, and brings pitch-up and tip-stall risks.
- **t/c:** thicker means lighter structure and more fuel volume but earlier wave drag.

## Procedure
1. Set wing loading from stall/landing and cruise requirements.
2. Choose sweep from cruise Mach and t/c via the drag-divergence estimate (see the drag polar skill).
3. Pick AR to balance induced drag against weight (use a sizing code to optimise range or fuel burn).
4. Choose taper to hit near-elliptic loading with the chosen sweep, then add twist (see washout skill).

## Gotchas
- Optimising for cruise alone ignores second-segment climb and approach, which are high-lift, low-speed conditions.
- The optimum AR moves with structural technology and span constraints; document the assumption.

## Verify
- [ ] Planform meets stall speed, climb gradient and cruise Mach with stated margins.
- [ ] Spanwise loading from a VLM run is near elliptic (e of about 0.9-0.95 or better).
