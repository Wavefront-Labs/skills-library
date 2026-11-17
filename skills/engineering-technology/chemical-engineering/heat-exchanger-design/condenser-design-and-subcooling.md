---
id: engineering-technology.chemical-engineering.heat-exchanger-design.condenser-design-and-subcooling
name: condenser-design-and-subcooling
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-condensers-reboilers, condenser-design-and-subcooling, condenser-design, film-condensation, desuperheating, subcooling, noncondensables, nusselt-condensation, shell-side-condenser, vent-condenser]
level: practitioner
status: draft
description: "Design process condensers: zones (desuperheat, condense, subcool), Nusselt film condensation estimates, vertical versus horizontal arrangement, noncondensables and vent design."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Condenser design and subcooling

**Goal:** a condenser sized with realistic heat transfer in each zone.

## Zones
1. **Desuperheating** (vapour cools to the dew point): gas-phase film coefficient, low.
2. **Condensing** (dew to bubble point for mixtures): condensation coefficient, strongly dependent on mixture and vapour shear; for multi-component vapours the condensing curve is not a straight line; use stepwise (zone) calculation with a simulator.
3. **Subcooling** (liquid sensible cooling, typically a few K, about 3 to 5 K for pump NPSH or storage).

## Film condensation estimates (Nusselt)
- Vertical surface: h = 0.943 [k^3 rho^2 g lambda/(mu L DT)]^(1/4) (laminar film), with liquid properties at film temperature and DT = T_sat - T_wall.
- Horizontal tube: h = 0.725 [k^3 rho^2 g lambda/(mu d DT)]^(1/4); for N tubes in a vertical row divide by N^(1/6).
Typical process condensing coefficients are 1,000 to 3,000 W/m2/K for organics and above 5,000 for steam.

## Design choices
- **Shell-side condensation** (horizontal exchanger, vapour on the shell side, cooling water in tubes) is the usual column overhead condenser; cooling water in tubes is easier to clean.
- **Vertical tube-side condensation** for downflow with low pressure drop and total condensation.
- Noncondensables blanket the surface and reduce h dramatically; vent from the end of the condensing path to a vent condenser.
- Provide a baffle cut oriented for drainage (horizontal cuts for condensers), and vapour inlet impingement protection.

## Gotchas
- Subcooling in the same shell can cause drainage and control problems; separate subcooler if needed.
- Pressure drop on the vapour side lowers the saturation temperature and the temperature driving force.

## Verify
- [ ] Heat balance per zone; sum of zone areas used for the total.
- [ ] Vent capacity sized for noncondensable flow with margin.
