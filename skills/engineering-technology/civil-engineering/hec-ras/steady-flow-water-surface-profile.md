---
id: engineering-technology.civil-engineering.hec-ras.steady-flow-water-surface-profile
name: steady-flow-water-surface-profile
category: engineering-technology
field: civil-engineering
product: hec-ras
tags: [hec-ras, hec-ras-steady, steady-flow, water-surface-profile, standard-step, cross-sections, manning-n, expansion-contraction, reach-boundary-conditions, flow-regime, floodway]
level: practitioner
status: draft
description: "Build a HEC-RAS 1D steady-flow profile model: cross-sections, Manning n, contraction/expansion, flow data, boundary conditions, mixed flow regime and sanity checks."
sources: ["USACE HEC-RAS Hydraulic Reference Manual", "USACE HEC-RAS User's Manual", "Chow, Open-Channel Hydraulics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# HEC-RAS 1D steady-flow profile

Goal: water surface elevations along a reach for given peak flows by the standard-step energy method.

## Build
1. Geometry: river centreline, cross-sections perpendicular to flow, listed from upstream to downstream, with station-elevation, left/right bank stations, downstream reach lengths (left overbank, channel, right overbank), Manning n by segment, and contraction/expansion coefficients (commonly 0.1 and 0.3 for gradual transitions, up to 0.3 and 0.5 near bridges or abrupt changes; confirm in the manual for the version used).
2. Add ineffective flow areas and blocked obstructions where flow does not convey (behind embankments, in dead storage). Add levees where they cut off overbank flow.
3. Flow data: peak flow per profile (for example 10-, 50- and 100-year), changes at tributaries. Do not forget the lowest flow to test the channel itself.
4. Boundary conditions: subcritical regime needs a downstream condition (known WS, critical depth, normal depth with a friction slope, or rating curve); supercritical needs upstream; mixed flow needs both. Normal depth at the end is an assumption: place the boundary far enough downstream that errors damp out before the area of interest.
5. Run with the regime set to subcritical, supercritical or mixed as the reach demands.

## Checks
- Energy loss, critical depth flags, and warnings in the output log; no "assumed critical depth" at key cross-sections without reason.
- Section spacing adequate: interpolate where the water surface jumps; large energy changes between neighbours mean sections too far apart or too different.
- Calibrate n against high-water marks or gauge ratings when available.
- Floodway encroachment analysis follows only after the base model is trusted.

## Verify
Compare one section by hand with Manning's equation; mass balance flows; check a steady 1D result against a 2D run where flow is complex.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
