---
id: agriculture-environment.horticulture.greenhouse-production.greenhouse-climate-and-crop-steering
name: greenhouse-climate-and-crop-steering
category: agriculture-environment
field: horticulture
product: greenhouse-production
tags: [horticulture, greenhouse-production, protected-cropping, polytunnel, glasshouse, greenhouse-climate, climate-computer, vpd, vapour-pressure-deficit, humidity-deficit, 24-hour-temperature, day-night-temperature, generative, vegetative, crop-steering, dli, daily-light-integral, par, supplemental-lighting, co2-enrichment, ventilation, screens, tomatoes, cucumbers, peppers, high-wire, botrytis, condensation]
level: advanced
status: draft
description: "Run a greenhouse climate for fruiting crops: target temperature, VPD and light (DLI), use CO2 and screens, read the plant to steer it generative or vegetative, and keep condensation and botrytis away."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Greenhouse climate and crop steering

**Goal:** keep the plant balanced between leaf growth (vegetative) and fruit load
(generative) using the climate levers you control — temperature, humidity, light, CO2
and irrigation — and avoid the diseases that follow condensation.

> Draft. Setpoints are typical for high-wire tomato in temperate heated glass; cucumber and
> pepper differ. Climate computer brands (Priva, Hoogendoorn/Ridder, Argus) use different
> menus. Verify against your grower adviser's targets for your variety.

## 1. Core targets (tomato, indicative)
| Lever | Typical target |
|---|---|
| 24-h mean temperature | ~18–21 °C; raise with more light, lower in dull periods |
| Day / night | ~20–24 °C day, ~16–18 °C night |
| VPD (vapour pressure deficit) | ~0.5–1.0 kPa (HD ≈ 3–7 g/m³) |
| DLI (daily light integral) | ~20–30 mol/m²/day for high yield; < ~10–12 needs supplemental light |
| CO2 | ~800–1,000 ppm with vents closed; ~400–500 when venting heavily |
| Root zone | ~18–20 °C minimum |

**Key relationship: temperature must follow light.** High temperature with low light
burns sugars the plant didn't make → thin, weak heads and flower abortion.

## 2. Reading the plant
Check weekly on 5–10 marked plants:
- **Stem diameter** ~15 cm below the head (tomato ~10–12 mm typical): thick = vegetative,
  thin = generative/weak.
- **Distance from the top flowering truss to the head**: large = vegetative, small = generative.
- **Weekly growth length**, leaf colour and curl, truss set and fruit count.
- **Fruit load** versus leaf area: heavy load pulls the plant generative.

## 3. Steering levers
**To steer generative** (more fruit, less leaf):
- Larger day/night temperature difference (DIF), warmer 24-h mean, a **pre-night drop**
  (cool quickly at end of day).
- Higher VPD (drier air), longer dry-back between irrigations / higher EC in the slab.
- Remove leaves, keep more fruit per truss.
**To steer vegetative** (more leaf, stronger head):
- Smaller DIF, lower 24-h temperature in low light, lower VPD (more humid).
- Lower EC, more irrigation, earlier first watering of the day.
- Prune trusses (fewer fruit), keep more leaves.
Make **one** change at a time and watch for 1–2 weeks.

## 4. Humidity and condensation
- Humid, still air on cool surfaces (fruit at dawn, roof, leaves) = condensation = *Botrytis*,
  leaf mould.
- Prevent: start heating ~1–2 hours **before sunrise** so fruit warms gradually; use a
  **minimum pipe** temperature (e.g. ~35–45 °C) to keep air moving; open a vent slightly
  with heat on to dump moisture ("vent and heat") when humidity deficit falls below ~2–3 g/m³.
- Energy screens: open gradually at dawn (gap opening) to avoid dumping cold air on the crop.

## 5. Light and CO2
- Calculate DLI from a PAR sensor (µmol/m²/s × seconds / 1,000,000). Track it daily and set
  temperature by light sum (many computers do "light-dependent temperature").
- Supplemental LED/HPS: on to make up DLI in winter; check plant temperature (HPS heats leaves).
- CO2 dosing pays only when vents are mostly shut; don't chase high ppm with open vents.

## 6. Polytunnels (unheated)
Fewer levers: ventilate early in the morning to avoid heat spikes (> ~30 °C hurts fruit set);
damp down paths for humidity in heat; close early afternoon in cold months to store heat;
water in the morning to keep nights drier.

## Gotchas
- Chasing one number (e.g. VPD) while ignoring light gives a weak plant.
- Big setpoint jumps shock the crop — ramp over 1–2 hours.
- Sensor drift: calibrate the dry/wet-bulb or RH sensors and keep the measuring box aspirated and shaded.

## Verify
- [ ] 24-h temperature correlates with daily light sum in your records.
- [ ] VPD/HD stays in band; no dawn condensation on fruit.
- [ ] Weekly plant measurements logged on marked plants.
- [ ] Steering changes made one at a time, with result noted.
- [ ] Sensors calibrated this season; CO2 only dosed with vents nearly closed.
