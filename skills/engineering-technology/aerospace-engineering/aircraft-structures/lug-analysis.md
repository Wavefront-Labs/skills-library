---
id: engineering-technology.aerospace-engineering.aircraft-structures.lug-analysis
name: lug-analysis
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [lug-analysis, lugs, pin-joints, bearing, net-section, joints-and-fasteners]
level: practitioner
status: draft
description: "Analyse axially and obliquely loaded lugs for net-section tension, bearing and shear tear-out using handbook efficiency factors, and check fatigue and bushings."
sources:
  - "MMPDS (joints chapter)"
  - "Bruhn, Analysis and Design of Flight Vehicle Structures"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lug analysis

**Goal:** margins for a clevis or single-shear lug carrying a pin load.

## Failure modes
- Net-section tension through the hole at the lug width.
- Bearing of the pin on the hole.
- Shear tear-out or shear-bearing near the edge.
- Hoop tension (the governing mode for short edge distance).
- Pin bending or shear; bushing slip.

## Method (handbook approach)
1. Geometry: pin diameter `D`, lug width `W`, edge distance `e`, thickness `t`. Ratios `W/D` and `e/D` set the efficiency.
2. Axial ultimate strength from handbook factors: `P = K * A_br * Ftu`, with `A_br = D t` and a coefficient `K` read from curves versus `e/D`, `W/D` and material. The curves and the efficiency factor definitions (axial, transverse, and combined obliquity) are published in MMPDS and in Bruhn; read the exact form from the edition you hold.
3. Obliquity: combine the axial and transverse capacity with the interaction rule in the handbook (an `R_a^1.6 + R_tr^1.6 = 1` type rule is used for aluminium lugs; confirm the exponent for your reference before use).
4. Check bearing yield at limit load against bearing yield allowable and the pin shear and bending.
5. Fatigue: stress concentration at the hole, fretting, and the need for bushings and interference fits.

## Gotchas
- Grain direction matters: transverse-grain lug strength is much lower in many alloys.
- Edge distance below about 1.5 D is a red flag for hoop failure.
- Clearance fits and pin bending shift loads; do not ignore.

## Verify
- [ ] Margins for ultimate (net, bearing, tear-out) and yield bearing are all reported with the allowable's source.
