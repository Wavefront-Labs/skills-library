---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.weather-station-siting-and-maintenance
name: weather-station-siting-and-maintenance
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, weather-station-siting, agricultural-weather-station, anemometer-height, rain-gauge-siting, pyranometer, wmo-siting, sensor-maintenance, farm-iot]
level: practitioner
status: draft
description: "Site and maintain an on-farm weather station: exposure rules for temperature, wind, rain and radiation, reference surface, ET inputs, cleaning and annual checks."
sources:
  - "FAO Irrigation and Drainage Paper 56, chapter 3 (https://www.fao.org/4/x0490e/x0490e07.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# On-farm weather station siting and maintenance

**Goal:** a station whose data is representative and good enough for irrigation scheduling, disease models and spray decisions.

## Siting
- Reference surface: short, well-watered grass with a fetch of upwind grass of tens of metres, representative of the local conditions; irrigated and green for ET reference stations (the FAO-56 reference crop). Avoid sites near buildings, paved areas, tree lines, ponds, or air-conditioner exhaust.
- Air temperature and humidity: in a ventilated radiation shield at about 1.5-2 m above ground (FAO-56 uses 2 m, in shelters placed per WMO standards); keep the shield clean and white.
- Wind: the international standard height is 10 m over open terrain; agricultural stations often use 2 m, and wind speed at other heights is converted to 2 m for ET calculations with u2 = uz x 4.87 / ln(67.8 z - 5.42) (FAO-56 Eq. 47; for z = 10 m the factor is 0.75, computed). Place the sensor away from obstacles by about ten times the obstacle height.
- Rain gauge: level, unobstructed, away from buildings and trees by at least two to four times the height of the obstruction; keep the funnel clean; protect from splash.
- Solar radiation: a pyranometer on a level mount with a full-sky view and no shading; clean the dome.
- Soil temperature and moisture sensors in representative soil as needed; leaf wetness sensors in the canopy if used for disease models.

## Maintenance
- Weekly or monthly: visual check, clean the radiation shield and pyranometer, clear the rain gauge funnel; check the battery and solar panel.
- Annual: calibrate or replace the humidity sensor; check the temperature against a reference thermometer; test the rain gauge by pouring a known volume; check the anemometer bearings and the pyranometer against a reference (recalibrate every one or two years); replace wetness sensor coatings.
- Quality control: range checks, rate-of-change checks, comparison with nearby stations; flag suspicious values before they enter ET calculations (`et0-penman-monteith-inputs-and-checks`).

## Verify
- [ ] Siting photos and distances from obstacles stored with the metadata.
- [ ] Calibration and maintenance log kept.
- Unconfirmed: local network standards; check the national weather service guidelines.
