---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-sutherland-viscosity-law
name: fluent-sutherland-viscosity-law
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-models, sutherland-viscosity, viscosity-law, air-properties, compressible-flow, temperature-dependent-viscosity]
level: practitioner
status: draft
description: "Set the Sutherland viscosity law for air in Fluent with the right coefficients, and know when constant viscosity or a polynomial is appropriate."
sources:
  - "Ansys Fluent user guide (viscosity: Sutherland law)"
  - "White, Viscous Fluid Flow (Sutherland law)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: Sutherland viscosity

**Goal:** temperature-dependent air viscosity for compressible flows where temperature varies.

## Law
`mu = mu0 (T/T0)^(3/2) (T0 + S)/(T + S)`. Fluent's three-coefficient form uses reference viscosity 1.716e-5 kg/(m s) at 273.11 K with S = 110.56 K for air; the two-coefficient form uses `mu = C1 T^(3/2)/(T + S)` with C1 = 1.458e-6 and S = 110.4 K. Check these values in the material database for your version.

## Steps
1. **Materials > air > Viscosity:** select `sutherland` (three-coefficient or two-coefficient), confirm the coefficients.
2. Energy equation on (temperature varies).
3. Use consistent viscosity in the Reynolds number: compute the reference Reynolds number from the freestream temperature.

## When to use
- Compressible flows with significant temperature changes (transonic and above, boundary layers with heating): use Sutherland.
- Low-speed incompressible runs: constant viscosity at the ambient temperature is fine.

## Gotchas
- Using sea-level viscosity for a cruise altitude shifts Reynolds number by several tens of percent: compute density and viscosity from the ISA at the altitude.
- The law is valid roughly 100-1900 K; beyond that use polynomial or kinetic theory.

## Verify
- [ ] Reported viscosity at the freestream temperature matches ISA value for the altitude.
