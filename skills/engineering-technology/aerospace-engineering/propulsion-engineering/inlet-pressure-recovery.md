---
id: engineering-technology.aerospace-engineering.propulsion-engineering.inlet-pressure-recovery
name: inlet-pressure-recovery
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, inlets, nozzles, inlet-pressure-recovery, pressure-recovery, ram-recovery, mil-e-5008b, supersonic-inlet, distortion]
level: practitioner
status: gated
description: "Estimate inlet total-pressure recovery from subsonic to supersonic flight with MIL-E-5008B-style relations, and design for distortion and shock losses."
sources:
  - "Mattingly, Elements of Propulsion"
  - "Seddon and Goldsmith, Intake Aerodynamics"
  - "MIL-E-5008B"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Inlet pressure recovery

**Goal:** inlet total-pressure ratio at the engine face over the flight envelope.

## Estimates
- Subsonic inlets: recovery `eta_r` of about 0.97-0.995 depending on length, lip radius and internal losses (gated: unconfirmed, source is paywalled or blocked). NASA Glenn gives the military-specification subsonic value as the inlet efficiency itself (`pt2/pt0 = ni`).
- Supersonic: the military specification relation `eta_r = 1 - 0.075 (M0 - 1)^1.35` for `1 < M0 < 5` (NASA Glenn inlet page, multiplied by the inlet efficiency `ni`) is a good first estimate; NASA states actual performance may be greater but is usually less than the specification value, so confirm with inlet data.
- Ram recovery relates to normal-shock total-pressure loss (see normal shock skill): at M 2 a normal shock leaves 72% total pressure, so a multi-shock inlet is needed at higher Mach (the threshold of about M 1.6 is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)).

## Design considerations
- Diffuser design, boundary-layer bleed, bypass doors and ramp or cone angles.
- Distortion (circumferential, radial) at the engine face must be within the engine's limits; tools: total-pressure rake data.
- Buzz and unstart in supersonic inlets need control (variable geometry or bleed).

## Procedure
1. Compute `eta_r` vs Mach for each design candidate.
2. Include recovery in the cycle deck as inlet total pressure ratio.
3. Verify with CFD and wind-tunnel data; define the distortion index per the engine specification.

## Gotchas
- Using a single recovery value for all Mach and angle of attack.
- Ground operation with static inlet suction and crosswind needs separate checks.

## Verify
- [ ] At M0 = 2 the formula gives about 0.925; compare to a normal-shock-only value (0.72) to see the margin.
