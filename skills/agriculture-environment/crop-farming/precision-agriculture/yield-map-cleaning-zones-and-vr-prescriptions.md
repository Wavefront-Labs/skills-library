---
id: agriculture-environment.crop-farming.precision-agriculture.yield-map-cleaning-zones-and-vr-prescriptions
name: yield-map-cleaning-zones-and-vr-prescriptions
category: agriculture-environment
field: crop-farming
product: precision-agriculture
tags: [precision-agriculture, precision-farming, yield-map, yield-monitor, yield-calibration, yield-data-cleaning, flow-delay, management-zones, zoning, ndvi, satellite-imagery, sentinel-2, em38, soil-ec, elevation, k-means, variable-rate, vrt, prescription-map, shapefile, isoxml, iso-11783, strip-trial, on-farm-trial, qgis, farm-management-software, nitrogen, lime, seeding-rate]
level: practitioner
status: gated
description: "Turn yield and sensor data into variable-rate decisions: calibrate and clean yield maps, build stable management zones from several layers, write a prescription, and prove it with strip trials."
sources: ["https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Yield map cleaning, management zones and VR prescriptions

**Goal:** vary inputs only where the field really differs in a way that changes the
best rate — and check it paid. Precision ag fails mostly on dirty data and on zones
that describe noise. (Guidance, RTK and ISOBUS setup are in
`engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.gnss-guidance-and-variable-rate-setup`.)

## 1. Get yield data right at the source
- **Calibrate the yield monitor** per crop at harvest start: harvest several loads
  across different flow rates, weigh each on a weighbridge/cart scale, enter the actual
  weights. Recalibrate when crop or conditions change markedly.
- Calibrate the **moisture sensor** against a reference meter.
- Set header width correctly and use **swath/section control** logging so partial
  widths are recorded.
- Log continuously; label every field and crop correctly in the display (a mislabelled
  field ruins the archive).

## 2. Clean yield maps
Raw yield data contain systematic errors. Clean with your farm software or a tool
such as Yield Editor-type filters / QGIS, in this order:
1. **Flow delay** (time between cutting and the sensor, often ~8–15 s (gated: unconfirmed, source is paywalled or blocked)): shift until
   yield transitions line up with the headland start/stop in both directions.
2. Remove **start-pass and end-pass** fill/drain points (ramp-up/down).
3. Remove points with **header up**, near-zero speed, or abrupt speed changes.
4. Remove **overlapped/narrow-width** passes or correct width.
5. Remove statistical outliers (e.g. beyond mean ± 3 SD (gated: unconfirmed, source is paywalled or blocked) within the field, or a
   min/max plausible yield).
6. Interpolate to a grid (e.g. 5–10 m cells (gated: unconfirmed, source is paywalled or blocked); kriging or inverse distance) and
   **normalise** (yield ÷ field mean) so years and crops can be compared.
Typically 10–30% of raw points get removed (gated: unconfirmed, source is paywalled or blocked); that's normal.

## 3. Build management zones
Use layers that are **stable over years** and relate to yield-limiting factors:
- Normalised yield maps from 3+ seasons (preferably different crops and seasons),
- Soil apparent electrical conductivity (EM38/Veris surveys) — texture, salinity,
  water holding,
- Elevation and derived wetness/slope,
- Multi-year satellite vegetation indices (e.g. NDVI from Sentinel-2) at a consistent
  growth stage,
- Soil sampling results.
Method: standardise layers, cluster (k-means or fuzzy k-means) into **2–4 zones** (gated: unconfirmed, source is paywalled or blocked),
smooth out slivers smaller than your spreader/sprayer can resolve (a zone narrower than
the boom is fiction). Ground-truth: dig, sample soil and talk to whoever has driven
that field for decades.
Rule: if zones don't hold their rank across most years, uniform rates are probably fine.

## 4. Write the prescription
- Decide what's limiting in each zone first: e.g. low zone = sandy, low water-holding →
  lower N target; high zone = good soil → higher N/seed. Lime and P/K are better
  candidates for zone-based VR than N in many systems because they're less weather-
  dependent; base them on **grid or zone soil tests**.
- Rate per zone from agronomy (yield target × uptake, soil test response curves).
- Export in the format your controller reads: **shapefile** (polygons with a rate
  attribute) or **ISO-XML (ISO 11783 TaskData)** (gated: unconfirmed, source is paywalled or blocked); check units (kg/ha vs product/ha) and
  the default rate outside zones and on headlands.
- Load into the terminal, check the map aligns with the field boundary on screen, and
  **test-run a section** before committing.

## 5. Prove it: strip trials
- Leave replicated **check strips** (uniform rate or alternative rates) across all
  zones, at least ~3 replicates (gated: unconfirmed, source is paywalled or blocked), as wide as the header (so yield data is clean).
- Compare yield in strips within each zone; calculate the margin, not just yield.
- Without this, you can't tell whether VR helped.

## Gotchas
- Mixing calibrated and uncalibrated years produces fake zones.
- Wet years and dry years can flip which zone yields best — use several seasons.
- File coordinate system mismatches shift prescriptions by metres or more; check on
  screen against imagery.
- Applicator response lag: the controller needs look-ahead set so rate changes happen
  at the zone boundary, not after it.

## Verify
- [ ] Yield monitor calibrated with weighed loads this season.
- [ ] Yield data cleaned (flow delay, start/end, outliers) before use.
- [ ] Zones built from multi-year layers and ground-truthed; no zones narrower than the implement.
- [ ] Prescription units and default rate checked on the terminal before application.
- [ ] Replicated check strips in place to measure the response.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; data-processing craft.
- Confirmed against: Sentinel-2 as an NDVI source is an ESA Copernicus mission.
- Not confirmed: the flow-delay range, share of points removed, cell size, zone count, outlier rule and ISO 11783 TaskData naming (ISO 11783 is paywalled).

Method: documentation only; no commands were run.
