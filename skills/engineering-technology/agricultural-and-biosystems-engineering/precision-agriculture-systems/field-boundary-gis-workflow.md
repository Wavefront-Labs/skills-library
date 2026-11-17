---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.field-boundary-gis-workflow
name: field-boundary-gis-workflow
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, field-boundary-gis, field-boundaries, qgis, topology-check, farm-gis, headland-buffer, boundary-digitising, farm-data-management]
level: practitioner
status: draft
description: "Maintain field boundaries in GIS: sourcing from GNSS or imagery, topology rules, area in a projected CRS, headland buffers, naming and handing to machines."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GIS workflow for field boundaries

**Goal:** one clean, well-named boundary layer that all farm records and machines use.

## Sources
- GNSS-recorded perimeters driven by the machine (check the offset of the antenna from the implement edge, and the logging of turns), a surveyed perimeter, or imagery digitised on screen (orthophotos or satellite imagery; check the date).
- Public parcel or subsidy-claim boundaries may differ from the working boundary; keep both, linked by ID.

## Cleaning
1. Fix topology: no overlaps between adjacent fields, no gaps, no self-intersections, no slivers (use QGIS topology checker or the vector geometry tools).
2. Simplify only slightly (to remove GNSS jitter) so that the area does not change.
3. Compute area in an equal-area or local projected CRS and store it; compare with the agricultural records.
4. Attributes: unique field ID, farm, name, crop year, crop, tenure; keep the IDs stable year to year.

## Derived layers
Headland and buffer strips (negative buffers for sprayer or no-spray zones near water, positive buffers for the implement width); exclusion areas (wells, powerlines, wet spots); the working area net of these.

## Delivery
Export to the machine format (`shapefile-isoxml-and-geotiff-handling`); keep a master in a GeoPackage in version control or with dated backups; track changes by year and note when a boundary changes (drainage, levelling, field merging).

## Verify
- [ ] Topology errors count is zero.
- [ ] Boundary area agrees with machine-logged field area within a small percent.
- Unconfirmed: local parcel data rules.
