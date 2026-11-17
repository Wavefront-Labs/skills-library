---
id: agriculture-environment.crop-farming.tractor-implements.hitching-ballasting-and-drill-calibration
name: hitching-ballasting-and-drill-calibration
category: agriculture-environment
field: crop-farming
product: tractor-implements
tags: [tractor-implements, tractor, three-point-hitch, 3-point-linkage, top-link, lower-links, sway-chains, stabilisers, drawbar, pto, pto-shaft, ballast, ballasting, wheel-slip, tyre-pressure, front-weights, seed-drill, air-seeder, drill-calibration, calibration-test, turn-test, fertiliser-spreader, spreader-tray-test, cultivator, disc-harrow, tillage-depth, field-setup, farm-machinery]
level: practitioner
status: gated
description: "Set up a tractor and implement: safe three-point and drawbar hitching, ballast and tyre pressure by wheel slip, PTO shaft checks, a drill calibration test and levelling tillage gear in the field."
sources: ["https://tractortestlab.unl.edu/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hitching, ballasting and drill calibration

**Goal:** the implement works at the right depth and rate, the tractor puts power down
without wasting fuel in slip or compaction, and nobody gets crushed between tractor
and implement. Always read the tractor and implement operator's manuals — numbers
below are typical, not universal. (Sizing tractor to implement is covered in
`engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.tractor-implement-matching`.)

## 1. Hitching safely
- Nobody stands between the tractor and the implement while the tractor moves. Reverse
  slowly, stop, **handbrake on, engine off (or neutral + PTO off) before getting off** to
  connect.
- **Three-point linkage:** match category (Cat 1/2/3 pins and ball sizes). Connect
  lower links first (left, then right using the levelling crank), then the top link.
  Fit linch pins/clips on every pin.
- **Top link length** sets the implement's pitch: adjust so the frame is level fore-
  and-aft at working depth (ploughs and cultivators often slightly nose-down to bite;
  check the manual).
- **Lower-link levelling** (side to side) with the right-hand lift-rod crank; check with a
  spirit level or by measuring both sides to the ground.
- **Sway** (stabilisers/check chains): locked for mounted implements that must not swing
  (drills, sprayers, mowers in transport); allowed some float for ploughs and some
  cultivators as per the manual.
- **Drawbar:** set the drawbar height and length the implement specifies (PTO
  implements need a set distance from PTO shaft to hitch point to keep joint angles
  within limits). Safety chain fitted. Hydraulic hoses: clean couplers, matched
  colours/labels, hoses routed away from the PTO.
- **PTO shaft:** correct length — enough overlap when fully extended (at least about
  a third of tube length is a common rule), not bottoming out when shortest (lift the
  implement through its full range slowly). Guards and guard chains fitted. Match PTO
  speed (540 vs 1000 rpm). Never step over a turning shaft.

## 2. Ballast and tyres
- Purpose: enough weight to transmit pull, with acceptable **wheel slip**.
- Measure slip (many tractors display it; or mark a tyre and count rotations over a
  fixed distance loaded vs unloaded):
  `slip % = (distance unloaded − distance loaded) ÷ distance unloaded × 100`.
- Typical efficient targets in tillage/heavy draft: around **8–15%** (gated: unconfirmed, source is paywalled or blocked) for 4WD/MFWD on
  firm soil (slightly lower on concrete-like surfaces, a little higher on soft soils).
  Less than ~5% under heavy draft (gated: unconfirmed, source is paywalled or blocked) usually means over-ballasted (wasted fuel,
  compaction); more than ~15–20% means add ballast or reduce draft (gated: unconfirmed, source is paywalled or blocked).
- Weight split: commonly ~55–60% front / 40–45% rear (gated: unconfirmed, source is paywalled or blocked) for MFWD pulling drawbar loads,
  heavier rear for mounted rear implements, plus front weights to keep steering
  weight (ensure the front axle keeps enough load — often ≥ 20% of total (gated: unconfirmed, source is paywalled or blocked) — with a
  heavy rear-mounted implement lifted).
- **Tyre pressure:** set to the load and speed per the tyre maker's load table; lower
  pressures in the field (bigger footprint, less compaction), higher for road. Central
  tyre inflation systems make this easy.
- Remove ballast for light work.

## 3. Drill / air seeder calibration test
1. Fill the bin with the actual seed lot (TSW differs between lots).
2. Set the metering rate per the chart as a starting point.
3. Disconnect/collect from the outlets (calibration tray or bags).
4. Turn the drive wheel/calibration crank a number of turns equal to a known area:
   `area (ha) = turns × wheel circumference (m) × working width (m) ÷ 10,000`
   (account for wheel slip/tyre sink — some manuals add a slip factor). Electronically
   metered seeders have a "calibration" or "rate check" routine — run it.
5. Weigh the collected seed: `rate (kg/ha) = weight (kg) ÷ area (ha)`. Adjust and repeat
   until within ~2–3% of target (gated: unconfirmed, source is paywalled or blocked).
6. In the field, cross-check after a known area: kg used ÷ ha sown.

## 4. Spreaders and tillage in the field
- Fertiliser spreader: set from the chart for the product's density and particle size,
  then **tray test** across the spread width; check overlap pattern (CV% under ~15 (gated: unconfirmed, source is paywalled or blocked) is a
  common target).
- Tillage: set depth, level the frame, check after 50 m for even working depth and
  levelling at the rear; adjust gangs/tines so there's no ridge or furrow between passes.

## Verify
- [ ] Pins, clips, safety chain, hoses and PTO guards checked; nobody between tractor and implement.
- [ ] Implement level fore-aft and side-to-side at working depth.
- [ ] Wheel slip measured under working load and inside the target band; tyre pressures set from the load table.
- [ ] Drill calibration within ~3% of target, cross-checked by area sown.
- [ ] Spreader or tillage pattern checked in the first run.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; machinery craft.
- Confirmed against: the drill calibration arithmetic was recomputed (area ha = turns x wheel circumference m x width m / 10,000) and the slip formula is the standard definition.
- Not confirmed: the target slip range, front/rear weight split, minimum front axle load, spreader CV limit and calibration tolerance (no free primary source reached).

Method: documentation only; no commands were run.
