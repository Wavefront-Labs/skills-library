---
id: natural-sciences.atmospheric-sciences.climate-modelling.working-with-cmip-and-reanalysis-data
name: working-with-cmip-and-reanalysis-data
category: natural-sciences
field: atmospheric-sciences
product: climate-modelling
tags: [climate-modelling, climatology, cmip6, cmip, esgf, ssp, ssp2-4.5, ssp5-8.5, historical-experiment, ensemble-members, variant-label, multi-model-ensemble, era5, reanalysis, copernicus-cds, netcdf, xarray, cdo, cf-conventions, regridding, xesmf, area-weighting, cos-latitude, anomalies, baseline-period, model-democracy, bias-correction, downscaling, calendar-noleap]
level: advanced
status: verified
description: "Analyse CMIP6 projections against ERA5 reanalysis: pick experiments and members, fix calendars and units, regrid, area-weight, take anomalies vs a baseline, show ensemble spread."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with CMIP and reanalysis data

**Goal:** climate-change numbers (e.g. "regional summer warming by 2050 under SSP2-4.5")
computed from CMIP6 model output and evaluated against observations/reanalysis in a way
that respects how the data are built and represents model uncertainty honestly.

## 1. Choose what to download
- **Experiments:** `historical` (to ~2014) for evaluation; `ssp126`, `ssp245`, `ssp370`,
  `ssp585` for scenarios (2015–2100). Join historical + SSP for continuous series.
- **Variables** use CMIP short names and tables: `tas` (near-surface air temperature, K)
  and `pr` (precipitation flux, kg m⁻² s⁻¹) in table `Amon` (monthly) or `day`.
- **Members:** variant labels like `r1i1p1f1` (realisation, initialisation, physics,
  forcing). Use the same member through historical and scenario. Multiple `r` members
  sample internal variability.
- Source: ESGF nodes, or cloud mirrors (e.g. Pangeo/Google Cloud CMIP6 Zarr) — record
  the dataset version and download date.
- **ERA5** reanalysis from the Copernicus Climate Data Store (hourly/monthly, ~0.25°).
  Reanalysis is a model-observation blend: excellent for temperature and circulation,
  less reliable for precipitation and in data-sparse regions/eras.

## 2. Read and harmonise (Python/xarray or CDO)
```python
import xarray as xr
from xarray.coders import CFDatetimeCoder
ds = xr.open_mfdataset("tas_Amon_MODEL_ssp245_r1i1p1f1_*.nc",
                       decode_times=CFDatetimeCoder(use_cftime=True))
# older xarray accepted use_cftime=True directly; current releases warn that it is deprecated
```
- **Calendars:** many models use `noleap` or `360_day`; use cftime and compute monthly or
  annual means rather than aligning by date strings.
- **Units:** K → °C (−273.15); pr flux × 86400 → mm/day. ERA5 precipitation is an
  accumulation (m) — convert carefully per its documentation.
- **Coordinates:** longitudes 0–360 vs −180–180; latitude order; check before subsetting
  a region.
- **Regrid** to a common grid before multi-model comparison: conservative remapping for
  fluxes like precipitation, bilinear acceptable for smooth fields (xESMF or
  `cdo remapcon`/`remapbil`).

## 3. Area-weight every spatial mean
Grid cells shrink toward the poles. Weight by cos(latitude) on regular grids, or better, by
the model's cell-area file (`areacella`). Mask land/ocean with `sftlf` when needed.
Unweighted global means are a common, large error (test field with a pole-to-equator gradient on a 1° grid: unweighted 268.9 K vs cos-lat weighted 273.0 K).

## 4. Anomalies and baselines
- Compute change relative to a stated baseline (e.g. 1995–2014 as in IPCC AR6, or
  1850–1900 for "pre-industrial").
- Compute each model's anomaly against **its own** baseline before combining — models
  have absolute biases of several degrees that anomalies remove.
- Use 20–30-year means for future periods so internal variability does not masquerade as signal.

## 5. Present the ensemble
- Use many models (and, where possible, multiple members); report the **median and a range**
  (e.g. 5–95 % or likely range), not a single model.
- One model = one vote ("model democracy") is the default, but some models share code and
  are not independent; AR6 also used constrained/weighted assessments for warming. If you
  weight or screen models (e.g. by historical performance or climate sensitivity), say so.
- Separate scenario, model and internal-variability uncertainty when possible.

## 6. Local applications
Raw GCM output at ~100 km resolution is biased locally. For impacts work use
**bias correction** (e.g. quantile mapping) and/or **downscaling** (statistical or dynamical,
e.g. CORDEX regional models). Bias correction can distort trends and inter-variable
consistency; trend-preserving methods exist.

## Gotchas
- Some models lack some variables, experiments or members; record exactly which went into
  each number.
- Mixing CMIP5 (RCPs) and CMIP6 (SSPs) is not like-for-like.
- Precipitation trends in reanalysis can be artefacts of changing observing systems.
- Big data volumes: subset server-side or use cloud Zarr with lazy (dask) loading.

The 1995–2014 baseline is the AR6 WGI choice because 2014 ends the CMIP6 historical runs (IPCC AR6 WGI Fig. 1.11 and chapter material). Check the current CMIP data-request tables and CDS documentation for variable details. Checked by running: noleap calendar read with cftime, pr x 86400, cos-lat weighting, longitude wrap.

## Verify
- [ ] Experiments, models, members and dataset versions listed.
- [ ] Calendars, units and longitude conventions harmonised.
- [ ] Spatial means area-weighted; regridding method stated.
- [ ] Anomalies computed per model against a stated baseline period.
- [ ] Results given as ensemble median + range; historical period evaluated against ERA5/observations.
