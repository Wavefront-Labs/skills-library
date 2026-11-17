---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.soil-moisture-sensor-selection-and-installation
name: soil-moisture-sensor-selection-and-installation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, soil-moisture-sensors, soil-water, irrigation-scheduling, tensiometer, capacitance-probe, tdr, granular-matrix, sensor-installation]
level: practitioner
status: verified
description: "Choose and install soil moisture sensors (tensiometer, capacitance, TDR, granular matrix): depth and location, calibration, reading interpretation and failure modes."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Kansas State University L-796, Tensiometers for Scheduling Irrigation (https://www.irrigationtoolbox.com/ReferenceDocuments/Extension/Kansas/l796.pdf)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Soil moisture sensor selection and installation

**Goal:** moisture data that actually represent the root zone and can trigger irrigation.

## Sensor types
- **Tensiometer**: measures matric potential directly, useful 0 to about -80 kPa (Kansas State L-796: 80 centibar is the functional upper limit; the water column breaks between 80 and 85); needs filling and maintenance; good for sandy soils and drip.
- **Granular matrix / gypsum blocks**: resistance-based potential sensors; low cost, slow response, calibration drift.
- **Capacitance (FDR) and TDR probes**: volumetric water content; need soil-specific calibration; salinity and air gaps affect readings.
- **Neutron probe**: accurate but involves a radioactive source (subject to radioactive-materials regulation; check the regulator before use).

## Installation
1. Place sensors in representative soils and plants (not in the lowest or highest spot), within the wetted zone for drip and near the emitter-plant mid-region.
2. Use at least two depths: one in the main root zone and one below to detect over-irrigation.
3. Ensure intimate soil contact: use a slurry or the manufacturer's installation tool; avoid air gaps and preferential water paths down the access tube.
4. Install several replicates per management zone.
5. Log with telemetry or a data logger; set alerts for thresholds.

## Interpretation
Use field capacity and refill point readings from your own field: watch the trace after a heavy irrigation (field capacity) and at a stressed state (refill point). Trends matter more than absolute values.

## Gotchas
- A sensor in the wrong place tells the wrong story.
- Soil cracking and salinity corrupt readings; recalibrate for each soil.

## Verify
- [ ] Gravimetric samples at the same depth agree with the sensor within the sensor's accuracy.
