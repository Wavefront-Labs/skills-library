---
id: engineering-technology.structural-engineering.connection-design.bolted-shear-connection
name: bolted-shear-connection
category: engineering-technology
field: structural-engineering
product: connection-design
tags: [connection-design, steel-connection, bolted-connection, shear-connection, shear-tab, single-plate, fin-plate, double-angle, end-plate, bolt-shear, bearing, tearout, block-shear, fillet-weld, slip-critical, a325, a490, f3125, grade-8-8, aisc-360, aisc-manual, eurocode-3, en-1993-1-8, as-4100, coped-beam]
level: practitioner
status: verified
description: "Design bolted steel shear connections (single plate, double angle, end plate) to AISC 360: bolt shear, bearing, block shear, weld sizing and ductility checks."
sources:
  - "ANSI/AISC 360 Specification for Structural Steel Buildings (Chapter J)"
  - "AISC Steel Construction Manual (Parts 7, 8, 9, 10)"
  - "RCSC Specification for Structural Joints Using High-Strength Bolts"
  - "EN 1993-1-8 Eurocode 3 - Design of joints"
  - "SCI P358 Joints in Steel Construction - Simple Joints to Eurocode 3"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bolted shear connections — every limit state, plus the ductility check

**Goal:** a simple (pinned) beam-end connection that carries the factored reaction
through every limit state along the load path. It must also rotate enough to behave
as a pin, without the bolts or welds failing first.

Values are AISC 360-16/22 LRFD (US units). EC3 notes follow. The engineer of record
must confirm the governing edition. The AISC and Eurocode texts are paywalled or blocked (aisc.org PDF returned 403), so clause values below are unconfirmed against the standard (gated: unconfirmed, source is paywalled or blocked) unless marked computed. Group A Fnv 54/68 ksi was matched by a Dlubal FAQ citing Table J3.2; Group B 68/84 only by a third-party calculator.

## 1. Trace the load path
Beam web → bolts → plate or angles → weld (or bolts) → supporting member. Every
element and interface is a check: bolt shear, bearing and tearout on both plies,
plate shear yield and rupture, block shear (plate and coped beam web), weld, and the
supporting web (local punching shear on thin column or girder webs).

## 2. Bolts
- **Shear:** φRn = 0.75·Fnv·Ab per shear plane. Table J3.2 values:

  | Bolt group | Threads included (N) | Threads excluded (X) |
  |---|---|---|
  | Group A (A325 / F3125 Gr A325) | Fnv = 54 ksi | Fnv = 68 ksi |
  | Group B (A490) | Fnv = 68 ksi | Fnv = 84 ksi |

  Assume N unless you control the thread location.
- **Bearing and tearout (J3.10)**, with deformation at service a consideration:
  Rn = min(2.4·d·t·Fu, 1.2·lc·t·Fu) per bolt, φ = 0.75. lc is the clear distance to
  the edge or the next hole. Edge bolts usually govern through tearout.
- **Holes:** standard hole = d + 1/16 in. For net area, add another 1/16 in (B4.3).
- **Spacing:** minimum 2⅔d, with 3d preferred. 3 in (76 mm) pitch is the US standard.
  Take minimum edge distances from Table J3.4 (the 360-22 tables were revised, so
  check yours).
- **Slip-critical** (only where required: oversized or slotted holes parallel to load,
  fatigue, load reversal): φRn = φ·μ·Du·hf·Tb·ns. Use μ = 0.30 for Class A and 0.50
  for Class B surfaces, Du = 1.13, and φ = 1.00 for standard holes.

## 3. Plates, angles and block shear
- **Shear yielding:** φ = 1.00, Rn = 0.6·Fy·Agv.
- **Shear rupture:** φ = 0.75, Rn = 0.6·Fu·Anv.
- **Block shear (J4.3):** Rn = 0.6·Fu·Anv + Ubs·Fu·Ant ≤ 0.6·Fy·Agv + Ubs·Fu·Ant, with
  φ = 0.75 and Ubs = 1.0 for a single bolt row. Check it on the plate and on a coped
  beam web.
- **Coped beams:** check flexural yielding and local buckling at the cope (Manual
  Part 9).

## 4. Welds
- Fillet weld: φRn = 0.75 × 0.6·FEXX × 0.707w per unit length. For E70 that is about
  1.392 kip/in per sixteenth of leg size (computed: 0.75 × 0.6 × 70 × 0.707 / 16 = 1.392).
- Minimum size comes from the thinner part joined (Table J2.4). Check base-metal shear
  rupture on thin supports.
- **Ductility rule for shear tabs:** size the fillet welds on both sides to (5/8)·tp.
  The plate then yields before the weld ruptures. This is the Manual Part 10
  conventional single-plate requirement.

## 5. Single plate (shear tab): conventional configuration
The AISC Manual Part 10 conventional configuration (standard or short-slotted holes,
2–12 bolts, a limit on the distance from bolt line to weld, and plate or web
thickness limited to about d/2 + 1/16) lets you use tabulated eccentricities and skip
a plate flexure-buckling interaction. Outside those limits, use the extended
configuration. In that case design the bolt group for eccentricity with the
instantaneous-centre tables (Manual Part 7) and check the plate for flexure plus
shear, and buckling. The configuration limits above are paraphrased (gated: unconfirmed, source is paywalled or blocked); read the current Part 10 table before relying on them.

## 6. Eurocode 3 (EN 1993-1-8) equivalents
- **Bolt shear:** Fv,Rd = αv·fub·A/γM2, with γM2 = 1.25 recommended. αv = 0.6 for
  classes 4.6, 5.6 and 8.8, and 0.5 for 10.9 with threads in the shear plane (gated: unconfirmed, source is paywalled or blocked; confirm against EN 1993-1-8 Table 3.4).
- **Bearing:** Fb,Rd = k1·αb·fu·d·t/γM2.
- **Practical guidance:** SCI P358, Joints in steel construction: Simple joints to Eurocode 3 (2014 reprint; steelconstruction.info), gives standard fin-plate and end-plate resistance tables and procedures to EN 1993-1-8 and the UK National Annex.

## Verify
- [ ] The load path is traced and every interface has a check.
- [ ] Bolt shear, bearing and tearout are checked on all plies, with edge bolts by lc.
- [ ] Shear yield, shear rupture and block shear are checked on plates and coped beam webs.
- [ ] Welds are sized for strength and for the (5/8)·tp ductility rule where applicable.
- [ ] Eccentricity is handled per the conventional or extended method.
- [ ] Spacing and edge distances meet the governing table edition.
