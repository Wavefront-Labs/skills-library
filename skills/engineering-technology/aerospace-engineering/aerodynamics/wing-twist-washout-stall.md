---
id: engineering-technology.aerospace-engineering.aerodynamics.wing-twist-washout-stall
name: wing-twist-washout-stall
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, finite-wing, washout, twist, stall-progression, spanwise-loading, tip-stall, aileron-effectiveness, stall-strip]
level: practitioner
status: draft
description: "Design wing twist and washout so the wing stalls inboard first, check the spanwise cl distribution against section cl_max, and know the induced-drag cost."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Anderson, Fundamentals of Aerodynamics"
  - "Nicolai and Carichner, Fundamentals of Aircraft and Airship Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Twist and washout for stall progression

**Goal:** first stall at the inboard wing so ailerons stay effective and the aircraft does not drop a wing.

## Method
1. Obtain the spanwise lift distribution `cl(y)` from lifting-line or a vortex-lattice run at wing `CLmax`.
2. Obtain the section `cl_max(y)` including local Reynolds number (chord changes along the span) and any high-lift device.
3. Plot the stall margin `cl_max(y) - cl(y)`; the minimum should sit inboard (often 30-60% span), not at the tip.
4. If the tip is critical, add geometric washout (negative twist toward tip), use a higher-`cl_max` tip section, add a leading-edge device on the outboard wing, or use stall strips inboard to trigger early separation.

## Typical practice
- Washout of a few degrees is common on straight wings; swept wings need more care because sweep moves load outboard and promotes tip stall.
- Twist is optimal for one `CL` only; at other `CL` the induced drag rises slightly, usually a small penalty.

## Gotchas
- Elliptic loading is not stall-safe; it brings the whole span to its limit nearly together.
- Aeroelastic twist can change the distribution; check with flexible loads for swept wings.
- Compressibility and Reynolds effects shift `cl_max(y)` between sea level and altitude.

## Verify
- [ ] Margin plot shows the minimum margin inboard of the aileron.
- [ ] Flight or wind-tunnel stall behaviour (tufts or oil flow) matches the predicted first-stall location.
