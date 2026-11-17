---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.manure-storage-sizing
name: manure-storage-sizing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, manure-storage-sizing, manure-storage, slurry-store, storage-days, freeboard, asabe-d384, nrcs-313, manure-management]
level: advanced
status: gated
description: "Size a manure storage: daily production, added water and bedding, rainfall and evaporation, required storage days, sludge and freeboard, and the design standards to check."
sources:
  - "USDA NRCS Conservation Practice Standards, code 313 Waste Storage Facility (state versions via https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Manure storage sizing

**Goal:** enough storage volume that manure can be applied at the right time and place, not forced by a full tank.

## Inputs
- Manure production: from the animal numbers and type using standard production tables (ASABE D384.2 Manure Production and Characteristics (gated: unconfirmed, source is paywalled or blocked), or the national equivalent) or from measured farm data. Use the current edition.
- Added materials: bedding, milking-parlour wash water, process water, feed waste and any other material that goes in the store.
- Rainfall minus evaporation on an open store surface (and catchment run-off from yards) over the storage period; for an open store a design storm is added on top (NRCS Conservation Practice Standard 313, Waste Storage Facility, state versions count the 25-year 24-hour precipitation and runoff as storage volume; confirm the current state standard and local rules).
- Storage period: set by the application window rules (closed periods, crop needs, ground conditions). Required periods vary by region; follow the regulation.

## Calculation
Volume = (daily manure + daily added water) x days + net precipitation volume + design storm + sludge or solids allowance + freeboard (set by the governing standard; for example the Texas NRCS 313 version, 2019, uses 6 in for vertical-walled tanks and 12 in (0.3 m) for other facilities exposed to precipitation and sizes the 25-year 24-hour runoff into the design, while the Alabama 2018 version requires 12 in of emergency depth beyond the 25-year 24-hour storm; confirmed by search of eFOTG, state versions differ).
Dimensions from the geometry: for earthen or lined basins, side slopes limited by soil and safety; for tanks, structural design is by a qualified engineer and the tank must resist hydrostatic and soil pressure.

## Other design points
- Location and setbacks from wells, streams, property boundaries and housing.
- Liner or tank watertightness and groundwater protection; leak detection where required.
- Agitation and pump-out points; safety around gas (hydrogen sulphide, methane, ammonia, carbon dioxide) in covered tanks and pits (confined space rules).
- Cover options for odour and ammonia reduction.

## Verify
- [ ] Production source, edition and the storage-days rule are recorded.
- [ ] Capacity cross-checked against a regulator or agency worksheet.
- Local storage period and design storm are confirmed against the governing regulation.
