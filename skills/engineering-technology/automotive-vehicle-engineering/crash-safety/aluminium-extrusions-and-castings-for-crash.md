---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.aluminium-extrusions-and-castings-for-crash
name: aluminium-extrusions-and-castings-for-crash
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [aluminium-crash, aluminium-extrusion, crash-box, high-pressure-die-casting, hpdc, casting-ductility, spr, flow-drill-screw, galvanic-corrosion, crash-materials, 6xxx]
level: practitioner
status: gated
description: "Use aluminium extrusions and castings in crash structures: crash can design, 6xxx temper and ductility, HPDC casting limits, joining, galvanic corrosion, and tests."
sources:
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "Huang, Vehicle Crash Mechanics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Aluminium extrusions and castings for crash

Alloy and temper statements are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Extrusions
- **Alloys:** 6xxx series (Al-Mg-Si, such as 6060, 6063, 6082 types) are common for crash cans, bumper beams, sills and battery frames. Temper (T4, T5, T6, T7) sets strength and ductility; overaged tempers (T7 type) trade strength for better crush ductility. Confirm exact alloy and temper with the extruder.
- **Crash can behaviour:** a multi-cell or round tube folds progressively when crushed axially; wall thickness, section size and a trigger (chamfer or bead) set the mean crush force and onset peak. Specific energy absorption of aluminium extrusions is attractive relative to mass; confirm with tests.
- **Bending crush:** thin-wall sections can crack at hinge lines; ductility test (three-point bend, VDA 238-100 style) screens the lot.
- **Process effects:** extrusion seams, grain structure at the surface, and recrystallised layers affect fracture; weld seams from porthole dies need qualification.

## 2. Castings
High-pressure die cast (HPDC) alloys (Al-Si-Mg types such as AlSi10MnMg) give complex integrated nodes and large structural castings (shock towers, rear underbody). Ductility is lower and more scattered than wrought and depends on porosity, section thickness and heat treatment (T7 or similar for crash zones, or as-cast low-iron alloys). Use vacuum-assisted casting and X-ray inspection; define acceptance (porosity grade, mechanical property from cut specimens). Large castings change repairability and crash load path design.

## 3. Joining
Self-piercing rivets (SPR), flow-drill screws, clinching, structural adhesives (with or without rivets), and laser or MIG welding for compatible grades. Spot welding of aluminium needs specialised equipment. Hybrid joints with steel need isolation against galvanic corrosion (coating, adhesive layer, isolating washers).

## 4. Modelling
Material cards with strain-rate effect (aluminium is much less rate-sensitive than mild steel but check temper), anisotropy for extrusions, and fracture models that account for casting thickness; correlate with component crush tests and rivet joint coupons.

## 5. Tests
Axial crush with quasi-static and dynamic loading, three-point bend, rivet strength coupons, casting tensile coupons from the actual part, corrosion tests.

## Verify
- [ ] Alloy, temper and process agreed with supplier; ductility test per lot.
- [ ] Casting acceptance criteria and inspection plan defined.
- [ ] Joint strength and corrosion protection validated.
- [ ] Crash CAE calibrated on component tests with the real material.
