---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.scs-curve-number-runoff
name: scs-curve-number-runoff
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [curve-number, scs, nrcs, tr-55, runoff-depth, hydrologic-soil-group, antecedent-moisture, initial-abstraction, unit-hydrograph, hec-hms]
level: practitioner
status: draft
description: "Compute direct runoff depth with the NRCS curve number method: CN by soil group and land use, S, Ia = 0.2S, runoff equation, AMC, limits and TR-55 use."
sources: ["NRCS National Engineering Handbook Part 630 Hydrology", "USDA TR-55 Urban Hydrology for Small Watersheds", "Chow, Maidment and Mays, Applied Hydrology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# NRCS curve number runoff

Inches: S = 1000/CN - 10. Initial abstraction Ia = 0.2 S (traditional). Runoff Q = (P - Ia)^2 / (P - Ia + S) for P > Ia, else 0. SI: S(mm) = 25400/CN - 254.

## Steps
1. Hydrologic soil group A to D from the soil survey (A infiltrates well, D is clay or high water table).
2. CN from the land use, cover and treatment table; area-weight a composite CN only when the subareas drain together, otherwise compute runoff per subarea.
3. Use average condition (II) unless the agency says otherwise; conditions I and III are conversions.
4. P from the design storm (24 h with SCS Type I, IA, II, III distribution by region).
5. Apply the runoff equation, then a unit hydrograph (SCS dimensionless, peak rate factor commonly 484) in HEC-HMS or the TR-55 methods.

## Gotchas
- Connected vs unconnected impervious area changes CN.
- Weak for small storms and low CN; some calibrations use Ia = 0.05 S. Use the ratio your jurisdiction requires.
- Not for snowmelt or frozen ground.

## Verify
Q = 0 at P = Ia; Q < P always; Q approaches P - S as P grows.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
