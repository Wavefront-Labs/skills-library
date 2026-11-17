---
id: engineering-technology.civil-engineering.civil-3d.pipe-network-design
name: pipe-network-design
category: engineering-technology
field: civil-engineering
product: civil-3d
tags: [civil-3d, pipe-networks, pipe-network, structures, parts-list, pipe-sizing, hydraflow, storm-sewer, invert, rim-elevation, cover-checks]
level: practitioner
status: draft
description: "Lay out a Civil 3D gravity pipe network: parts list, structures, alignment/profile, inverts and cover, pipe rules, hydraulic checks and how to update from changes."
sources: ["Autodesk Civil 3D Help (Pipe Networks)", "Local storm sewer design criteria", "FHWA HEC-22 Urban Drainage Design Manual"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pipe network design in Civil 3D

## Setup
1. Create a pipe network parts list: pipe families (concrete, PVC, HDPE) with size ranges, and structure families (manhole, pit, inlet). Names must match the authority's standard drawings and catalogue.
2. Draw the network from the Pipe Network Layout Tools (by layout or from objects such as polylines/alignments). Set a surface for rim elevation and an alignment for station-based design.
3. Apply pipe rules (minimum cover, minimum slope, maximum drop across structures, minimum diameter, maximum length between structures) and structure rules so Civil 3D flags violations or adjusts them (`Apply Rules`).
4. Check invert levels: pipe slopes must give minimum self-cleansing velocity (commonly about 0.6 to 0.9 m/s at design flow; local criteria vary), drops through structures, cover (often 0.6 m or more under roads; check the authority's), clearances to other utilities.
5. Profile view: draw the network in a profile along the alignment to inspect crossings and cover.
6. Hydraulics: use Hydraflow Storm Sewers Extension or export to SWMM/Storm and Sanitary Analysis to compute HGL, check surcharging and pipe capacity; Manning's equation for pipe full flow Q = (1/n) A R^(2/3) S^(1/2).
7. Edit parts rather than delete/re-add so that connections hold; use label styles for pipe size, slope and invert.

## Gotchas
- Surface changes do not always update rim elevations unless the network is set to the surface and refreshed.
- Pipes can be disconnected from structures after copy; check connectivity in the Pipe network vistas.
- Authority's part catalogue may differ from the default Autodesk parts: build a custom part list.

## Verify
Design report lists violations of rules as zero; hand-check one reach's capacity; plan and profile labels agree with the model.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
