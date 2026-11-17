---
id: natural-sciences.oceanography.ocean-modelling.regional-ocean-model-setup-and-validation
name: regional-ocean-model-setup-and-validation
category: natural-sciences
field: oceanography
product: ocean-modelling
tags: [ocean-modelling, ocean-model, regional-model, roms, croco, mom6, nemo, grid-generation, bathymetry-smoothing, open-boundary-conditions, atmospheric-forcing, era5, spin-up, time-step, model-validation, skill-score, taylor-diagram, model-data-comparison]
level: advanced
status: docs-checked
description: "Set up and validate a regional ocean model: grid and bathymetry, boundary and surface forcing (ERA5 accumulation trap), spin-up and independent model-data skill metrics."
sources: ["https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regional ocean model setup and validation

**Goal:** a regional simulation that is numerically stable, forced sensibly, spun up,
and *shown* to reproduce observations for the processes you will use it to study.
Numeric thresholds (slope limits, time steps, spin-up length) are model-specific: take
them from your model's own documentation and record where you got them.

## 1. Frame the question first
Resolution, domain and physics follow from the question (eddies, shelf tides, upwelling).
Decide the processes to resolve, then check the grid spacing resolves them.

## 2. Grid and bathymetry
- Place open boundaries away from the area of interest and where the flow is simple.
- Smooth bathymetry for terrain-following models and check the slope/stiffness metrics
  your model's documentation defines; steep slopes cause pressure-gradient errors.
- Set a minimum depth unless wetting/drying is on.
- Concentrate vertical levels where the dynamics are (surface mixed layer, bottom on shelves).

## 3. Forcing
- Initial and boundary conditions come from a global analysis or reanalysis: T, S,
  velocities, sea-surface height. Record the product and version.
- Open boundary schemes and tidal forcing follow your model's documentation. Mismatches
  show as noise and spurious currents along boundaries.
- Surface forcing from an atmospheric reanalysis such as ERA5 through bulk formulae. Unit
  trap, per the ECMWF ERA5 data documentation: radiation and precipitation are
  accumulations (for the reanalysis, over the hour ending at the validity time), whereas
  analysed fields such as 2 m temperature are instantaneous. Convert accumulations to
  rates before use.
- Rivers: discharge and temperature at point sources.

## 4. Running
- Blow-ups in the first days usually mean a too-long time step, bad bathymetry or boundary
  inconsistencies.
- Spin-up: plot domain-averaged kinetic energy, T and S until they stabilise and discard
  that period.
- Keep a run log: code version, compile options, namelist, input file versions.

## 5. Validation
- Compare against independent observations not used in forcing (tide gauges, profiles,
  moorings, satellite fields, radar currents).
- Report bias, RMSE and correlation; a Taylor diagram summarises correlation, standard
  deviation and centred RMS together.
- Validate the processes you will study, not just mean SST.
- For biogeochemical models validate the physics first.

## Gotchas
- Boundary data interpolated with mismatched vertical coordinates or land masks.
- Model point output compared with observations at a different depth or time average.
- Tuning mixing to match the validation set, then calling that validation.
- Mixing up potential and in-situ temperature in initial conditions.

## Verify
- [ ] Bathymetry slope metrics checked against the model's documented limits.
- [ ] Model stable for the full period; boundary regions free of noise.
- [ ] Spin-up period identified from domain diagnostics and excluded.
- [ ] Validation against independent data with bias, RMSE and correlation reported.
- [ ] Code version and all inputs recorded.

## Checked
2026-11-01. Confirmed in the ECMWF ERA5 data documentation: radiation and precipitation are
accumulations (reanalysis accumulations are over the hour ending at the validity time) and
analysed fields are instantaneous. Removed (not confirmed in a page read): Rossby radius
figures, rx0/rx1 target values, CFL expression, spin-up durations, named bathymetry, tide and
reanalysis products, and boundary scheme names.
Method: documentation only; no commands were run.
