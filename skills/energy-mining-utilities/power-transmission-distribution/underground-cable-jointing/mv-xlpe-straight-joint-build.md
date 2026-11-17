---
id: energy-mining-utilities.power-transmission-distribution.underground-cable-jointing.mv-xlpe-straight-joint-build
name: mv-xlpe-straight-joint-build
category: energy-mining-utilities
field: power-transmission-distribution
product: underground-cable-jointing
tags: [underground-cable-jointing, cable-jointing, cable-jointer, cable-splicing, splicer, mv-cable, medium-voltage, 11kv, 22kv, 33kv, xlpe, epr, straight-joint, through-joint, heat-shrink, cold-shrink, stress-control, semicon, insulation-screen, conductor-screen, ferrule, mechanical-connector, shear-bolt, earth-screen-continuity, cable-identification, cable-spiking, spiking-gun, partial-discharge, vlf-test, cable-fault-location]
level: advanced
status: draft
description: "Build a medium-voltage XLPE straight joint that won't fail: identify and spike the cable, prepare screens and semicon cleanly, connector and stress control, screen continuity, testing."
sources:
  - "Heat-shrink and cold-shrink joint kit instructions from major accessory makers and utility jointing manuals, summarised in general terms; no kit-specific dimensions reproduced"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building an MV XLPE straight joint

**Goal:** join two lengths of single- or three-core XLPE medium-voltage cable so the
joint has no voids, no contamination and continuous screens. Most MV joint failures
trace back to preparation, not the kit. **The kit's instruction sheet and dimensions
always win** — every manufacturer's cutback lengths differ.

## 1. Prove you have the right cable
1. Confirm from records and on site (cable route, labels, tracing) which cable is yours.
2. Isolate and earth at both ends under your permit.
3. **Identify** the cable at the excavation with a signal-injection cable identifier
   (signal on at one end, polarity/strength confirmed on the target cable only).
4. **Spike it** with a remotely fired spiking gun from behind cover before any
   knife touches it. Spiking proves the cable is dead and earthed even if
   identification was wrong. Never skip it because "records are good".

## 2. Set up a clean workplace
- A jointing tent or shelter; dry conditions. Moisture and dust are joint killers.
- Hands and cloths clean; use the solvent the kit specifies (lint-free wipes).
- Lay out kit contents and check against the list; check shelf-life dates on
  cold-shrink parts and mastics.
- Straighten and overlap the cable ends, mark the centre, and cut square.

## 3. Prepare each cable end (in kit order)
1. Remove oversheath to the kit length; fold back or cut the metallic screen
   wires/tapes as instructed.
2. **Remove the insulation screen (semicon)** to its cutback line: score lightly with
   a dedicated tool, never cut into the insulation. The cut edge must be straight and
   smooth; a nick or a jagged step concentrates electrical stress.
3. Remove insulation to expose the conductor for the connector length plus any
   specified gap; chamfer the insulation edge if the kit calls for it.
4. **Clean the insulation from insulation toward semicon, never the other way** —
   wiping back over the semicon drags conductive carbon onto the insulation surface.
5. Remove any semicon residue; light abrasion with the specified cloth grit if the
   instructions allow, then a final solvent wipe.

## 4. Connector and stress control
- Fit the connector (compression ferrule with the matching die, or a shear-bolt
  connector tightened until the heads shear). File and clean burrs; any sharp
  edge here is a discharge site.
- Fill the connector area with the kit's stress-relief mastic or void filler.
- Position stress-control tubes/patches exactly at the semicon cut. Their location
  relative to that edge is the heart of the joint.
- **Heat-shrink:** shrink with a soft yellow flame, moving continuously, from the
  centre outward so air is pushed out, not trapped. **Cold-shrink:** pull the
  core in the direction marked; position before releasing — you cannot slide it after.

## 5. Screens, sheath and earthing
- Restore the metallic screen across the joint with the supplied mesh or connector so
  earth continuity is unbroken; sheath bonding and earthing are often specified by
  network design (cross-bonding on long circuits — don't improvise).
- Seal with the outer sleeve or resin shell and make it watertight.

## 6. Testing before return to service
- Insulation resistance test, then the after-installation test your network uses
  (often VLF AC or DC sheath test; some utilities add partial-discharge diagnostics).
- Record joint location, kit type, jointer and test results on the as-built record.

## Common failures
- Cuts in the insulation from semicon removal. Contamination wiped from semicon onto
  insulation. Stress control mispositioned by a few millimetres. Moisture in the
  conductor. Screen not reconnected, leaving a floating screen.

## Verify
- [ ] Cable identified and spiked before cutting.
- [ ] Cutbacks match the kit sheet; semicon edge smooth with no insulation damage.
- [ ] Cleaning done from insulation toward semicon; no residue.
- [ ] Connector die/torque correct; burrs removed; stress control on the cut line.
- [ ] Screens continuous; joint sealed; tests passed and recorded.
