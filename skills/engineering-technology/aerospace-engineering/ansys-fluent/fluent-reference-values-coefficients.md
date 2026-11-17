---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-reference-values-coefficients
name: fluent-reference-values-coefficients
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-boundary-conditions, reference-values, force-coefficients, reference-area, moment-centre, half-model]
level: practitioner
status: draft
description: "Set Fluent reference values (area, length, velocity, density) so lift, drag and moment coefficients match the definition used by the test or design team."
sources:
  - "Ansys Fluent user guide (reference values and force reports)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: reference values for coefficients

**Goal:** coefficients identical to the definition the project uses.

## Steps
1. **Setup > Reference Values:** Area (planform area for aircraft; frontal area for bluff bodies), Length (mean aerodynamic chord for moments), Velocity (freestream), Density (freestream), Temperature, Pressure (for Cp), Ratio of specific heats.
2. Use "Compute from" the far-field boundary to fill velocity, density and temperature.
3. **Half models:** area is the half-model area when using symmetry (Fluent reports forces on the modelled half); either double the forces or define reference area as the half planform consistently.
4. Moment centre: set the moment reference point (x, y, z) in the moment report definition.
5. Create drag and lift report definitions with force vectors derived from alpha: drag direction `(cos(alpha), 0, sin(alpha))`, lift direction `(-sin(alpha), 0, cos(alpha))` (check axes).

## Gotchas
- Coefficients reported with wrong reference area are the most common mistake; compare `CL` against a quick hand estimate.
- Dynamic pressure uses reference density and velocity: with different units or altitude states these must match the freestream.

## Verify
- [ ] A rigid check, `CL` slope at low alpha approaches `2 pi AR/(2+AR)`-type estimates for a simple wing, and the half-model results equal the full-model results.
