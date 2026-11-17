---
id: engineering-technology.aerospace-engineering.aircraft-structures.bonded-joint-design
name: bonded-joint-design
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [bonded-joints, adhesive-joints, peel-stress, lap-shear, hart-smith, joints-and-fasteners]
level: practitioner
status: draft
description: "Design adhesively bonded lap and scarf joints with shear-lag stress models, avoid peel, size overlap, and plan surface preparation and testing."
sources:
  - "Hart-Smith, adhesive-bonded joint analyses (NASA contractor reports)"
  - "ASTM D1002"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Bonded joints

**Goal:** a bonded joint whose strength is set by the adherends, not the adhesive.

## Principles
- Load is transferred over the ends of the overlap, not uniformly: the shear-lag (Volkersen) solution has stress peaks at both ends and a low plateau between.
- A long enough overlap (several multiples of the load-transfer length) makes the adhesive plastic zone carry the load, and adding length adds no strength.
- Single-lap joints have eccentric load paths, creating peel stress at the overlap ends; peel is much weaker than shear and often governs.
- Hart-Smith's elastic-plastic model treats the adhesive as bilinear; the strength is limited by its shear strain energy capacity and the adherend strength.

## Design rules
1. Prefer double-lap, scarf or stepped-lap joints over single lap for primary load.
2. Taper adherend ends to reduce peel.
3. Do not use bonding alone for primary structure where the regulator expects mechanical backup; confirm with the authority and the certification basis.
4. Verify adhesive thickness range and fillet.
5. Surface preparation and process control dominate real strength: abrasion, cleaning, anodising or primer for metal, peel-ply for composite, control of time between prep and bond.

## Tests
ASTM D1002 gives single-lap shear coupons for comparison of adhesive and surface prep; it does not give design allowables. Thick-adherend and peel tests give more design-relevant data.

## Gotchas
- A disbond can grow undetected; plan inspections or crack-stoppers.
- Hot-wet cycles reduce the adhesive strength.

## Verify
- [ ] The analysis shows the adherends fail before the adhesive at the design load.
