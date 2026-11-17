---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-ideal-gas-energy-equation
name: fluent-ideal-gas-energy-equation
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-models, ideal-gas-energy, energy-equation, compressible-flow, operating-pressure, gauge-pressure]
level: practitioner
status: draft
description: "Switch on the energy equation with ideal-gas density in Fluent for compressible aerodynamics, and set operating pressure to zero or atmospheric consistently."
sources:
  - "Ansys Fluent user guide (energy equation, density, operating conditions)"
  - "Fluent solver theory guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: energy equation and ideal gas

**Goal:** a compressible setup that is self-consistent.

## Steps
1. **Models > Energy: On.**
2. **Materials > air:** Density = ideal-gas; Cp constant or piecewise polynomial; Viscosity = Sutherland (see that skill); thermal conductivity constant or kinetic theory.
3. **Cell Zone Conditions > Operating Conditions:** choose the operating pressure. With ideal gas density, a common approach is to set the operating pressure to 0 Pa so that all pressures are absolute and boundary pressures are given as the absolute values; the alternative is to use 101325 Pa with gauge boundary values. Pick one and stay consistent.
4. Boundary pressures: gauge = absolute minus operating pressure.
5. Solver: pressure-based coupled or density-based solver for high Mach.

## Gotchas
- A mix of gauge and absolute values gives a wrong Mach number: check using a report of Mach and static pressure at the farfield.
- Precision loss with high operating pressure and low differences: use double precision (`3ddp`).
- Reference values (see that skill) are used for coefficients only; they do not set the flow.

## Verify
- [ ] Report Mach, static pressure, temperature at the inlet or farfield match the requested freestream.
