---
id: engineering-technology.invention-prototyping.rapid-prototyping.fdm-sla-print-for-function
name: fdm-sla-print-for-function
category: engineering-technology
field: invention-prototyping
product: rapid-prototyping
tags: [invention-prototyping, rapid-prototyping, 3d-printing, additive-manufacturing, fdm, fff, sla, msla, resin-printing, sls, pla, petg, abs, asa, nylon, tpu, print-orientation, layer-adhesion, anisotropy, tolerances, clearance, heat-set-inserts, design-for-additive-manufacturing, dfam, slicer, prusaslicer, cura, orcaslicer, iteration, fixtures, jigs]
level: practitioner
status: draft
description: "Design and print functional FDM/SLA test parts: process choice, orientation for strength, tolerances and clearances, heat-set inserts, and fast iteration loops."
sources: ["Gibson, Rosen, Stucker & Khorasani, Additive Manufacturing Technologies (3rd ed.)", "Redwood, Schöffer & Garret, The 3D Printing Handbook (3D Hubs)", "ISO/ASTM 52900 additive manufacturing terminology", "PrusaSlicer and UltiMaker Cura documentation", "Filament and resin manufacturer technical data sheets"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print for function — FDM and SLA parts that survive testing

**Goal:** get a physical test article that answers a real question (fit, mechanism,
load, ergonomics) in hours, designed around how printers actually fail.

## 1. Choose the process by the question
| Question | Process | Why |
|---|---|---|
| Does it fit / move / mount? | FDM in PLA or PETG | Cheap, fast, easy to modify |
| Snap fits, hinges, impact | FDM PETG, nylon or ASA; or SLS nylon | Tougher, less brittle than PLA |
| Small detail, sealing faces, optics mock-up | SLA/MSLA resin | ~25–50 µm layers, smooth, near-isotropic |
| Flexible seal, grip, bumper | FDM TPU (Shore ~85–95A) | Prints rubbery parts directly |
| Warm environment (car, motor housing) | PETG, ASA, nylon or high-temp resin | PLA softens around 55–60 °C |
| Real load, many cycles | Outsource SLS/MJF nylon or machine it | FDM layer bonds are the weak point |

Standard resins are brittle and creep; use "tough" or "engineering" resins for clips.
Check the material data sheet — values vary a lot between brands.

## 2. Orient for the load, not for the looks
FDM parts are **anisotropic**: across the layers (Z) they are often only ~50–80% as
strong as in-plane, and fail by layer peel. So:
- Lay parts so bending stress runs **along** the layer lines (print a hook lying flat,
  not standing up).
- Snap-fit arms lie in the XY plane.
- Put the cosmetic face up or against the bed, never on the supported side.
- Minimise supports on functional surfaces; design 45° chamfers instead of flat overhangs.
SLA: tilt parts 15–45° to the build plate to reduce peel forces, and add drain holes to
hollow parts so trapped resin does not crack them later.

## 3. Design rules that save a reprint
Typical starting values for a tuned 0.4 mm nozzle FDM printer (calibrate yours):
- **Wall thickness:** multiples of line width, ≥ 1.2 mm (3 perimeters) for anything structural.
- **Sliding/rotating clearance:** 0.2–0.3 mm per side; press fit −0.05 to −0.1 mm,
  then test with a tolerance coupon.
- **Holes print undersize** (often 0.1–0.3 mm): model nominal and drill/ream, or add
  compensation in the slicer.
- **Bridges:** ≤ ~10–20 mm unsupported; **overhangs:** ≤ 45–50° from vertical.
- **Threads:** do not tap plastic for repeated assembly — use **heat-set brass inserts**
  (hole size from the insert maker, pressed in with a soldering iron at roughly the
  filament's print temperature) or captive hex-nut pockets.
- **Fillets** at load-carrying inside corners; sharp corners crack first.
- Strength comes mostly from **perimeters**, not infill: 4 walls at 20% infill usually beats
  2 walls at 60%.

## 4. Slicer settings for a functional part
- Layer height 0.2 mm (0.12–0.16 for fine fits), 4 perimeters, 5 top/bottom layers.
- Infill 15–40% gyroid or cubic; 100% only for small, highly loaded features.
- Raise nozzle temperature to the top of the material range for better layer bonding.
- Brim for ABS/ASA/nylon corners that lift; enclosure for ABS/ASA.
- Dry hygroscopic filament (nylon, TPU, PETG) before printing — wet filament pops and
  gives weak, stringy parts.

## 5. Iterate deliberately
1. Write down what the print must prove before slicing.
2. Print the **smallest section** that answers it — just the hinge, just the boss.
3. Print variants in one plate (three clearances, three wall counts) and label them
   in the model with embossed text.
4. Record material, settings and result next to the CAD revision.
5. Change one variable per iteration once the design is close.

## Gotchas
- Elephant's foot (first-layer flare) makes bottom faces oversize — chamfer bottom edges 0.5 mm.
- PLA creeps under sustained load even at room temperature; a clip that holds today may be
  loose next week.
- Uncured resin is a skin sensitiser: gloves, ventilation, full post-cure. Under-cured parts
  are weak and tacky.
- Printed strength numbers from a data sheet are for ideal test bars; your part will be lower.
- Do not judge final-product durability from a print — note what the test can and cannot tell you.

## Verify
- [ ] The print answers a question written down before slicing.
- [ ] Orientation puts the main stress along the layers, not across them.
- [ ] Clearances were confirmed with a test coupon on this printer and material.
- [ ] Threads use inserts or nuts, not tapped plastic, where assembly repeats.
- [ ] Material, settings and outcome are logged against the CAD revision.
