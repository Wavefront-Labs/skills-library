---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.prescription-map-creation-and-file-formats
name: prescription-map-creation-and-file-formats
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, prescription-file-formats, variable-rate, prescription-maps, shapefile, iso-xml, rx-map, rate-attribute]
level: practitioner
status: draft
description: "Build a variable-rate prescription: zones to rates, product units, shapefile or ISO-XML format, projection and attributes, and a test load into the controller."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Prescription map creation and file formats

**Goal:** a file the controller reads and applies at the intended rates.

## Steps
1. **Rates by zone**: decide target rates from agronomic recommendations (soil tests, yield goals, crop model or a nutrient guideline) and set minimum and maximum limits, plus a default rate outside the zones.
2. **Polygons or grid**: create zones in GIS or farm software; a grid layer with cells equal to or larger than the controller's response distance is more robust than many small polygons.
3. **Attributes**: a numeric rate field in the units the controller expects (kg/ha, seeds per hectare, litres per hectare); product name and unit conversions are checked.
4. **Format**: shapefile (with .shp, .shx, .dbf, .prj) is widely supported; ISO 11783 TaskData (ISO-XML) is used by ISOBUS task controllers; some manufacturers use proprietary formats; use the converter provided by the manufacturer or farm software.
5. **Projection**: geographic WGS84 latitude and longitude is the usual requirement; confirm that the .prj is present.
6. **Test**: load the file in the display, view the map and values at several points; check that the rate unit and product mapping are right.

## Gotchas
- Zone boundaries drawn without regard for controller lag cause incorrect rates near edges.
- Mixed units (lb/ac in the file and kg/ha in controller) cause large errors.
- Overwritten or wrong field boundary yields a rate of zero outside.

## Verify
- [ ] On a stationary test or a short test run, the controller shows the right target rates at known points.
