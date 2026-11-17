---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.rational-method-peak-flow
name: rational-method-peak-flow
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [rational-method, peak-flow, time-of-concentration, runoff-coefficient, intensity-duration-frequency, idf, catchment, drainage-design]
level: practitioner
status: draft
description: "Compute design peak flow with the rational method Q = CiA: time of concentration, IDF intensity, runoff coefficient, units, catchment limits and when to use hydrographs."
sources: ["Chow, Maidment and Mays, Applied Hydrology", "FHWA HDS-2 Highway Hydrology", "Australian Rainfall and Runoff (Geoscience Australia)", "Local drainage manuals (check jurisdiction)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Rational method peak flow

Formula: Q = C i A / K. SI: Q in m3/s, i in mm/h, A in km2, K = 3.6 (Q = 0.278 C i A). US: Q in cfs, i in in/h, A in acres, K about 1.

## Steps
1. Delineate the catchment from survey or LiDAR and confirm the outlet.
2. Time of concentration tc: sum of overland (sheet), shallow concentrated and channel/pipe flow times. Use the method your authority prescribes; minimum tc is often 5 to 10 min.
3. Intensity i from the IDF curve for duration = tc and the design AEP/return period. Never take it from a different duration.
4. Runoff coefficient C from land use and slope tables; some manuals raise C for rarer storms. Composite C = sum(Ci Ai)/sum(A).
5. Multiply. At downstream nodes recompute with the longer tc; take the maximum at each point, do not just sum upstream peaks.

## Limits
- For small mainly urban catchments (drainage manuals commonly cap near a few hundred acres or about 1 km2; local limits vary). For storage design, large or complex catchments use a hydrograph method (unit hydrograph, curve number, RORB, HEC-HMS).
- Assumes uniform rainfall and steady peak at tc; it gives no volume.

## Verify
Units trace on paper; compare against an independent method (regional regression or flood frequency); check C against a measured gauge if available.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
