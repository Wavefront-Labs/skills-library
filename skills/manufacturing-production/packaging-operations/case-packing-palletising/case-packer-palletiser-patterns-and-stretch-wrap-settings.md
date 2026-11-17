---
id: manufacturing-production.packaging-operations.case-packing-palletising.case-packer-palletiser-patterns-and-stretch-wrap-settings
name: case-packer-palletiser-patterns-and-stretch-wrap-settings
category: manufacturing-production
field: packaging-operations
product: case-packing-palletising
tags: [case-packing-palletising, packaging-operations, end-of-line, case-erector, case-packer, case-sealer, hot-melt, carton-tape, palletiser, palletizer, robotic-palletiser, layer-palletiser, pallet-pattern, interlocking, column-stack, tie-sheet, slip-sheet, overhang, stretch-wrapper, stretch-film, pre-stretch, containment-force, film-wraps, pallet-stability, pallet-quality, sscc-label, euro-pallet, gma-pallet]
level: practitioner
status: draft
description: "Set up end-of-line packing: case erector and sealer checks, column vs interlock pallet patterns, no overhang, and stretch-wrap pre-stretch, wraps and containment force."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Case packer, palletiser patterns and stretch-wrap settings

**Goal:** cases that are square, full and sealed, built into pallets that arrive at the
customer upright and undamaged. Most transit damage is decided here, in the pattern
and wrap settings.

## 1. Case erecting and packing
- **Blanks:** store flat, dry and at room conditions; damp or warped corrugated jams the
  erector and gives weak cases. Load the magazine the right way up (printing, flap
  direction).
- **Squareness:** an out-of-square case jams the packer and stacks badly. Check the
  forming section and flap folders.
- **Sealing:** hot-melt glue needs the right temperature, bead pattern and **compression
  time**; test by tearing a flap — fibre tear across the glue line means a good bond,
  clean separation means it failed (cold glue, too little, dusty board). Tape sealers:
  centred tape with enough leg length onto the sides.
- **Count/fill check:** an under-filled case is a short shipment; many lines weigh
  cases on a checkweigher.

## 2. Pallet patterns
Start from the customer's spec (pallet type, max height, max weight, pattern, labels).
- **Column stacking** (cases directly on top of each other): uses the full compression
  strength of the case corners — best for **strength**, but columns can lean and
  separate, so needs good wrapping (and sometimes corner boards or tie sheets).
- **Interlocking** (each layer rotated/brick pattern): ties layers together — better
  **stability**, but loses a large share of stack strength (often quoted at roughly
  40–50%; treat as indicative) because corners no longer line up.
- Many loads compromise: column-stacked lower layers with an interlocked or
  tie-sheeted top.
- **No overhang.** Cases hanging over the pallet edge lose much of their compression
  strength and get crushed; small underhang is acceptable.
- **Footprint:** know the pallet (e.g. 1200×1000 or 1200×800 mm Euro pallet in Europe,
  48×40 in GMA in the US). Pattern software from the palletiser maker or packaging
  designers calculates cube efficiency and orientation.

## 3. Programming a palletiser pattern
- Robot palletisers: define case dimensions, pallet size, layer pattern, label-out
  orientation (labels facing outward where the customer asks), tie/slip sheet
  layers, and pick/place offsets. Run the first pallet slowly and watch each layer.
- Layer (conventional) palletisers: row-forming turners and pushers make each layer;
  turning-device timing and case friction cause most mis-formed layers.
- Keep safety fencing, light curtains and pallet-exit interlocks intact; the robot
  cell is a no-entry zone while in auto.

## 4. Stretch wrapping
- **Pre-stretch:** powered pre-stretch rollers stretch film before it reaches the
  load (commonly 150–300%, depending on film). More pre-stretch = less film used, but
  past the film's limit it tears or loses strength — use the film supplier's figure.
- **Containment force** is what actually holds the load: a function of film
  thickness, pre-stretch, number of wraps and wrap force (tension from the carriage
  to the load). Measure it with a containment-force tool against a target for your
  load type, rather than guessing from wrap count.
- **Wrap pattern:** extra wraps at the **bottom** to lock the load to the pallet
  (film should reach a few cm onto the pallet deck), overlap between spirals (often
  ~50%), extra wraps at the top. A top sheet helps with dust and water.
- Wrap force too high crushes corners or pulls light loads over; too low and the load
  shifts in transit.

## 5. Pallet quality check
Before release: correct pattern and height, no overhang, no damaged cases, film
secure to the pallet, label(s) — usually a GS1 **SSCC** pallet label — on the
specified sides and scannable, and the pallet itself undamaged.

## Verify
- [ ] Case glue shows fibre tear; cases square and full.
- [ ] Pattern matches the customer spec; no overhang.
- [ ] Containment force within target; film anchored to the pallet base.
- [ ] Labels present on required faces and scannable.
- [ ] A test pallet passed a tilt or transit test if the load is new.

*Uncertain: interlock strength loss and pre-stretch ranges are rules of thumb; verify
with case/film suppliers or transit testing (e.g. ISTA procedures).*
