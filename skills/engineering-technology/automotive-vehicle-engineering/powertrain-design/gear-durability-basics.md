---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.gear-durability-basics
name: gear-durability-basics
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [gear-durability, gear-fatigue, iso-6336, agma-2001, tooth-bending, pitting, micropitting, case-hardened-steel, driveline-components, load-spectrum]
level: practitioner
status: gated
description: "Assess gear durability for transmissions: tooth bending and contact stress per ISO 6336 or AGMA, duty-cycle load spectra, Miner damage, materials and test."
sources:
  - "ISO 6336 (calculation of load capacity of spur and helical gears; confirm edition)"
  - "AGMA 2001 (fundamental rating factors for involute gear teeth; confirm edition)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Gear durability basics

## 1. Failure modes to design against
- **Tooth root bending fatigue:** cracking at the fillet; catastrophic.
- **Pitting / micropitting:** contact fatigue on flanks; progressive.
- **Scuffing / scoring:** lubricant film breakdown under heavy sliding.
- **Wear, tip breakage, case spalling.**

## 2. Rating method
Use a recognised standard: ISO 6336 (spur and helical) or AGMA 2001 for bending and contact (series scope, titles and current editions (gated: unconfirmed, source is paywalled or blocked); confirm the edition your company uses). Both start from nominal tangential load and apply factors (application/overload, dynamic, load distribution, geometry, material, life). Do not copy a factor from memory; implement from the standard edition your company uses, or use validated gear-calculation software.

## 3. Load spectrum
Road tests or CAE give torque vs time per gear. Count into bins (time at load per gear, or rainflow-style counting), then apply **Palmgren-Miner** linear damage: D = sum(n_i / N_i). Use a design target D below 1 with margin per your durability requirement (lifetime kilometres with a specified usage mix). Include abusive events (clutch drop, launch, hill start) as separate low-count events.

## 4. Geometry levers
- Larger module and face width and higher contact ratio helical gears reduce stress and noise.
- Profile and lead modifications (tip relief, crowning, helix correction) tuned for deflection under load centre the contact and cut transmission error and whine.
- Root fillet radius and shot peening raise bending life.

## 5. Material and heat treatment
Case-hardened alloy steels are typical for automotive gears; core hardness, case depth, retained austenite and steel cleanliness drive life. Superfinishing reduces micropitting; lubricant selection (viscosity grade, additives) and temperature matter.

## 6. Validate
Bench tests: back-to-back or power-recirculating rigs at accelerated load; pitting tests with inspection intervals; contact pattern under load; teardown and flank inspection. Link transmission error to gear whine (see gear whine skill).

## Verify
- [ ] Standard and edition recorded; calculation reviewed by a gear specialist.
- [ ] Load spectrum from measured data, including abuse cases.
- [ ] Micropitting and scuffing checked, not only bending and pitting.
- [ ] Contact pattern verified under load.
