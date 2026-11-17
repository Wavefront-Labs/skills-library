---
id: engineering-technology.civil-engineering.hec-ras.bridge-hydraulics-modelling
name: bridge-hydraulics-modelling
category: engineering-technology
field: civil-engineering
product: hec-ras
tags: [hec-ras, hec-ras-bridge, bridge-hydraulics, bridge-scour, energy-method, momentum-method, yarnell, wspro, pressure-flow, weir-flow, low-flow-high-flow]
level: advanced
status: draft
description: "Model a bridge in HEC-RAS: four-section layout, low-flow method choice (energy, momentum, Yarnell, WSPRO), pressure and weir flow, ineffective areas, and checks."
sources: ["USACE HEC-RAS Hydraulic Reference Manual (Modeling Bridges chapter)", "FHWA HDS-1 Hydraulics of Bridge Waterways", "FHWA HEC-18 Evaluating Scour at Bridges"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Bridge hydraulics in HEC-RAS

## Cross-section layout
Use the four-section approach: section 1 downstream of the structure at the end of the expansion zone, section 2 just downstream of the face, section 3 just upstream of the face, section 4 upstream at the start of the contraction zone. Sections 2 and 3 are cut at the structure faces; ineffective flow areas at 2 and 3 represent the contraction/expansion of flow into and out of the opening. Section positions are set from expansion and contraction ratios and distances in the reference manual.

## Bridge data
Deck/roadway profile (high chord), low chord, piers (width, shape), abutments, skew, and sloping abutment embankments.

## Low flow (flow below the low chord)
Choose by situation: Energy (standard step) default, Momentum when piers cause significant loss, Yarnell for pier losses with Class A flow only, WSPRO for contracting-flow situations. Several methods can be computed and the highest water surface taken (a common conservative option).

## High flow
- Pressure flow when upstream stage reaches the low chord (orifice flow) and weir flow when overtopping the deck/road. Energy or pressure/weir equations with discharge coefficients and submergence; choose coefficients per the manual.
- Use the Hydraulic Reference Manual to check the coefficient ranges.

## Scour
HEC-RAS outputs hydraulic variables for HEC-18 calculations; scour is a separate analysis.

## Checks
Look for sections with water surface below channel inverts, bridge cross-section warnings and sudden energy jumps; run sensitivity of n and coefficients; compare with observed high-water marks.

## Verify
Headloss across the bridge consistent with another method; flow split sums to total.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
