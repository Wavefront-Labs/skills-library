---
id: manufacturing-production.metal-plastics-fabrication-production.scientific-moulding.decoupled-moulding-process-studies
name: decoupled-moulding-process-studies
category: manufacturing-production
field: metal-plastics-fabrication-production
product: scientific-moulding
tags: [scientific-moulding, scientific-molding, decoupled-moulding, decoupled-molding, rjg, viscosity-curve, relative-viscosity, in-mould-rheology, cavity-balance, pressure-drop-study, gate-seal-study, gate-freeze, cooling-study, process-window, doe, cavity-pressure, cavity-pressure-sensor, intensification-ratio, transfer-position, fill-only, 95-percent-full, injection-moulding, injection-molding, process-validation, iq-oq-pq]
level: advanced
status: draft
description: "Develop a robust moulding process with the standard studies: fill-only shots, viscosity curve, cavity balance, pressure drop, gate-seal and cooling studies, then a process window."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decoupled moulding process studies

**Goal:** a process derived from data about *this* mould and material, where filling,
packing and cooling are controlled separately ("decoupled"), so normal variation in
viscosity doesn't move the part. Output is a documented process sheet with a window,
not a set of numbers that happened to work.

## 0. Prerequisites
Material dried and verified, mould temperatures at setpoint with water circuits as
designed, machine calibrated (velocity linearity matters), and the **intensification
ratio** of the machine known so you can convert hydraulic to plastic pressure.

## 1. Fill-only (first stage) set-up
Set hold pressure/time to (near) zero. Inject fast with velocity control and pick a
**transfer position** that fills parts to roughly **95–98 %** — short, but nearly full.
The machine must not hit its pressure limit during fill (if it does, you are
pressure-limited and not truly velocity controlled).

## 2. Viscosity (rheology) curve
Run fill-only shots at a series of injection velocities, low to max. For each, record
fill time and peak injection pressure; compute **relative viscosity** =
peak plastic pressure × fill time (in practice: pressure × intensification ratio × time).
Plot viscosity vs shear rate proxy (1/fill time). Choose a velocity on the **flat part**
of the curve, where viscosity barely changes with speed — that is where lot-to-lot
viscosity variation affects fill least.

## 3. Cavity balance (multi-cavity)
At the chosen velocity, take short shots well before full (e.g. ~50–90 %) and weigh
each cavity. Imbalance beyond the site's limit (commonly quoted as within a few
percent) points at runner/hot-runner/gate issues — fix the tool or hot-runner zones,
don't hide it with hold pressure.

## 4. Pressure-drop study
Short shots that stop at the end of sprue, runner, gate and part, recording peak
pressure at each. If the total is near the machine maximum, there's no reserve to
compensate for variation — address gating/runner or machine selection.

## 5. Second stage: hold (pack) pressure
With transfer set, add hold pressure in steps; check appearance and dimensions. Pick
a pressure inside a range that gives good parts, not at the edge.

## 6. Gate-seal (gate freeze) study
Increase hold time in steps (e.g. 0.5–1 s), weighing parts (runner removed) at each.
Part weight rises then plateaus when the gate freezes. Set hold time at the plateau
**plus a margin** (a common rule is ~1–2 s or a small %) so normal variation doesn't
unseal it. Hot-runner valve gates behave differently — gate close is timed instead.

## 7. Cooling study
Reduce cooling time stepwise while measuring CTQ dimensions/warp after stabilisation.
Choose the shortest time where dimensions are stable — this is where cycle time is won.

## 8. Process window / DOE
Vary the key factors (e.g. melt temp, hold pressure, mould temp) at high/low levels
in a DOE; measure CTQs. Confirm all corners make good parts; record the window on
the process sheet. Feeds IQ/OQ/PQ validation in regulated (medical) moulding.

## Cavity pressure monitoring
In-mould pressure sensors (RJG eDART and similar) let you transfer on cavity pressure
and sort parts automatically by pressure curve — the strongest form of decoupled
control. Place sensors near the gate and at end-of-fill.

## Gotchas
- Using machine "hydraulic" pressure as if it were plastic pressure across different
  presses — always convert by intensification ratio when transferring a process.
- Transfer by position assumes a stable check ring; check cushion repeatability first.
- Studies on an un-stabilised mould (still heating) give garbage — run 15+ min first.

## Verify
- [ ] Fill velocity on the flat region of the viscosity curve.
- [ ] Cavity balance within limit; pressure drop leaves reserve.
- [ ] Hold time above gate-freeze plateau with margin.
- [ ] Window DOE corners all produce conforming CTQs; documented on the process sheet.

*Draft: percentages and margins are commonly taught values (e.g. RJG-style training)
paraphrased from memory; confirm against your site's method.*
