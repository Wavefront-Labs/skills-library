---
id: manufacturing-production.cnc-machining-production.swiss-type-turning.guide-bushing-setup-and-small-part-strategies
name: guide-bushing-setup-and-small-part-strategies
category: manufacturing-production
field: cnc-machining-production
product: swiss-type-turning
tags: [swiss-type-turning, swiss-lathe, swiss-turn, sliding-headstock, citizen, star, tsugami, tornos, guide-bushing, guide-bush, rotary-guide-bushing, guide-bushing-clearance, ground-bar, bar-tolerance, h8, h9, pinch-turning, balanced-turning, back-working, sub-spindle, gang-tools, simultaneous-machining, superimposed-machining, small-diameter-parts, medical-parts, thin-wall, deflection, chip-control, oil-coolant, non-guide-bushing, cnc-machining-production]
level: advanced
status: draft
description: "Set up sliding-headstock lathes: guide bushing adjustment for bar tolerance, front/back working overlap, pinch turning, small-diameter deflection control and chip management."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Guide bushing setup and small-part strategies on Swiss-type lathes

**Goal:** make small, long, precise parts (pins, bone screws, connector contacts)
consistently on a sliding-headstock lathe (Citizen, Star, Tsugami, Tornos and others)
by getting the guide bushing, bar and tool overlap right.

*Draft: general Swiss practice; programming syntax (multi-path `!`/`%` waits,
superimposition codes) is builder-specific — check your machine's manual.*

## 1. Why Swiss is different
- The **headstock slides in Z** carrying the bar through a stationary **guide bushing**;
  tools cut right next to the bushing. The unsupported length is always tiny, so long
  slender parts can be turned with little deflection.
- Consequence: part accuracy depends on **bar quality** and **bushing clearance**, more
  than on a conventional lathe.

## 2. Bar stock
- Use **ground bar** with a tight diameter tolerance (commonly h8 or tighter, depending
  on the job) and straightness. Drawn bar varies too much for the bushing to hold it.
- Chamfer bar ends; deburr. Check a sample of bars with a micrometer along their length.
- Bar remnant is longer than on a conventional lathe (the bar must stay in the
  bushing and collet) — include it in material costing.

## 3. Guide bushing adjustment
1. Fit the bushing size for the bar. Rotary (synchronised) guide bushings are common;
   fixed bushings exist for some jobs.
2. Adjust clearance on a sample bar: typically just a few microns of running clearance
   — the bar slides freely by hand with no detectable play. Too tight → seizure, heat,
   bar marking; too loose → chatter, taper and poor roundness.
3. Recheck after warm-up and with each new bar batch; bar diameter variation between
   batches matters.
4. **Non-guide-bushing mode** (on convertible machines): uses the collet only, saving
   remnant on short parts and allowing un-ground bar; you lose the long-part support.

## 4. Front and back working
- **Main spindle** (front) does OD turning, cross drilling, milling with gang tools.
- **Sub-spindle** (back) picks off the part and does back-end features with
  back-working tools — **simultaneously** with the front cutting the next part.
- Cycle time is set by the longer of the two channels; balance work between them.
  Move features to the back end if the front is the bottleneck.
- Synchronisation waits between channels (wait codes) must be placed so neither
  channel waits needlessly — check the two-channel timeline in the control or CAM.

## 5. Small-diameter strategies
- **Pinch / balanced turning:** two opposing tools cut simultaneously, cancelling radial
  force — longer, thinner sections with less deflection and faster removal.
- Take the **finish pass close to the bushing** and in as few Z moves as possible;
  rough the length in steps, finish in one continuous pass.
- **Sharp, positive-rake inserts** with small nose radius (e.g. 0.05–0.2 mm) to reduce
  cutting force on tiny diameters.
- Thread whirling for long fine bone-screw threads rather than single-point threading
  (if the machine has a whirling attachment).
- Thin walls: finish OD before drilling where possible, or support with a pin in the
  sub-spindle.

## 6. Chips and coolant
- Neat cutting oil is common on Swiss machines: better finish and tool life on small
  parts, but fire risk under unattended running — suppression system and mist
  extraction.
- Long chips wrap around gang tools. Use chip-breaking cycles (peck turning, interrupted
  feed) and check the chip conveyor.

## Gotchas
- Changing bar supplier changes the bushing setting.
- Over-tightened bushing marks finished OD — visible as spiral marks.
- Cutoff burr/pip on the back end is handled on the sub-spindle — plan a back facing.
- Measurement at room temperature vs machine temperature on 10 µm tolerances.

## Verify
- [ ] Bar diameter checked against the bushing setting for each batch.
- [ ] Bushing clearance set with no play and no seizing after warm-up.
- [ ] Two-channel timeline balanced; no unnecessary waits.
- [ ] First-article size, roundness and straightness measured on full part length.
- [ ] Fire suppression active before oil-coolant unattended runs.
