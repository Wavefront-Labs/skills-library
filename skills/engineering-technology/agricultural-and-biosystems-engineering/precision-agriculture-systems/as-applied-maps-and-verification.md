---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.as-applied-maps-and-verification
name: as-applied-maps-and-verification
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, as-applied-maps, variable-rate, prescription-maps, application-records, rate-error, data-logging, nutrient-management-records]
level: practitioner
status: draft
description: "Use as-applied data to verify variable-rate and uniform applications: logging settings, comparing to target, quantifying error, and keeping records for compliance and analysis."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# As-applied maps and verification

**Goal:** proof that the right product and rate went where intended.

## Logging
1. Enable logging of target rate, applied rate, product, speed, boom or section state and position at 1 Hz or faster; log the operator, implement and field names.
2. Calibrate the sensors regularly (flow meters, speed) so that the logs are meaningful (see sprayer and spreader calibration skills).
3. Export logs in a standard format (shapefile, ISO-XML, CSV) and store with the field and operation.

## Verify and analyse
- Compare applied versus target: calculate the mean error and the percentage of area within tolerance (for example +/- 10 percent).
- Check total product used (weigh tank or meter) against the mapped total over the area; reconcile any difference.
- Identify coverage gaps and overlaps; section control effectiveness.
- Check anomalies (rate at zero speed, or flows after the boom is shut).

## Records
Maintain records for regulation (nutrient management plans, pesticide application records) and sustainability programmes; the retention period depends on the regulator; do not rely on controller memory alone.

## Gotchas
- A log shows what the controller recorded, not necessarily what the nozzles or spreader delivered; confirm with physical calibration checks.
- Data ownership and sharing terms with software providers.

## Verify
- [ ] Total applied volume from the log matches product use within about 5 percent.
