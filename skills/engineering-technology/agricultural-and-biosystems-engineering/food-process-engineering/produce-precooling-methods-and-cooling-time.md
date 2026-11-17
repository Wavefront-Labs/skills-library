---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.produce-precooling-methods-and-cooling-time
name: produce-precooling-methods-and-cooling-time
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, precooling, food-refrigeration, cold-chain, forced-air-cooling, hydrocooling, vacuum-cooling, seven-eighths-cooling-time, postharvest]
level: practitioner
status: draft
description: "Choose and size precooling for fresh produce: forced-air, hydrocooling, vacuum, package icing, with half-cooling time, seven-eighths cooling time and airflow design."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Produce precooling methods and cooling time

**Goal:** remove field heat rapidly to extend shelf life.

## Methods
- **Forced-air (pressure) cooling**: fan draws cold air through vented containers on pallets; widely used for berries, grapes, many vegetables.
- **Hydrocooling**: showers or immersion in chilled water; fast; suited to produce tolerant of wetting (sweet corn, cherries, stone fruit) with sanitiser in the water.
- **Vacuum cooling**: evaporative cooling under vacuum, fast for leafy vegetables; loses about 1 percent of weight per 6 C of cooling.
- **Package icing/top ice**: broccoli and similar.
- **Room cooling**: slow; use only for less perishable or in combination.

## Cooling time
Cooling follows approximately `(T - T_med) / (T_i - T_med) = exp(-t ln2 / t_half)`. The **half-cooling time** is the time to reduce the temperature difference to half; the **seven-eighths cooling time** (three half-cooling times) is the usual practical target. Measure with a thermocouple at the product centre.

## Design (forced air)
1. Air flow per pallet commonly about 0.001-0.002 m3/s per kg of product in many guidelines (check postharvest handbooks); tight pallets with proper vent area (about 5 percent or more) and baffling are essential.
2. Static pressure and fan sizing from the container vents and pallet resistance.
3. High humidity (more than 90 percent RH) to limit moisture loss.

## Gotchas
- Chilling injury for sensitive crops: do not cool below the safe temperature.
- Water quality for hydrocooling (chlorine level, pH) is a food-safety control.

## Verify
- [ ] Product core hits target within the designed seven-eighths time.
