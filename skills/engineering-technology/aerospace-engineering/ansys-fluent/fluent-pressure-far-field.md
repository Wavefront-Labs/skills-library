---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-pressure-far-field
name: fluent-pressure-far-field
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-boundary-conditions, pressure-far-field, far-field, mach-number, flow-direction, farfield-distance]
level: practitioner
status: draft
description: "Configure the pressure far-field boundary in Fluent for subsonic and transonic aerodynamics, including Mach, flow direction, temperature and domain size."
sources:
  - "Ansys Fluent user guide (pressure far-field boundary condition)"
  - "Fluent solver theory guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: pressure far-field

**Goal:** a freestream boundary for external compressible flow.

## Requirements
- Ideal-gas density must be on (the boundary is built for compressible flow with characteristic-based non-reflecting handling).
- Inputs: gauge pressure, Mach number, temperature, flow direction (x, y, z components), turbulence specification.

## Steps
1. **Boundary Conditions > pressure-far-field:** set Gauge Pressure (consistent with operating pressure; see ideal-gas skill), Mach Number, X/Y/Z-Component of Flow Direction, Temperature.
2. Compute flow direction for angle of attack alpha in the x-z plane: `(cos(alpha), 0, sin(alpha))` for lift along +z (check the axis convention of the CAD).
3. Set turbulence intensity and viscosity ratio.
4. Place the boundary at least 20-50 chord lengths away for lifting flows (the characteristic condition reduces but does not remove the influence).

## Practice
- To sweep angle of attack rotate the flow direction vector, and define drag and lift directions accordingly in the report definitions.
- For a half-model with symmetry plane, set symmetry on the cut.

## Gotchas
- At low Mach (below about 0.2) the compressible far-field condition is poorly conditioned: use velocity inlet and pressure outlet with the pressure-based solver.
- Mach number far-field with near-sonic Mach and a close boundary can reflect shocks.

## Verify
- [ ] Reported freestream Mach, pressure, and temperature on the far-field face match inputs.
