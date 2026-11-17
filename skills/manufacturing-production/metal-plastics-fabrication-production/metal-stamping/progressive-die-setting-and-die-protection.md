---
id: manufacturing-production.metal-plastics-fabrication-production.metal-stamping.progressive-die-setting-and-die-protection
name: progressive-die-setting-and-die-protection
category: manufacturing-production
field: metal-plastics-fabrication-production
product: metal-stamping
tags: [metal-stamping, press-shop, stamping-press, progressive-die, die-setting, die-setter, shut-height, tonnage, tonnage-monitor, coil-feed, servo-feed, straightener, pilot-release, pitch, die-protection, sensors, misfeed, slug-pulling, burr, first-off, first-piece, lockout-tagout, loto, die-cart, quick-die-change, qdc, smed, link-press, servo-press]
level: practitioner
status: draft
description: "Set a progressive die in a stamping press and run it safely: shut height, coil feed and pilot release, die protection sensors, inching through, first-off approval and hit-to-hit watch items."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Progressive die setting and die protection

**Goal:** get a progressive die from the cart to approved first-off parts without
crashing it — a die crash can cost weeks and a fortune — and keep it running with
sensors that stop the press before a misfeed becomes a crash.

## Safety first
Die setting happens inside the press's danger zone. Follow **lockout/tagout**, use die
blocks (safety blocks) whenever you are between the dies with the ram up, and never
reach into the die area under power. Use inch/single-stroke modes with two-hand
controls as designed. Site procedures override anything here.

## 1. Before the die arrives
- Confirm press **tonnage and bed size** are right for the die (die card), and the
  **shut height** range of the press covers the die's shut height.
- Press slide adjusted **up** above the die's shut height before loading.
- Coil: right material, gauge, width and coil weight; check the material cert matches.
- Die maintenance tag: is the die released from the toolroom, sharpened, sensors tested?

## 2. Setting the die
1. Clean bolster and ram face — a chip under the die ruins parallelism.
2. Move the die in on rollers/cart (QDC systems: hydraulic lifters and clamps), locate
   on keys/locating pins so it is square to the feed line.
3. Slowly bring the slide down in inch mode to just touch, then set to the die's
   **shut height** (minus whatever your shop's method for closing to load). Clamp the
   upper die to the ram, lower die to bolster, torque/hydraulic clamps engaged.
4. Connect die protection sensors, air, lube, and any in-die tapping/transfer services.
5. Set **tonnage monitor** limits per the die's baseline (high and low per channel).

## 3. Coil feed
- Straightener roll settings for the gauge (too little → coil-set curvature, too much
  → work hardening/marking).
- Feed **pitch/progression** exactly per die card; feed height level with the die
  pass line.
- **Pilot release**: the feed rolls must open while the pilots locate the strip; the
  release timing (crank angle) is set so pilots enter before forming starts. Wrong
  timing → pilot holes elongated and misfeeds.
- Lubrication applied to the strip if the die requires it.

## 4. First hits
- Thread the strip by inching, one station at a time, checking each station cuts and
  forms as expected. Watch for slugs pulled up onto the die face.
- Run a few parts single-stroke, then continuous at low SPM.
- **First-off inspection**: dimensions and features per the control plan, burr height,
  part orientation; approval by QA/lead per site rules before production rate.

## 5. Die protection
Sensors (proximity, photo-eye, contact pins) are programmed with a **crank-angle window**
in which each signal must (or must not) occur:
- **Misfeed / strip position** (pilot or end-of-strip sensor),
- **Part out / part ejection** (part must leave the die each hit),
- **Slug and scrap** (slug-pulling, scrap chute blocked),
- **Stock buckle** and end-of-coil.
Test each sensor on setup by simulating its fault at inch speed. A bypassed sensor is
the most common precursor to a crash — log any bypass with approval.

## 6. Hit-to-hit watch items
- Tonnage trend creeping up → dulling punches, material change, lube failure.
- Rising burr height → sharpen interval approaching or punch-die clearance worn.
- Slugs on the surface → slug pulling (vacuum, punch shedder pins, sharpening).
- Scrap and part chutes clear.

## Verify
- [ ] Shut height, clamping and keys confirmed before first stroke.
- [ ] Feed pitch and pilot release timing verified by inching.
- [ ] Every die-protection sensor fault-tested; no unapproved bypass.
- [ ] Tonnage limits set from baseline.
- [ ] First-off approved before rate production.

*Draft: generalised across mechanical and servo presses; controller names (Link, Wintriss
and other die-protection units) and timing values are press-specific.*
