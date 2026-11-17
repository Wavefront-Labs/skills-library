---
id: engineering-technology.civil-engineering.stormwater-drainage-design.detention-basin-sizing
name: detention-basin-sizing
category: engineering-technology
field: civil-engineering
product: stormwater-drainage-design
tags: [detention-basin, stormwater-detention, storage-volume, outlet-structure, orifice, weir, pre-post-development, routing, modified-puls, freeboard, emergency-spillway]
level: practitioner
status: draft
description: "Size a detention basin so post-development peak flow does not exceed pre-development: storage estimate, orifice and weir outlets, routing check, emergency spillway."
sources: ["FHWA HEC-22 Urban Drainage Design Manual", "Local stormwater design manuals (jurisdiction specific)", "Chow, Maidment and Mays, Applied Hydrology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Detention basin sizing

Goal: limit post-development outflow to the pre-development (or authority) rate for each required storm and pass the extreme event safely.

## Steps
1. Pre- and post-development hydrographs or peaks for the required AEPs (e.g. 2, 10 and 100 year). Allowable discharge is the pre-development peak or a per-hectare site rate if the authority sets one.
2. Preliminary storage: triangular hydrograph or modified rational method; refine by routing.
3. Outlet: orifice Q = Cd A sqrt(2 g h), Cd about 0.6 sharp-edged, h to the orifice centroid. Sharp-crested weir Q = C L H^1.5 (C about 1.7 in SI, 3.1 in US units). Use staged outlets for multiple storms.
4. Route (level-pool or modified Puls) in HEC-HMS, SWMM or a spreadsheet with a stage-storage-discharge table. Try several durations; the critical duration exceeds tc.
5. Emergency spillway sized for the authority's extreme event with the primary outlet blocked; add freeboard per local rule (often 0.3 m or more).
6. Safety and upkeep: side slopes per local rule, forebay, access, outlet screen, dam-safety thresholds (height and volume triggers vary by jurisdiction).

## Gotchas
- Tailwater can drown the outlet: check downstream rating.
- Several basins in series can worsen downstream peaks by shifting timing.
- Allow for sediment build-up.

## Verify
Routed peak outflow is at or below allowable for all AEPs; routing mass balance closes within a few percent.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
