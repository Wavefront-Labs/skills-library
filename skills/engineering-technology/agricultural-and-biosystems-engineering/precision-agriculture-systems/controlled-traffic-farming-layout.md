---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.controlled-traffic-farming-layout
name: controlled-traffic-farming-layout
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, controlled-traffic, autosteer, machine-guidance, ctf, permanent-wheel-tracks, track-width, compaction]
level: practitioner
status: draft
description: "Plan controlled traffic farming: base track width, machinery width multiples, permanent wheel lanes, RTK repeatability, drainage, and the expected benefit and cost."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Controlled traffic farming layout

**Goal:** confine wheel traffic to permanent lanes so the cropped area stays uncompacted.

## Design
1. **Base track width** (often 3 m in several regions, but locally differs) set by the main tractor, harvester and sprayer tyre centres. All machines are adjusted so their wheels run in the same lanes.
2. **Implement widths** are multiples of the module (for example 6, 9, 12, 18, 24, 36 m): seeder and sprayer match harvesting header width; where a harvester header is not a multiple, use a chaser bin and transfer grain at lane positions.
3. **Lane layout** on contour or with drainage in mind: lanes act as waterways; design grades to avoid erosion; consider tramline and permanent drainage in wet climates.
4. **Guidance**: RTK with repeatable accuracy (about 2 cm) and fixed base coordinates so lanes are reused each year.
5. **Tyres** and track width: match tyre sizes; dual tyres and tracks help flotation; set tyre pressure for lane traction.
6. **Share of area trafficked**: typically about 15 percent in well-designed systems, versus 50-85 percent for random traffic (commonly quoted extension range; compute for your fleet).

## Benefits and costs
Reduced compaction, better infiltration and trafficability, lower fuel use and sometimes yield gains; costs for machinery modification, RTK system and planning. Benefits vary by soil and climate; evaluate on-farm.

## Gotchas
- Machinery fleet incompatibilities; hire contractors who match the system.
- Lane compaction and erosion on slopes need management.

## Verify
- [ ] Measure wheel track alignment between machines and map the percentage of area trafficked.
