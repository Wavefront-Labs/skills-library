---
id: engineering-technology.chemical-engineering.piping-instrumentation.vapour-and-two-phase-line-sizing
name: vapour-and-two-phase-line-sizing
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-line-sizing, vapour-and-two-phase-line-sizing, gas-line-sizing, two-phase-flow, erosional-velocity, api-rp-14e, flow-regime, slug-flow, rho-v-squared, compressible-flow, lockhart-martinelli]
level: advanced
status: gated
description: "Size vapour and two-phase lines: compressible-flow pressure drop, velocity and rho-v-squared limits, erosional velocity, flow regime checks and slug avoidance."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vapour and two-phase line sizing

**Goal:** line sizes for gas and two-phase service that avoid erosion, noise and slugging.

## Vapour lines
1. Limit pressure drop to a fraction of the line pressure (for example a few percent; stricter for compressor suction, vacuum and relief headers).
2. Use compressible-flow equations when the pressure drop exceeds about 10 to 20% of the inlet pressure; otherwise the incompressible Darcy equation at the average density is acceptable.
3. Typical velocity guidance: well below sonic velocity, often kept under about 0.3 to 0.5 Mach and, for noise and vibration, within company limits (values of 15 to 30 m/s are typical for general gas lines; much lower for vacuum).

## Two-phase lines
1. **Erosional velocity** (API RP 14E): V_e = C/sqrt(rho_m), with rho_m the mixture density; C = 100 in field units (ft/s, lb/ft3) (gated: unconfirmed, source is paywalled or blocked), which converts to 122 in SI (m/s, kg/m3; computed: 100 x 0.3048 x sqrt(16.018) = 121.99) for continuous service. Operators often use a fraction of this. Confirm the constant and applicability, especially for corrosive or solids-containing flow.
2. Check **rho_m v^2** (momentum flux) against a limit, often set by the company (of the order of several thousand Pa) to limit vibration.
3. **Flow regime**: plot on a Baker or Mandhane type map; avoid slug flow in lines feeding equipment sensitive to surging (compressors, columns, flare). Slug flow can be prevented by sizing for higher velocity or by a vertical rise and a slug catcher.
4. Pressure drop with a two-phase method (homogeneous model for a first estimate, Lockhart-Martinelli or Beggs-Brill for better results), including acceleration and static head.
5. Avoid pockets in long horizontal runs; slope to drain.

## Gotchas
- Flashing liquids (letdown valve) have large vapour fractions downstream; size the line downstream of the valve as two-phase.
- Relief and flare headers need specific criteria (Mach number limits per API 521; confirm).

## Verify
- [ ] Velocity below erosional limit at the maximum rate.
- [ ] Flow regime identified; slug risk assessed.
