---
id: natural-sciences.oceanography.satellite-oceanography.satellite-sst-and-ocean-colour-matchup-validation
name: satellite-sst-and-ocean-colour-matchup-validation
category: natural-sciences
field: oceanography
product: satellite-oceanography
tags: [satellite-oceanography, remote-sensing, sst, sea-surface-temperature, ghrsst, l2p, l3, l4, skin-temperature, foundation-temperature, ocean-colour, ocean-color, chlorophyll, modis, viirs, sentinel-3, olci, pace, altimetry, sla, quality-flags, matchup, validation, nasa-podaac, copernicus-marine, xarray, netcdf, cloud-masking]
level: practitioner
status: draft
description: "Use satellite SST, ocean-colour and altimetry products correctly: processing levels, quality flags, skin vs bulk temperature, and building in-situ matchups with time/space windows for validation."
sources: ["GHRSST Data Specification (GDS 2.x)", "IOCCG reports on ocean-colour validation", "NASA Ocean Biology Processing Group and PO.DAAC product documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Satellite SST and ocean-colour matchup validation

**Goal:** pick the right satellite product for a question, filter it properly, and know
how well it agrees with in-situ truth in *your* region — rather than trusting a global
accuracy number.

## 1. Know the processing levels
- **L1/L1B:** calibrated radiances. Rarely needed by users.
- **L2:** geophysical values per pixel along the swath (orbit geometry, gaps, full flags).
  Best for matchups.
- **L3:** gridded, possibly averaged in time (daily/8-day/monthly). Gaps remain.
- **L4:** gap-free analyses blending sensors and in-situ (e.g. OSTIA, MUR, OISST for SST;
  gridded altimetry SLA/ADT). Smooth, with effective resolution coarser than grid spacing.
Use L4 for maps and climatologies; L2/L3 for validation and fine features.

## 2. What is actually measured
- **SST:** infrared radiometers see the **skin** (~10–20 µm); microwave sees the sub-skin
  (~mm) through cloud but at ~25 km resolution and not near coasts. In-situ buoys measure
  at ~0.2–1 m depth. GHRSST products may provide **foundation** SST (free of diurnal
  warming). Daytime, low-wind conditions can create diurnal warming of 1 °C or more at the
  surface — compare like with like (night-time data, or wind-filtered).
- **Ocean colour:** water-leaving reflectance → chlorophyll by empirical band-ratio or
  semi-analytical algorithms. Works best in open ocean ("Case 1"); coastal waters with
  sediment and CDOM bias chlorophyll high. Chlorophyll is lognormally distributed —
  analyse log10(Chl).
- **Altimetry:** sea-level anomaly relative to a mean; degraded within ~10–20 km of coasts
  (newer SAR/SWOT products improve this).

## 3. Quality flags
- SST (GHRSST L2P): use `quality_level` ≥ 4 (or 5 for best) — *check the product's
  convention*; apply `sses_bias` if the product recommends it.
- Ocean colour L2: exclude pixels with flags such as cloud/ice, stray light, high glint,
  high sensor zenith, atmospheric-correction failure, low water-leaving radiance (NASA
  OBPG standard L2 flag set).
- Read the flag meanings in the file attributes; bit masks differ between products.

## 4. Building matchups
```python
import xarray as xr
ds = xr.open_dataset("L2_granule.nc")   # placeholder; geolocation in lat/lon arrays
# For each in-situ point: find nearest pixel, extract a 3x3 (or 5x5) box
```
- **Window:** time within ±1–3 h (ocean colour, often ±3 h) or ±30 min–few hours (SST,
  depending on diurnal concerns); space: the box centred on the in-situ location.
- **Homogeneity filter:** require enough valid pixels in the box (e.g. ≥50%) and low
  variability (coefficient of variation < ~0.15) — otherwise you're validating a front, not
  the sensor.
- Use the median of valid box pixels.
- In-situ data at matching depth (shallowest reliable, e.g. upper few metres) and with its
  own QC.

## 5. Statistics
- SST: bias (sat − in-situ), standard deviation, robust SD (median absolute deviation ×
  1.4826), number of matchups; split day/night and by wind speed.
- Chlorophyll: log-space bias and RMSE, or median ratio; slope of log-log regression.
- Report per region and season; global stats hide coastal failure.

## Gotchas
- Mixing skin and bulk SST without adjustment (~0.1–0.2 °C cool-skin difference at night).
- Trusting L4 fine-scale detail that's actually interpolation.
- Ignoring the time difference between a daily L3 composite and the in-situ time.
- Product reprocessing changes values — record version/R-number.

## Verify
- [ ] Product level, version and algorithm recorded.
- [ ] Flags applied as documented for that product.
- [ ] Matchup windows and homogeneity criteria stated.
- [ ] Bias, scatter and N reported, split by day/night or region.
- [ ] Chlorophyll analysed in log space.
