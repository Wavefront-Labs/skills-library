---
id: engineering-technology.aerospace-engineering.propulsion-engineering.subsonic-diffuser-design
name: subsonic-diffuser-design
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [subsonic-diffuser, diffuser, inlet-design, flow-separation, distortion, dc60]
level: practitioner
status: draft
description: "Design a subsonic inlet diffuser for pressure recovery without separation, using area ratio, divergence angle, length and distortion limits at the engine face."
sources:
  - "Seddon and Goldsmith, Intake Aerodynamics"
  - "Mattingly, Elements of Propulsion"
  - "SAE ARP1420"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Subsonic diffuser design

**Goal:** slow the flow from the highlight to the compressor face with minimal loss and uniform flow.

## Parameters
- Area ratio `AR = A_exit/A_inlet`; ideal pressure-rise coefficient `Cp_ideal = 1 - 1/AR^2` for incompressible flow.
- Equivalent cone divergence angle; non-dimensional length `L/W1` (or `L/D`).
- Inlet blockage (boundary-layer thickness) and inlet Mach number.
- Face Mach number commonly in the range of about 0.4 to 0.6 for turbofans; confirm with the engine maker.

## Procedure
1. Fix the engine corrected flow and face Mach to get the face area.
2. Choose the throat Mach (set by the highest flight condition and the off-design cases, like take-off at high power).
3. Select a diffuser length from stall maps (Kline, Reneau and Johnston types): staying inside the "no appreciable stall" region for the given `AR` and `L/W1` requires total equivalent cone angles of only a few degrees to roughly ten.
4. For S-ducts, calculate the pressure and swirl distortion with CFD; compare circumferential distortion descriptor DC60 per SAE ARP1420 and the engine's allowable.
5. Consider boundary-layer control or vanes if length is limited.

## Gotchas
- Thick inlet boundary layers (from the nacelle lip at high angle of attack) lower the stall-free limit.
- Crosswind and high-incidence cases usually set the lip shape and diffuser requirement, not cruise.
- Maps are for straight, steady diffusers; curved or unsteady inlets need CFD and test.

## Verify
- [ ] Predicted total-pressure recovery and DC60 meet the engine specification at the critical flight and ground conditions.
