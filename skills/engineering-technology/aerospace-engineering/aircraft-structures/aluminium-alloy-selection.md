---
id: engineering-technology.aerospace-engineering.aircraft-structures.aluminium-alloy-selection
name: aluminium-alloy-selection
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aluminium-alloys, aluminum-alloys, 2024, 7075, 7050, alloy-selection, aerospace-materials]
level: practitioner
status: verified
description: "Select wrought aluminium alloys and tempers for airframe components by strength, damage tolerance, corrosion and stock form, using common aerospace practice."
sources:
  - "MMPDS (aluminium alloy chapter)"
  - "Niu, Airframe Structural Design"
  - "Aluminum Association designation system"
  - "https://link.springer.com/article/10.1007/s11665-009-9554-z"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Aluminium alloy selection

**Goal:** an alloy and temper that fits the component's governing requirement.

## Common aerospace families
Alloy-to-application pairings below are common practice; a literature check supports 2524-T3 replacing 2024 on fuselage skins (for example the Boeing 777), 7050-T7451 as an incumbent thick-plate alloy and Al-Cu-Li alloys (2195, 2050) in tank, fuselage skin and spar uses; the other specifics (T73/T76 tradeoffs, 2219 cryogenic weldability, Alclad effects) are (gated: unconfirmed, source is paywalled or blocked).
- **2xxx (Al-Cu)**, for example 2024-T3: good fatigue and damage tolerance, used on fuselage skin and lower wing skins. 2524 is a damage-tolerant development used for fuselage skins.
- **7xxx (Al-Zn-Mg-Cu)**, for example 7075-T6 high strength; T73 and T76 tempers trade some strength for resistance to stress-corrosion and exfoliation; 7050-T7451 and 7055 for thick plate and extrusions with better through-thickness properties; used in upper wing skins and spars.
- **2219**: weldable and good at cryogenic temperatures, used for propellant tanks.
- **Al-Li alloys** (for example 2195, 2050): lower density and higher stiffness, with anisotropy and cost to manage.
- **Alclad** sheet has a thin pure-aluminium layer for corrosion protection and lowers fatigue and strength slightly.

## Selection checklist
1. Governing criterion: static strength (upper wing compression: 7xxx), fatigue and fracture (lower wing: 2xxx), corrosion, weldability, thermal exposure.
2. Stock form: sheet, plate, extrusion, forging; properties vary with thickness and direction (L, LT, ST).
3. Short-transverse properties for thick plate and forgings: check SCC and fracture toughness.
4. Use design allowables from MMPDS for the exact alloy, temper, form and thickness; do not use typical values.
5. Define surface treatments: anodise, primer, sealant, galvanic isolation.

## Gotchas
- The same alloy has different allowables in different thicknesses and grain directions.
- Elevated-temperature exposure degrades T6 tempers.
- Check the current designation: tempers and specifications change, and suppliers' details vary.

## Verify
- [ ] Each component's drawing note names alloy, temper, form and specification.
