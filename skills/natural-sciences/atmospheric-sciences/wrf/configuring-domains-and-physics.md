---
id: natural-sciences.atmospheric-sciences.wrf.configuring-domains-and-physics
name: configuring-domains-and-physics
category: natural-sciences
field: atmospheric-sciences
product: wrf
tags: [wrf, wrf-arw, weather-research-and-forecasting, wps, geogrid, ungrib, metgrid, real-exe, wrf-exe, namelist-input, namelist-wps, nesting, parent-grid-ratio, domain-design, map-projection, lambert-conformal, time-step, cfl, physics-options, microphysics, pbl-scheme, cumulus-parameterisation, convection-permitting, gray-zone, era5-boundary-conditions, gfs, spin-up, wrf-python, ncl, post-processing]
level: advanced
status: docs-checked
description: "Set up a WRF run: WPS steps, nested domain design and ratios, time step from grid spacing, physics suites, cumulus in the gray zone, boundary data, spin-up and common crashes."
sources: ["https://raw.githubusercontent.com/wrf-model/WRF/master/run/README.namelist"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring WRF domains and physics

**Goal:** a WRF-ARW simulation with sensibly designed domains and physics that runs
stably and whose output answers your question — without weeks of trial and error.

## 1. The pipeline
1. **WPS** (`namelist.wps`):
   - `geogrid.exe` — defines domains on a map projection and interpolates static data
     (terrain, land use, soil). Download the mandatory high-resolution geog data.
   - `ungrib.exe` — extracts meteorological fields from GRIB (GFS, ERA5, etc.) using the
     matching **Vtable**.
   - `metgrid.exe` — interpolates them onto the domains → `met_em*` files.
2. **real.exe** — vertical interpolation, creates `wrfinput_d0*` and `wrfbdy_d01`.
3. **wrf.exe** — the model run, configured by `namelist.input`.
Check `rsl.error.0000` / `rsl.out.0000` after each step; they report the real cause of failures.

## 2. Domain design
- **Projection:** choose the map projection to suit your latitude and plot the domains before running geogrid in full.
- **Nesting ratio:** `parent_grid_ratio` is the parent-to-nest grid size ratio (odd integers such as 3 are typical),
  e.g. 27 → 9 → 3 km. Keep nests well inside their parents, away from parent boundaries.
- Make domains large enough that the weather systems you care about develop inside the
  domain, not at the boundaries; the outer domain's boundaries are where large-scale data enter.
- **Vertical levels:** `p_top_requested` is the model top in Pa (the README example is 5000). Use more
  levels near the surface for boundary-layer studies.

## 3. Time step
Rule of thumb: **time_step (s) ≈ 6 × dx (km)** for the outermost domain (the README recommends 6*dx for typical real-data cases; 27 km → 162 s, so use 160 or less). Nests use `parent_time_step_ratio`. Adaptive
time stepping is available (`use_adaptive_time_step`). CFL errors in `rsl` files mean the step is too long or winds
are extreme — reduce it.

## 4. Physics choices
Start from a tested suite rather than mixing schemes freely. The README defines
`physics_suite = 'CONUS'` (mp_physics 8, ra_lw/ra_sw 4, bl_pbl 2, sf_sfclay 2, sf_surface 2) and `'tropical'` (mp_physics 6, ra 4, bl_pbl 1, sf_sfclay 91, sf_surface 2).
Key decisions:
- **Microphysics** (`mp_physics`): Thompson (8) and WSM6 (6) are the suite defaults above.
- **PBL** (`bl_pbl_physics`) with its matching surface layer (`sf_sfclay_physics`); some PBL schemes require specific surface
  layer options — the namelist check will complain.
- **Cumulus** (`cu_physics`): usually switched off at convection-permitting spacing; in the **gray zone** prefer a scale-aware scheme or avoid that spacing.
- **Radiation:** RRTMG (4) for both long- and shortwave; `radt` is minutes between radiation calls.
- **Land surface:** Noah (2) in both suites; match `num_soil_layers` and the input data.

## 5. Boundary and initial conditions
- Interval (`interval_seconds`) must match the input data (e.g. 21600 for 6-hourly GFS,
  3600 for hourly ERA5).
- Discard a **spin-up** period (length depends on the application; longer for soil moisture in
  regional climate runs).
- For long runs, consider spectral/grid nudging on the outer domain to keep large scales on track.

## 6. Output and post-processing
- `history_interval` per domain; `frames_per_outfile` to keep files manageable.
- wrf-python (`getvar`, `interplevel`) or NCL/UPP; WRF uses a staggered Arakawa-C grid —
  destagger winds before computing derived fields.

## Common crashes
- "Segmentation fault": stack size, CFL, or memory.
- Mismatched number of metgrid levels (`num_metgrid_levels`, `num_metgrid_soil_levels`) —
  read from `ncdump -h met_em...`.
- Missing SST or land-sea mask inconsistency over lakes/coasts — check land use and SST updating.

Verify option numbers against the `README.namelist` of your version.

## Checked
2026-11-01. Confirmed against WRF run/README.namelist (master): time_step 6*dx recommendation, parent_grid_ratio, parent_time_step_ratio, use_adaptive_time_step, p_top_requested, radt, and the CONUS and tropical physics_suite definitions. Removed: nest size divisibility rule, resolution-jump rule, level counts, Morrison/MYNN/YSU pairings, cumulus spacing thresholds, radt rule, w_damping advice and Noah-MP number (not confirmed).

Method: documentation only; no commands were run.

## Verify
- [ ] geogrid output plotted; nests well inside parents, sizes divisible by ratio.
- [ ] Time step consistent with dx; no CFL warnings.
- [ ] Cumulus on/off appropriate to each domain's spacing.
- [ ] real.exe completes; interval matches driving data.
- [ ] Spin-up discarded; output checked against observations.
