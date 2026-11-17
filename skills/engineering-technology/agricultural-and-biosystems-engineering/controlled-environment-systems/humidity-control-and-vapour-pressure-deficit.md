---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.humidity-control-and-vapour-pressure-deficit
name: humidity-control-and-vapour-pressure-deficit
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, vapor-pressure-deficit, vpd, humidity-control, relative-humidity, condensation, dehumidification, greenhouse-humidity, climate-control]
level: practitioner
status: gated
description: "Control greenhouse humidity with VPD: saturation vapour pressure, VPD calculation, target ranges, condensation and disease risk, and ways to dehumidify or humidify."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56, Chapter 3 (https://www.fao.org/4/x0490e/x0490e07.htm)"
  - "ASHRAE Handbook (Fundamentals) (https://www.ashrae.org)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Humidity control and vapour pressure deficit

**Goal:** an air state that keeps the crop transpiring and growing, without condensation or disease.

## VPD
- Saturation vapour pressure (kPa) at air temperature T (C): es = 0.6108 x exp(17.27 x T / (T + 237.3)). Actual vapour pressure ea = es x RH / 100.
- VPD = es - ea (kPa); leaf VPD uses leaf temperature in es.
- Target ranges depend on the crop and growth stage and are set by the grower and crop advisers (commonly quoted greenhouse ranges of roughly 0.5-1.2 kPa are practice values (gated: unconfirmed, source is paywalled or blocked)); VPD below about 0.3-0.4 kPa (gated: unconfirmed, source is paywalled or blocked) means low transpiration and risk of calcium deficiency and fungal disease; very high VPD stresses the crop.
- VPD ties temperature and humidity: at a given RH, a warmer greenhouse has a higher VPD.

## Dehumidify
- Ventilate and heat: open the vents slightly while the pipe heating runs (humidity venting); energy costly.
- Mechanical dehumidifiers and cooled coils (grow rooms, closed systems), or heat recovery ventilators; hygroscopic membranes in some designs.
- Air circulation fans to reduce humid pockets near the crop and cold surfaces.
- Avoid wet floors and over-watering at the end of the day.

## Humidify
- High-pressure fog, low-pressure misting, wet pad (`fan-and-pad-evaporative-cooling-design`), and mist or fog in propagation. Control with VPD, not RH alone.

## Condensation risk
Dew point of the air above the surface temperature of the leaf or cover causes condensation; Botrytis and other leaf diseases need free water for hours. Monitor dew point margin as well as RH.

## Verify
- [ ] Sensor RH and temperature checked (`aspirated-sensor-placement-and-calibration`).
- [ ] VPD logged and linked to leaf wetness observations.
- Equation matches FAO-56 Eq. 11 (fetched); FAO-56 gives the same form in Example 3 (e0 = 2.30 kPa at 19.75 C); check: es(20 C) = 2.338 kPa, VPD at 25 C and 70 percent RH = 0.95 kPa (computed).
