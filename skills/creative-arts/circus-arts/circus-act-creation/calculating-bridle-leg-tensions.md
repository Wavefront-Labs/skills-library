---
id: creative-arts.circus-arts.circus-act-creation.calculating-bridle-leg-tensions
name: calculating-bridle-leg-tensions
category: creative-arts
field: circus-arts
product: circus-act-creation
tags: [circus-act-creation, circus-arts, rigging-load-calculation, rigging-math, bridle-math, bridle-leg-tension, bridle-angle, horizontal-force, arena-rigging, aerial-point]
level: advanced
status: draft
description: "Calculate two-leg bridle tensions for an aerial point: symmetric and asymmetric formulas, the 120-degree rule, horizontal forces, worked example."
sources: ["Harry Donovan, Entertainment Rigging (2002) - bridle calculations", "ETCP Certified Rigger - Arena candidate handbook (rigging math content) - https://etcp.esta.org", "Jay O. Glerum, Stage Rigging Handbook (3rd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calculating bridle leg tensions

**Goal:** know the load in each leg and on each beam point when an aerial apparatus hangs
from a bridle (two slings from two beam points meeting at an apex), so every component
can be rated correctly. Always have a qualified rigger check the final numbers.

## Symbols
W = load at the apex (use the dynamic peak, not body weight - see dynamic load factors).
H = vertical distance from the apex up to the beams (same beam height both sides).
D1, D2 = horizontal distances from the apex to beam point 1 and 2.
L1, L2 = leg lengths: L = sqrt(D^2 + H^2).

## Formulas (beams at equal height)
- Vertical load on each beam point:
  V1 = W x D2 / (D1 + D2)      V2 = W x D1 / (D1 + D2)
  (the point **closer** to the apex takes **more** load).
- Leg tensions:
  T1 = V1 x L1 / H             T2 = V2 x L2 / H
- Horizontal force pulling the beam points towards each other:
  F_h = V1 x D1 / H  (= V2 x D2 / H)

## Symmetric bridle quick rules
T = (W / 2) x (L / H). By included angle between the legs:
- 60 degrees: each leg about 58% of W.
- 90 degrees: about 71%.
- 120 degrees: **100%** - each leg carries the full load. Riggers treat 120 degrees as the
  maximum included angle.
- Beyond 120 degrees leg tensions climb steeply.

## Worked example
Duo lyra, design peak W = 8.5 kN. Beams 6 m apart, apex 2 m left of centre (D1 = 1 m,
D2 = 5 m), H = 2 m.
- V1 = 8.5 x 5/6 = 7.08 kN; V2 = 8.5 x 1/6 = 1.42 kN.
- L1 = sqrt(1 + 4) = 2.24 m; L2 = sqrt(25 + 4) = 5.39 m.
- T1 = 7.08 x 2.24 / 2 = 7.93 kN; T2 = 1.42 x 5.39 / 2 = 3.83 kN.
- F_h = 7.08 x 1 / 2 = 3.54 kN.
Point 1 must be rated for 7.08 kN vertical plus the horizontal pull; leg 1 hardware for
7.93 kN at its working load limit.

## Gotchas
- Beams at different heights change the geometry; use the full 3D method or software.
- Short legs (small H) dramatically increase tension. Raise the apex height if you can.
- Swinging apparatus moves the apex and changes the split; check the extremes.

## Verify
- [ ] V1 + V2 = W (check your arithmetic).
- [ ] Included angle at or under 120 degrees.
- [ ] Each leg's hardware WLL at or above its calculated tension.
