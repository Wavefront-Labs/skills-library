---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.advanced-high-strength-steel-selection
name: advanced-high-strength-steel-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [ahss, advanced-high-strength-steel, dual-phase, dp-steel, trip-steel, martensitic-steel, complex-phase, crash-materials, steel-selection, springback, hole-expansion]
level: practitioner
status: gated
description: "Select AHSS for crash structures: DP, TRIP, CP, martensitic grades, strength-formability trade-offs, edge cracking, springback, welding and zone placement."
sources:
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "Steel supplier and worldsteel AHSS application guidelines (https://www.worldautosteel.org); confirm current guidelines"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Advanced high-strength steel selection

Strength ranges per family are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Families
Naming convention: grade abbreviations followed by minimum tensile strength in MPa (for example DP780); suppliers and standards use slightly different conventions, so check the specification.
- **Dual phase (DP):** ferrite plus martensite; good strength and work hardening; common for rails, cross-members and reinforcements from about 590 to 1180 MPa.
- **TRIP:** retained austenite transforms during deformation; high elongation for a given strength; good energy absorption in complex parts.
- **Complex phase (CP) and ferritic-bainitic:** higher yield ratio, better hole expansion and edge stretch; used for parts with flanging.
- **Martensitic (MS):** very high strength (about 1200-1500 MPa), low elongation; roll-formed bumper beams and door intrusion beams.
- **Press-hardened (hot-stamped) steel:** see hot stamping skill.

## 2. Selection logic
1. Identify the function: energy absorption zone (needs ductility and progressive folding) versus intrusion-resistant zone (needs high strength). Fine-tune by position: crush rails and crash boxes use ductile grades; A-pillar, B-pillar, sill and roof rail reinforcements use ultra-high strength.
2. Check the forming process: draw, stretch, flange, bend or roll-form; use forming limit curves, hole-expansion ratio, and bending (VDA 238-100 bending test) data from the supplier.
3. Gauge reduction: a stronger grade lets thickness fall for the same load-bearing strength, but stiffness depends on geometry and modulus, not strength; check stiffness separately.
4. Cost and supply: tooling wear, press tonnage, and coating (galvanised, galvannealed) availability.

## 3. Manufacturing issues
- **Springback** grows with strength: compensate in die design (simulation-based springback compensation), use stretch forming or restrike.
- **Edge cracking** after shear cutting: use laser cut, milled or reamed edges, or higher hole-expansion grades; keep consistent clearance.
- **Welding:** spot weld HAZ softening and lower nugget ductility at high strength; weld schedules and electrode wear need development; some very high strength steels need a prolonged hold or tempering pulse.
- **Delayed cracking** (hydrogen) in ultra-high strength steel at cut edges and in service on very high strength parts; follow supplier guidance.

## 4. Crash data
Material cards with strain-rate and failure (see material cards), component three-point bend and axial crush tests. Do not extrapolate from lower-strength grades.

## Verify
- [ ] Each zone's function (absorb or resist) matched to grade ductility.
- [ ] Forming, springback and edge-cracking assessed from supplier data.
- [ ] Welding schedule validated, including HAZ strength in crash CAE.
- [ ] Stiffness verified separately from strength.
