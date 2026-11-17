---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.aspirated-sensor-placement-and-calibration
name: aspirated-sensor-placement-and-calibration
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, aspirated-sensor, climate-sensor, radiation-shield, rh-calibration, saturated-salt-calibration, ndir-co2-sensor, sensor-placement, climate-control]
level: practitioner
status: draft
description: "Place and calibrate greenhouse climate sensors: aspirated radiation-shielded temperature and RH box, representative location, salt calibration for RH, CO2 span checks."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Aspirated sensor placement and calibration

**Goal:** climate measurements that represent the crop and that you can trust for control decisions.

## Placement
- Temperature and humidity sensors in an aspirated, radiation-shielded box (a small fan draws air over the sensor at a few metres per second), because an unshielded sensor reads warm in sun and humidity readings lag.
- Hang at crop height or just above the canopy, away from heating pipes, doors, vents, direct sunlight and wet surfaces; representative of the zone. Use at least one per climate zone and more in large or complex compartments; compare multiple sensors to see the spatial spread.
- CO2 sensor inside the crop zone; light sensors outside (global radiation) and, if needed, within the crop; outdoor weather station for wind, rain, temperature and radiation.
- Keep cables away from heat, label them and protect connectors from moisture.

## Calibration and checks
- Temperature: compare with a reference thermometer in a stirred ice bath (0 C) and at another point; offsets applied in the controller.
- Relative humidity: capacitive sensors drift; check with saturated salt solutions in a sealed container, where at about 25 C a saturated sodium chloride solution gives about 75 percent RH, magnesium chloride about 33 percent and lithium chloride about 11 percent (allow hours to equilibrate, keep the temperature stable and confirm values for your temperature in the standard or manual); replace sensors that drift beyond the specified limits.
- CO2 (NDIR): check with zero (nitrogen) and span gas of known concentration at least every season; follow the manufacturer on automatic baseline correction, because it can drift where CO2 is held high all day.
- Clean the aspirator fan and filters; check the fan runs.

## Verify
- [ ] Calibration log with date, reference and correction applied.
- [ ] Two sensors in the same compartment agree within the stated tolerance.
- Unconfirmed: salt RH values at your temperature; confirm with standards.
