---
id: manufacturing-production.assembly-line-hand-work.hand-assembly.assembling-to-takt-at-a-paced-station
name: assembling-to-takt-at-a-paced-station
category: manufacturing-production
field: assembly-line-hand-work
product: hand-assembly
tags: [hand-assembly, assembly-line-hand-work, assembly-operator, paced-line, takt, cycle-time, work-instructions, standard-work, part-orientation, poka-yoke, error-proofing, snap-fit, press-fit, arbor-press, click-check, self-inspection, andon, esd, ergonomics, two-handed-work, motion-economy, line-stop, defect-escalation]
level: intro
status: draft
description: "Work a paced assembly station: read the instruction, lay out parts for two-handed flow, seat snap and press fits with a check, self-inspect, keep takt, and pull andon on defects."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assembling to takt at a paced station

**Goal:** build every unit right, in the station's cycle time, for a whole shift — without
passing a defect to the next station or hurting yourself. Speed comes from a fixed method,
not from rushing.

## 1. Before the first unit
- **Read the work instruction** at the station: the steps, the *key points* (the details
  that make or break quality: "until it clicks", "connector latch fully down") and
  the reasons. Note the revision and that it matches the model on the line.
- Check the parts in the bins match the instruction (part number on the bin label and
  on the parts). Similar-looking parts in neighbouring bins are a classic mix-up.
- Check tools: right bit, torque tool status OK, press set, ESD wrist strap tested if
  you handle electronics (most ESD stations have a tester at the station).

## 2. Lay out for flow
- Parts in the order you use them, within easy reach (roughly forearm reach, no
  stretching or twisting), with the most-used closest.
- **Use both hands at once** where the instruction allows: left picks the next part while
  right finishes the current step. Pick from the front of bins; tilt bins toward you.
- Keep the next unit's parts presented, not dumped. A tidy station is faster.

## 3. Orientation and fit
- Find the **orientation feature** before fitting: keying tab, flat, chamfer, pin 1
  mark, arrow, colour stripe. Good designs only fit one way (poka-yoke); where they
  don't, the instruction should say how to tell.
- **Snap fits:** push square until you **feel and hear the click**, then **tug-test**
  (gentle pull) to confirm it latched. Partial snaps pass the eye and fail later.
- **Press fits:** use the press or fixture designed for it, never a hammer. Seat
  fully to the stop; the press may have a force/position monitor — a red light means
  reject, not "try again harder".
- **Connectors:** push until latched, then pull-check the housing (not the wires).
- **Cables:** route as shown; pinched or stretched wires are the top hidden defect.

## 4. Self-inspection
Each station checks its own work before passing it on: the key points, nothing loose,
no damage, no leftover parts. **Spare screw or clip at the end of the cycle = something is
missing** — find it before passing the unit. Many stations use a parts-count or
"empty tray" check for exactly this.

## 5. Keeping to takt
- Know your **cycle time vs takt**. If you are consistently behind, tell the team leader —
  the station may be overloaded; don't hide it by skipping steps.
- When you fall behind on one unit, don't rush the next; finish correctly and recover
  over several cycles. Rushing causes the defect that stops the line.
- Rotate stations as the site plans; repetitive strain risk rises with long periods on one
  task.

## 6. When something is wrong — andon
Pull andon / call the team leader at the **first** sign of: wrong or damaged parts, a
defect from an upstream station, a fit that needs force it shouldn't, a tool fault,
or you can't make takt. Don't fix an upstream defect silently — the station that made it
needs to know. Don't pass a unit you're unsure about.

## 7. Ergonomics
- Bench and fixture height suits you (elbow height for light assembly, a bit lower for
  force work). Ask for adjustment.
- Push with the palm or a tool rather than the thumb for repeated snaps; repeated thumb
  pressing is a common strain injury.
- Report aches early.

## Verify
- [ ] Instruction revision and parts match the model being built.
- [ ] Every snap and connector tug-tested; press monitors green.
- [ ] No leftover parts at end of each cycle.
- [ ] Cycle within takt without skipping key points.
- [ ] Andon used for any doubt rather than passing the unit.
