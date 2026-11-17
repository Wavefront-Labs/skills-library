---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.ground-truthing-and-sensor-calibration
name: ground-truthing-and-sensor-calibration
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, ground-truthing, remote-sensing-agriculture, crop-sensing, calibration, reference-strip, validation, spad]
level: practitioner
status: draft
description: "Calibrate sensor or imagery readings against ground data: sampling plan, biomass or tissue measurements, regression, reference strips and validation on independent points."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ground-truthing and sensor calibration

**Goal:** turn an index value (NDVI, NDRE, canopy reflectance) into an agronomic quantity such as biomass, nitrogen uptake or yield potential.

## Plan
1. **Stratify** the field by sensor values (low, medium, high) so the sample covers the range, rather than random locations only.
2. **Locate** sample sites with GPS and mark them so the sensor pixels or readings match the physical sampling area.
3. **Measure at the same time** as the sensor pass: biomass (cut and dry weigh a defined area), tissue nitrogen (lab), chlorophyll meter (SPAD) readings, plant counts, soil moisture, or yield at harvest.
4. Collect enough points (often 20-30 per field or season at minimum, more for regional models).

## Analysis
1. Regress ground variable against index; check R squared, residuals and range of validity.
2. **Validate** on points not used for calibration (for example from another field or year).
3. Account for growth stage: calibrations apply only to the stage tested.
4. **Reference strips (N-rich strips)**: apply non-limiting nitrogen in a strip and compare sensor readings with the surrounding field to derive a sufficiency index, which makes the recommendation relative and less dependent on absolute calibration.

## Use
Apply the calibrated model to produce maps for decisions such as variable-rate nitrogen, scouting priorities or zone delineation.

## Gotchas
- Soil background, row spacing and sun angle affect the readings.
- Extrapolating beyond the calibrated range or to other crops is unreliable.

## Verify
- [ ] Independent validation data show acceptable error for the decision threshold.
