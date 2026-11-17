---
id: manufacturing-production.electronics-semiconductor-manufacturing.ic-packaging-test.wire-bond-setup-and-pull-shear-testing
name: wire-bond-setup-and-pull-shear-testing
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: ic-packaging-test
tags: [ic-packaging-test, wire-bonding, ball-bond, wedge-bond, gold-wire, copper-wire, kns, kulicke-soffa, asm-pacific, capillary, efo, free-air-ball, bond-pull-test, wire-pull, ball-shear, mil-std-883, jesd22-b116, intermetallic, nsop, non-stick-on-pad, nsol, cratering, bond-parameters, ultrasonic, back-end, osat, assembly-test, semiconductor]
level: practitioner
status: draft
description: "Set up and buy off a ball wire bonder: capillary and wire checks, free-air ball, bond parameters, then destructive pull and ball-shear tests and how to read failure modes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wire bond setup and pull/shear testing

**Goal:** a bonder that makes reliable first (ball) and second (stitch) bonds on this
device, proven by pull and shear tests *before* production — and a failure-mode
vocabulary to tell a parameter problem from a contamination or die problem.

## 1. Setup checklist
- **Wire**: type (Au, Cu, Pd-coated Cu, Ag alloy), diameter and lot per the bonding
  diagram. Copper wire needs forming gas (N₂/H₂) at the EFO to stop ball oxidation —
  check flow.
- **Capillary**: part number matches the program; check usage count against its life
  limit (bond count) and inspect the tip for build-up or chipping.
- **Program**: bonding diagram (pad-to-lead map), loop profiles, device revision.
- **Heater block / workholder** temperature correct for the leadframe/substrate;
  clamps holding the leads flat — bouncing leads give weak stitches.
- Teach/verify **PR (pattern recognition)** references for die and leads.

## 2. Free-air ball (FAB)
The EFO spark melts the wire tail into a ball. Check FAB diameter and shape on the
first bonds: off-centre "golf club" or pointed balls → EFO gap, tail length or gas flow.
FAB size drives the squashed-ball diameter on the pad.

## 3. Bond parameters
Main levers per bond: **force, ultrasonic power, time, temperature** (plus impact/contact
velocity). Typical tuning:
- Squashed ball diameter and height within the spec (measured optically/SEM).
- Too little energy → non-stick on pad (NSOP) or weak shear.
- Too much → pad **cratering** (damage under the pad), splash of pad metal, or
  ball lift with silicon attached.
- Stitch: enough to give a good "crescent" with no heel cracks; heel cracks show as
  low pull with breaks at the heel.
Use a DOE on a few parameters rather than one-at-a-time drift; save the qualified
window.

## 4. Destructive testing
- **Wire pull test**: hook under the loop near mid-span (or per the spec location),
  pull to failure, record force (gf/cN) and **failure mode**:
  | Code (typical) | Where it broke | Meaning |
  |---|---|---|
  | Wire break mid-span | wire | Good — bonds stronger than wire |
  | Neck break above ball | ball neck | Acceptable if force OK; low force → heat-affected zone/looping damage |
  | Ball lift | ball/pad interface | Bad — weak bond, contamination, low energy |
  | Heel break | stitch heel | Acceptable if force OK; low → stitch damage |
  | Stitch lift | stitch/lead | Bad — lead contamination, clamping, plating |
  Minimum forces depend on wire diameter (MIL-STD-883 method 2011 gives a table;
  customer specs often tighter).
- **Ball shear test** (JESD22-B116): shear tool pushes the ball at a set height above
  the pad. Record force and mode; look for intermetallic coverage on the pad after shear
  (a gold ball on aluminium should leave substantial IMC; little coverage = weak bond).
- Sample at setup, after capillary change, after any parameter change, and per the
  in-process sampling plan.

## 5. In-process watch items
- NSOP/NSOL auto-stops rising → pad contamination (plasma clean before bond may be
  needed), wrong heater temp, capillary worn.
- Wire sweep after moulding comes from loop height/shape — coordinate with mould.
- Copper wire is harder: higher cratering risk on fragile low-k pads; use qualified
  recipes only.

## Verify
- [ ] Wire, capillary and program match the bonding diagram; capillary within life.
- [ ] FAB and squashed-ball geometry in spec.
- [ ] Pull forces above minimum with acceptable failure modes; no ball/stitch lifts.
- [ ] Shear forces and IMC coverage acceptable.
- [ ] Setup results logged before production release.

*Draft: failure-mode codes and minimum forces differ between MIL-STD-883, JEDEC and
customer specs; values not reproduced — look them up for your wire.*
