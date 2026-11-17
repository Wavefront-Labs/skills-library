---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.in-field-soil-sensor-network-design
name: in-field-soil-sensor-network-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, soil-sensor-network, soil-moisture-network, sensor-placement, representative-site, sensor-installation, site-calibration, soil-probe-network]
level: advanced
status: draft
description: "Design an in-field soil sensor network: choosing representative sites, depths, replicates, installation contact, site calibration, communications and upkeep."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# In-field soil sensor network design

**Goal:** a sensor network whose readings represent the field and support decisions, and that survives the season.

## Site selection
- Divide the field into zones using soil maps, EC maps, elevation and yield history (`apparent-electrical-conductivity-mapping`); place a station in each major zone, in an area typical of that zone (not at the field edge, wet spot or compacted headlands).
- Within a station, use replicate sensors (at least two or three probes) because one probe can give a poor reading due to poor soil contact or a rock; include multiple depths (for example 15, 30, 60 and 90 cm) to see the active root zone, drainage below it, and where the crop takes water.

## Installation
- Install with close contact: prepare a hole with a tool matching the probe diameter, use slurry for contact when needed, avoid air gaps and preferential flow paths along the cable. Backfill and compact to the original bulk density.
- Place in the crop row or with a known relation to the drip or sprinkler wetted pattern; for drip, install sensors in the wetted bulb with the emitter distance recorded.
- Mark locations with GNSS coordinates and flags; protect from machinery.

## Calibration and interpretation
- Factory calibration of capacitance and similar sensors is generic; check with site-specific soil samples (gravimetric water content) and adjust. Salinity and temperature affect some types; read the manual.
- Establish field capacity and refill thresholds from the sensor record after a thorough wetting and drainage (`soil-moisture-sensor-selection-and-installation`).

## Communications and power
Wired data loggers, radio, or LoRaWAN telemetry (`lorawan-coverage-planning-for-farms`); battery or solar power (`solar-and-battery-power-budgeting-for-field-nodes`); plan for tillage and harvest removal and re-installation.

## Verify
- [ ] Replicate probes agree within a stated tolerance after a wetting event.
- [ ] Soil sample cross-check at installation and mid-season.
- Unconfirmed: sensor spacing and depths for your crop; adapt.
