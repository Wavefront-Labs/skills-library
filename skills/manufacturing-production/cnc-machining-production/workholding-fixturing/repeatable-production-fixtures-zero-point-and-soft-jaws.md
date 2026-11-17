---
id: manufacturing-production.cnc-machining-production.workholding-fixturing.repeatable-production-fixtures-zero-point-and-soft-jaws
name: repeatable-production-fixtures-zero-point-and-soft-jaws
category: manufacturing-production
field: cnc-machining-production
product: workholding-fixturing
tags: [workholding-fixturing, workholding, fixturing, fixture-design, 3-2-1-locating, 3-2-1-principle, locators, datum-scheme, clamping, clamping-force, vice, vise, machine-vice, soft-jaws, chuck, collet, zero-point-clamping, zero-point-system, quick-change-pallet, tombstone, fixture-plate, dowel-pins, diamond-pin, part-distortion, thin-wall, clamping-distortion, dovetail-workholding, vacuum-fixture, setup-reduction, smed, cnc-machining-production]
level: practitioner
status: draft
description: "Hold production parts repeatably: 3-2-1 locating on the drawing datums, clamping against locators, soft jaws, zero-point systems for fast changeovers, and controlling clamping distortion."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Repeatable production fixtures, zero-point systems and soft jaws

**Goal:** every part sits in the same place to within microns, the setup changes in
minutes, and the clamping doesn't bend the part out of tolerance.

*Draft: practical principles; clamp force numbers must come from the clamp maker
and a cutting-force estimate for your operation.*

## 1. Locate first, then clamp
- **3-2-1 principle:** 3 points on the primary datum plane, 2 on the secondary, 1 on
  the tertiary — six contacts constrain six degrees of freedom. More contacts on a
  rough surface over-constrain and rock.
- **Locate on the drawing datums** (or on surfaces already machined to them) so the
  fixture doesn't add tolerance stack-up between datum and feature.
- **Clamp towards the locators**, never away from them, and opposite to the cutting
  forces where possible (cutting forces push the part *into* locators, not off them).
- Clamps over supports: clamping where there's no support underneath bends the part.
- For holes: one **round pin** and one **diamond (relieved) pin** — two round pins
  jam on hole-spacing tolerance.

## 2. Vices and soft jaws
- A good machine vice gives repeatability if the fixed jaw is trammed/indicated and the
  part sits against the same stop every time (a side stop on the fixed jaw).
- **Soft jaws** machined in place to the part profile give full contact and locate
  odd shapes. Machine them **clamped on a spacer** of roughly the part width at
  production clamping pressure, so jaws are in their working position when cut.
- Mark jaw sets with part number and op; store with the setup sheet.
- For lathes: bore soft jaws with a **boring ring** or plug gripped at production
  pressure. Same rule — cut them as they will be used.

## 3. Zero-point clamping for changeovers
- **Zero-point systems** (receivers in the table, pull studs on pallets/fixtures)
  locate and clamp with repeatability typically within a few microns, so the work offset
  of a fixture stays valid every time it goes back on the machine.
- Benefits: fixtures set up **offline** (on a bench or a second receiver) while the machine
  runs (SMED: move setup from internal to external time).
- Record each fixture's work offset relative to the receiver on its setup sheet; with a
  common grid, offsets transfer between identical machines.
- Keep receivers clean — chips under a pull stud destroy repeatability. Air blast-off and
  covers when empty.

## 4. Multi-part and tombstone fixtures
- More parts per cycle reduce tool changes per part and allow longer unattended runs.
- Balance clamp access with tool reach — tall tombstones need long tools on top rows.

## 5. Distortion control
- **Clamping distortion:** thin parts clamped hard are machined flat, then spring back
  when released. Reduce clamp pressure for the finishing pass (programmable hydraulics,
  or a stop for the operator to loosen and re-snug).
- **Residual stress:** rough all over, release, let it relax, then finish. Leave even stock.
- **Dovetail workholding** on a small machined dovetail uses very little stock to hold
  for 5-axis access, with low clamping deformation.
- **Vacuum fixtures** for thin plates — check holding force against cutting forces
  (vacuum force = pressure × sealed area) and plan for seal leaks.

## 6. Proving a fixture
- Load the same part 5–10 times, probe/indicate a feature each time: the spread is the
  fixture's repeatability. Compare to the tolerance (aim for a small fraction of it).
- Error-proof (poka-yoke): a pin or shape that makes loading a part backwards impossible.

## Gotchas
- Chips on locators: design self-cleaning locators (small pads, air blast) and chip escape.
- Hydraulic fixtures lose pressure overnight — pressure monitoring for unattended runs.
- A fixture that only one setter can load correctly isn't a production fixture.

## Verify
- [ ] Locators on drawing datums, 3-2-1, clamps pushing into locators.
- [ ] Repeatability test done and well inside tolerance.
- [ ] Soft jaws cut at production pressure and labelled.
- [ ] Zero-point offsets recorded on the setup sheet.
- [ ] Part flat/round in tolerance after unclamping.
