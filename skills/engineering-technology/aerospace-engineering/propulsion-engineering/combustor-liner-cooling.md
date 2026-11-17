---
id: engineering-technology.aerospace-engineering.propulsion-engineering.combustor-liner-cooling
name: combustor-liner-cooling
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [liner-cooling, film-cooling, effusion-cooling, combustor-liner, combustors-emissions]
level: practitioner
status: draft
description: "Choose and size combustor liner cooling (film, effusion, impingement, thermal barrier coating) and see its effect on emissions, pattern factor and liner life."
sources:
  - "Lefebvre and Ballal, Gas Turbine Combustion"
  - "Mattingly, Elements of Propulsion"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Liner cooling

**Goal:** keep liner wall temperature within life limits using as little air as possible.

## Methods
- **Film cooling** (louvres, machined rings, splash cooling): a slot injects a protective air layer along the wall; effectiveness decays with distance so slots are repeated.
- **Effusion (transpiration-like) cooling**: many small angled holes in the liner give convective cooling inside the holes plus film; efficient with lower air use.
- **Impingement plus film** in double-wall liners.
- **Thermal barrier coating** lowers metal temperature and extends life.

## Sizing steps
1. Estimate the gas-side heat flux from flame radiation and convection at the worst axial station (primary zone).
2. Choose a wall temperature limit from the liner alloy and desired life.
3. Size the film mass flow or hole array to meet it using published film-effectiveness correlations (Lefebvre).
4. Account for the cooling air in the airflow split: air used for cooling is unavailable for primary-zone combustion and dilution.

## Emissions link
- Cooling air entering near the flame can quench CO and unburnt-hydrocarbon oxidation, raising CO and UHC at low power.
- Modern low-NOx combustors want most air in the premixer, so they use efficient effusion cooling to free air.

## Gotchas
- Hole blockage and coating spallation produce local hot streaks.
- Cooling-air momentum affects the flow pattern and can change pattern factor.
- Radiation increases with pressure; the same liner runs hotter at take-off than in cruise.

## Verify
- [ ] Predicted wall temperature at take-off is below the alloy limit at the primary-zone hot spot.
