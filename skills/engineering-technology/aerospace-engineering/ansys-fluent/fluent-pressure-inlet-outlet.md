---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-pressure-inlet-outlet
name: fluent-pressure-inlet-outlet
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-boundary-conditions, pressure-outlet, pressure-inlet, stagnation-pressure, backflow, nacelle-inlet]
level: practitioner
status: draft
description: "Set pressure inlet and pressure outlet boundaries in Fluent for internal flows and nacelles: stagnation values, supersonic initial pressure, and backflow settings."
sources:
  - "Ansys Fluent user guide (pressure inlet and pressure outlet boundary conditions)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: pressure inlet and outlet

**Goal:** flow through nacelles, ducts and test sections with specified pressures.

## Pressure inlet
- Specify **Gauge Total Pressure** and **Total Temperature**; for compressible flow also **Supersonic/Initial Gauge Pressure** (the static pressure used if the inlet flow is supersonic and for initialisation).
- Direction: normal to boundary or components. Turbulence: intensity and viscosity ratio.

## Pressure outlet
- Specify **Gauge Pressure** (static); for engine intake simulations apply a mass-flow-outlet or a pressure outlet tuned to hit the target mass flow.
- Backflow: set the backflow total temperature and turbulence quantities (backflow intensity and viscosity ratio); poor backflow settings can destabilise or pollute the solution.
- Radial equilibrium pressure distribution for swirling flows.

## Practice
1. Compute total pressure and temperature from freestream Mach and static values for ram conditions in the nacelle problem.
2. For fan or engine face, use pressure outlet iterated to match the corrected mass flow, or mass-flow outlet.
3. Monitor mass-flow imbalance between inlet and outlet.

## Gotchas
- Gauge vs absolute again: check the operating pressure.
- A pressure outlet in a region with strong recirculation produces backflow: extend the domain or use a different condition.

## Verify
- [ ] Mass imbalance is below the target (for example under 0.1% of inflow).
