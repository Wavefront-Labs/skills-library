---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.packaging-barrier-permeability-calculation
name: packaging-barrier-permeability-calculation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, barrier-permeability, oxygen-transmission-rate, water-vapour-transmission-rate, packaging-film, laminate-barrier, moisture-gain-shelf-life]
level: advanced
status: verified
description: "Calculate gas and moisture barrier of packaging: permeability, OTR and WVTR units, laminate layers, test conditions and moisture-gain shelf life."
sources:
  - "ISO standards catalogue (https://www.iso.org)"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Packaging barrier permeability calculation

**Goal:** choose a film and pack size so oxygen or moisture exchange stays within the shelf-life limit.

## Definitions
- Permeability P = (flux x thickness) / (partial pressure difference); transmission rates (OTR in cm3 per m2 per day, WVTR in g per m2 per day) are for a specific film thickness and test condition. Quote the temperature and humidity, because values change strongly.
- Laminate in series: total resistance = sum of (thickness/P) per layer; the best barrier layer (foil, metallised film, EVOH, PVDC) dominates, but defects (pinholes, flex cracks) matter more than the layer's nominal value.
- EVOH barrier worsens with humidity, so in humid or retort uses it must be protected by polyolefin outer layers.
- Temperature: P follows Arrhenius with an activation energy; WVTR increases a lot at tropical temperature.

## Test methods
Standard tests (ASTM and ISO methods exist for oxygen transmission rate by coulometric sensor and for water vapour transmission rate by infrared or gravimetric cup; typical WVTR test conditions are around 38 C and 90 percent relative humidity, and OTR around 23 C and dry or 50 percent RH (gated: unconfirmed, source is paywalled or blocked); check the current edition for the conditions you need).

## Moisture-gain shelf life
For a dry product in a package with a moisture sorption isotherm of slope b: ln[(me - mi)/(me - mc)] = (k/x) x (A/Ws) x (p0/b) x t, where me is the equilibrium moisture at the outside humidity, mi initial, mc critical, k/x film permeability per thickness, A package area, Ws mass of dry solids, p0 the saturation vapour pressure at the temperature, and t time (the Labuza equation). Use measured isotherm data (`water-activity-and-sorption-isotherms`) and pack area per product mass.

## Verify
- [ ] Barrier values quoted with test conditions.
- [ ] Shelf life confirmed with real package storage at the hot-humid condition.
- Unconfirmed: material values; use supplier or test data.
