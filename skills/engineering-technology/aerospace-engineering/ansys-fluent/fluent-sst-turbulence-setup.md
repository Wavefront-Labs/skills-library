---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-sst-turbulence-setup
name: fluent-sst-turbulence-setup
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-models, fluent-sst, k-omega-sst, turbulence-setup, viscous-model, production-limiter]
level: practitioner
status: draft
description: "Set up k-omega SST in Fluent for aerospace external flow: viscous panel options, near-wall treatment, freestream turbulence, and production limiter and curvature options."
sources:
  - "Ansys Fluent user guide (viscous models and k-omega SST)"
  - "Menter 1994 SST paper"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: k-omega SST setup

**Goal:** a correctly configured SST run for a wing or aircraft.

## Steps
1. **Setup > Models > Viscous:** choose **k-omega (2 eqn)**, then **SST**.
2. Options: **Production Limiter** (on; limits turbulence over-production in stagnation regions), **Curvature Correction** (only for strongly curved or rotating flows), **Compressibility Effects** (on for high speed), **Low-Re corrections** only for transition-sensitive work.
3. **Near-wall treatment:** mesh with `y+` about 1; Fluent's SST uses a blended y+-insensitive wall formulation so moderately larger y+ is tolerated.
4. **Boundary conditions:** in the pressure far-field panel set **Specification Method** (Intensity and Viscosity Ratio): for external aerodynamics typically low intensity (0.1% or below for free flight; use tunnel value for test comparisons) and viscosity ratio 1-10.
5. **Solution methods:** second-order upwind for flow and turbulence.

## Practice
- Run with the turbulence equations frozen initially, then enable them, or use hybrid initialization.
- Monitor turbulent viscosity ratio field after the run: values in the thousands in the freestream indicate bad inlet settings.

## Gotchas
- Default turbulence intensity for some boundary conditions is 5%, too high for flight: check the defaults.
- SST with y+ 30-100 is acceptable but not optimal.

## Verify
- [ ] Viscosity ratio field is moderate in the freestream.
- [ ] Skin friction trend matches a flat-plate check on the same mesh settings.
