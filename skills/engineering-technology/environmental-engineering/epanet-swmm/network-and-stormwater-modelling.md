---
id: engineering-technology.environmental-engineering.epanet-swmm.network-and-stormwater-modelling
name: network-and-stormwater-modelling
category: engineering-technology
field: environmental-engineering
product: epanet-swmm
tags: [environmental-engineering, epanet-swmm, epanet, swmm, epanet-2-2, swmm-5-2, water-distribution, hydraulic-model, stormwater-model, urban-drainage, hazen-williams, darcy-weisbach, chezy-manning, pressure-driven-analysis, demand-driven-analysis, dynamic-wave, kinematic-wave, routing-step, continuity-error, water-age, chlorine-decay, model-calibration, horton, green-ampt, curve-number, wntr, pyswmm, us-epa, water-quality-modelling, runoff-simulation]
level: practitioner
status: gated
description: "Build, run and calibrate EPANET 2.2 water networks and SWMM 5.2 stormwater models: head-loss and demand options, routing method and step, continuity checks, calibration."
sources: ["US EPA, EPANET 2.2 User Manual", "US EPA, Storm Water Management Model (SWMM) User's Manual Version 5.2", "Rossman, SWMM Reference Manual Volume I (Hydrology) and Volume II (Hydraulics), US EPA", "Walski et al., Advanced Water Distribution Modeling and Management", "CIWEM Urban Drainage Group, Code of Practice for the Hydraulic Modelling of Urban Drainage Systems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network and stormwater modelling — EPANET 2.2 and SWMM 5.2 done properly

**Goal:** an EPANET network or SWMM drainage model with deliberate options, healthy
numerics and field calibration before anyone designs from it.

## 1. Set up the EPANET 2.2 options first
| Option | Choices / typical value | Guidance |
|---|---|---|
| Flow units | GPM, MGD, CFS… (US) or LPS, LPM, MLD, CMH… (SI) | The flow unit sets the whole unit system; pick once. |
| Head-loss formula | Hazen-Williams (H-W), Darcy-Weisbach (D-W), Chezy-Manning (C-M) | H-W is the industry habit for water (C ≈ 140–150 new PVC/lined DI, 100–120 old unlined iron). D-W is physically correct for any fluid/temperature; roughness in mm (or millifeet in US units). Never mix roughness values meant for another formula. |
| Demand model | DDA (demand-driven) or PDA (pressure-driven) | DDA delivers full demand even at negative pressure. Use PDA for fire flow, outages, low-pressure zones: set minimum pressure (no flow below), required pressure (full demand), and pressure exponent (0.5 is the usual orifice value per the EPANET 2.2 manual; DDA is the default model, minimum pressure defaults to 0 and required pressure to 0.1, all confirmed from the 2.2 documentation). |
| Accuracy / trials | default accuracy 0.001; trials limit (check your build's default) | 2.2 also offers head-error and flow-change limits; tighten them if the run reports unbalanced solutions. |
| Time steps | hydraulic 1 h for EPS, quality step ~5 min | Quality step must be ≤ the hydraulic step; shorten the hydraulic step if tanks/controls switch often. |

Quality: *Age*, *Trace* or *Chemical* with bulk (Kb, 1/day, negative for decay) and
wall (Kw) coefficients; measure chlorine Kb by bottle tests. Run water-age EPS for
several days (often 7–14) so tank ages stabilise.

## 2. Set up the SWMM 5.2 options
- **Infiltration:** Horton / Modified Horton, Green-Ampt / Modified Green-Ampt, or
  SCS Curve Number. Use the one your soil data supports; don't calibrate a CN model
  with Horton thinking.
- **Routing model:** *Steady flow* (screening only), *Kinematic wave* (dendritic
  networks, no backwater, no surcharge physics) or *Dynamic wave* (needed for
  backwater, loops, flow reversal, surcharge, pumps/weirs interacting, tidal outfalls).
- **Routing step:** kinematic wave tolerates 30–60 s; dynamic wave typically 1–30 s (rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
  Enable variable time step (safety factor around 75 %) and set a minimum step
  (e.g. 0.5 s). Keep the runoff wet step ≤ the rainfall interval (5 min data → 5 min
  or less).
- **Dynamic wave settings:** inertial terms (dampen is the usual default), normal
  flow limitation (slope / Froude / both), surcharge method (Extran or Slot in 5.2),
  head convergence tolerance and max trials per step. Leave defaults until a problem
  forces a change, then change one at a time.

## 3. Build and check the network
Import GIS assets with traceable IDs; check for orphan nodes, zero-length links,
inverts climbing downstream and unintended closed valves. Assign demands from meter
data and diurnal patterns (EPANET), or subcatchment area, imperviousness, width and
slope (SWMM; width ≈ area ÷ overland flow length is the most sensitive parameter).
Run steady state before extended-period or design-storm runs.

## 4. Judge numerical health before results
- **EPANET:** the status report must show no "system unbalanced" or "negative
  pressures" warnings you can't explain; disconnected nodes are an error, not a nuance.
- **SWMM:** read the report's continuity errors. Target runoff and flow-routing
  continuity error within about ±1–2 %; above ~5 % the results are not usable (rule-of-thumb thresholds; the SWMM manual's own cutoff was not found (gated: unconfirmed, source is paywalled or blocked) — check the current User's Manual). Then
  read *Highest Flow Instability Indexes* and *Time-Step Critical Elements*: fix short
  conduits (lengthen or merge), tiny storage nodes, and abrupt diameter changes.

## 5. Calibrate and verify
- Water networks: hydrant flow tests and pressure loggers across zones; adjust
  roughness by pipe group (material/age), then demands, then valve status. Many
  guidelines aim for heads within roughly 1–2 m (check your utility's standard (gated: unconfirmed, source is paywalled or blocked)).
- Drainage: flow/depth surveys over several storms; calibrate on some events, verify
  on others, against peak-flow, volume and depth tolerance bands from the client's
  current guidance (e.g. CIWEM).

## 6. Scripting
In Python, **WNTR** (EPA/Sandia) reads EPANET `.inp` files and adds pressure-driven
and resilience analyses; **PySWMM** steps a SWMM run and can alter states mid-run
(e.g. real-time control). Script scenario batches instead of hand-editing `.inp` files.

## Gotchas
- H-W is invalid for non-water fluids and very low/high Reynolds numbers; use D-W.
- DDA hides failures: a network that "works" at -20 m pressure is broken.
- Kinematic wave ignores backwater: tailwater has no effect.
- Units inherited from an imported `.inp` file (US vs SI) catch everyone once.

## Verify
- [ ] Head-loss formula, demand model and units are stated in the model report.
- [ ] EPANET runs without unbalanced/negative-pressure warnings, or each is explained.
- [ ] SWMM runoff and routing continuity errors are within about ±2 %.
- [ ] Routing method justified (dynamic wave wherever backwater or surcharge matters).
- [ ] Calibrated against field data and verified on an independent event or test.
