---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.canopy-airflow-design
name: canopy-airflow-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, canopy-airflow, horizontal-airflow, air-velocity, leaf-boundary-layer, tipburn, circulation-fans, anemometer-survey, vertical-farming]
level: practitioner
status: draft
description: "Design and verify airflow across the plant canopy: target velocity, horizontal airflow fans, ducted delivery, dead zones, leaf boundary layer and measurement."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Canopy airflow design

**Goal:** uniform air movement over every leaf, so transpiration, temperature, humidity and CO2 are even and disease and tipburn are limited.

## Why
Still air around leaves creates a thick boundary layer: leaf temperature, humidity and CO2 differ from the room average, slowing photosynthesis and transpiration and favouring fungal growth and calcium-related disorders such as tipburn in lettuce. Moving air thins the boundary layer.

## Targets
- Velocity at the canopy: commonly cited at around 0.3-1 m/s in growing rooms (for example about 0.5 m/s as a working target for leafy greens); too high causes desiccation and leaf damage. Use the crop and breeder guidance.
- Uniformity: aim for small variation across the canopy; the lowest zones control crop variability.

## Layouts
- Horizontal airflow (HAF) fans in a loop pattern in greenhouses, or fans at the end of each tier in multi-tier racks with air passing across the tiers.
- Ducted or plenum delivery with distribution slots between tiers, sized for equal flow along the length; return paths kept free.
- Through-canopy air with perforated shelves, in some vertical systems.
- CFD modelling helps for complex racks; always verify in the built room.

## Fan selection
Fan flow and pressure from the duct and rack resistance; fans in ventilation clusters (`ventilation-fan-selection-and-static-pressure`) with variable speed to adjust seasonally; low-noise and energy-efficient EC motors.

## Verify
- [ ] Anemometer grid across the canopy (many points, three heights) with a contour map.
- [ ] Smoke or fog visualisation to find dead zones.
- Unconfirmed: target velocities per crop.
