---
id: engineering-technology.civil-engineering.hec-ras.two-d-flood-model
name: two-d-flood-model
category: engineering-technology
field: civil-engineering
product: hec-ras
tags: [hec-ras, usace, hydrologic-engineering-center, 2d-modelling, two-dimensional, unsteady-flow, flood-modelling, floodplain-mapping, ras-mapper, mesh, breaklines, manning-n, land-cover, courant-number, diffusion-wave, shallow-water-equations, rain-on-grid, boundary-conditions, flood-extent, model-calibration, volume-accounting, hydraulic-modelling, aep, 1-percent-aep]
level: advanced
status: verified
description: "Set up, run and check a HEC-RAS 2D unsteady flood model: terrain, mesh and breaklines, Manning's n land cover, boundary conditions, time step and Courant control."
sources: ["USACE HEC-RAS Hydraulic Reference Manual", "USACE HEC-RAS 2D Modeling User's Manual", "USACE HEC-RAS User's Manual", "Chow, Open-Channel Hydraulics (1959)", "Arcement & Schneider, USGS WSP 2339: Guide for Selecting Manning's Roughness Coefficients for Natural Channels and Flood Plains"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# HEC-RAS 2D flood model — from terrain to a defensible flood extent

**Goal:** a stable, mass-conserving 2D unsteady model whose depths, velocities and
extents for the design event (commonly the 1% AEP / "100-year") you can defend in review.
Written against HEC-RAS 6.x; menu names drift between versions.

## 1. Terrain (RAS Mapper)
1. Set the **projection** first (an ESRI .prj in a metric or US-feet projected CRS).
   Everything else inherits it.
2. Import the DEM (LiDAR, 1 m or 1 ft typical) as a Terrain. Layer in a separate
   bathymetry/channel surface with higher priority — LiDAR rarely sees below water.
3. Use **terrain modifications** for culverts' openings, levee crests or channel
   burns rather than editing the raw DEM.
Sub-grid bathymetry lets cells be larger than the DEM pixel, but only if cell faces
line up with controlling features.

## 2. Mesh
- **Perimeter** around the whole area that can get wet, plus margin. A perimeter that
  clips the flood creates glass walls.
- **Base cell size:** commonly 10–50 m (30–150 ft) in the floodplain, 2–10 m in urban
  streets (practice figures, not from the manual (gated: unconfirmed, source is paywalled or blocked)). Have at least ~3–5 cells across the main channel's active width if the
  channel is in the 2D area (or model the channel in 1D).
- **Breaklines** along levees, road embankments, channel banks, walls; set a smaller
  cell spacing along them (use the breakline Near Spacing, Near Repeats and Far Spacing settings, which default to the nominal cell size; half the base is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)). Faces
  must sit on crests or flow leaks over them.
- **Refinement regions** at structures and constrictions; fix every mesh error RAS
  Mapper reports before running.

## 3. Roughness (Manning's n)
Build a land-cover layer and assign n. Indicative values from Chow (1959) Table 5-6 as commonly quoted (gated: unconfirmed, source is paywalled or blocked). Note USGS WSP 2339 is a base-value-plus-adjustments method, not a land-cover table; use it for channel and floodplain n build-up:
| Cover | n |
|---|---|
| Asphalt/concrete roads | 0.015–0.020 |
| Short grass / pasture | 0.030–0.040 |
| Crops | 0.035–0.050 |
| Light brush | 0.050–0.070 |
| Dense trees | 0.100–0.160 |
| Main channel, clean natural | 0.030–0.040 |
Buildings: either block them out of the mesh or use a high n (values from ~0.3 to 1.0
appear in practice — check local guidance; several Australian state guidelines publish
recommended values). Use a calibrated value, not the first table entry.

## 4. Boundary conditions
- **External BC types in the manual:** Flow Hydrograph, Stage Hydrograph, Normal Depth, Rating Curve. Normal Depth takes a friction slope (from the land slope near the BC line); Flow Hydrograph takes an energy slope used to distribute flow to wet cells.
- **Inflow:** Flow Hydrograph on an external BC line, with an EG slope for
  distributing flow — or rain-on-grid (Precipitation BC) for direct rainfall.
- **Outflow:** Normal Depth with a friction slope approximating the local bed slope,
  placed far enough downstream (several cell widths, ideally beyond the study reach) that
  the assumption cannot influence results. Or a Stage Hydrograph if tidal/known.
- **Initial conditions:** use a ramp-up or a short initial-conditions period so the
  model starts wet and stable; don't trust the first hours of output.

## 5. Equations, time step, Courant
- **Diffusion Wave** (HEC-RAS 6.x ships it as a selectable option; confirm the default in your project) is fast and fine for gradually varied floodplain
  flow. Use **full momentum / Shallow Water Equations (SWE-ELM or SWE-EM)** for
  rapidly varying flow, dam break, sharp contractions, supercritical flow, or
  wherever momentum matters around structures.
- Courant number C = V·Δt / Δx. HEC-RAS 2D User's Manual ("Selecting an Appropriate Grid Size and Time Step"): Diffusion Wave keep C at or below 2, maximum 5 for gradually changing events (rapidly rising hydrographs or dry-channel routing may need C at or below 1); SWE-EM keep C at or below 1; SWE-ELM target 1, up to 3 may stay stable and accurate. Setting C = 1 gives Δt ≤ ΔX/V (SWE) or 2ΔX/V (diffusion wave).
- Use the **adaptive time step based on Courant** (Unsteady Analysis › Computation
  Options) with sensible min/max; or set Δt ≈ Δx_min / V_max.

## 6. Run and interrogate
1. Read the **computation messages**: iteration warnings, 2D cells exceeding
   iteration limits, and the **volume accounting error** — the manual gives no numeric limit (its example overall error is 0.02%, called very low), so agree a tolerance with the reviewer (gated: unconfirmed, source is paywalled or blocked).
2. In RAS Mapper, check max depth, max velocity and max WSE. Look for checkerboarding,
   cells that drain/fill in alternate steps, and velocity spikes at faces.
3. Run a **mesh sensitivity**: halve the cell size locally — peak levels changing by
   more than a tolerance agreed with the reviewer (e.g. 50–100 mm, 0.2–0.3 ft; rule of thumb (gated: unconfirmed, source is paywalled or blocked)) mean the mesh is not converged there.
4. Calibrate against gauge records or surveyed debris lines from historic floods;
   adjust n within physically plausible ranges, never far outside the table.

## Gotchas
- Flow appearing on the wrong side of a levee almost always means a missing or
  misaligned breakline, not a roughness issue.
- Rain-on-grid models "wet" every depression; filter mapped extents by a depth
  threshold (e.g. 50–100 mm) agreed with the reviewer.
- 1D/2D connections (lateral structures, SA/2D connections) are the commonest
  instability source; check weir coefficients and that elevations match the terrain.

## Verify
- [ ] Mesh has no errors; breaklines follow every embankment that controls flow.
- [ ] Volume accounting error small and within the agreed tolerance, and no repeated iteration-limit warnings.
- [ ] Courant numbers in the governing cells are within the version's guidance for the chosen equation set.
- [ ] Downstream boundary is far enough away that changing its slope barely moves levels in the study area.
- [ ] Mesh-sensitivity run shows converged peak levels.
- [ ] Results reproduce a historic event or gauge within an agreed tolerance, or the model is reported as uncalibrated.
