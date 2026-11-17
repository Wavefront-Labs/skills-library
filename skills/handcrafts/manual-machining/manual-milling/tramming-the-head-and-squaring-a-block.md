---
id: handcrafts.manual-machining.manual-milling.tramming-the-head-and-squaring-a-block
name: tramming-the-head-and-squaring-a-block
category: handcrafts
field: manual-machining
product: manual-milling
tags: [manual-milling, milling-machine, bridgeport, turret-mill, knee-mill, vertical-mill, tramming, tram, dial-indicator, test-indicator, vice, vise, indicating-the-vice, parallels, soft-jaw, squaring-stock, six-sides, face-mill, fly-cutter, end-mill, climb-milling, conventional-milling, feeds-and-speeds, surface-speed, chip-load, engineers-square, cylinder-square, deburring, machinist]
level: practitioner
status: draft
description: "Tram a knee-mill head, indicate the vice square, then mill all six faces of a sawn block flat, parallel and square with the standard 1-2-3-4 face sequence and a round bar."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tramming the head and squaring a block

**Goal:** a block with six faces flat, parallel and square to within about 0.02 mm
over 100 mm — the basic accuracy that every later milling operation relies on.

## 1. Tram the head
A head out of tram leaves a dished or stepped surface when fly-cutting or face-milling.
1. Clean the table. Mount a dial test indicator on an arm in the spindle (collet or
   tram bar) sweeping a circle of 150–250 mm diameter.
2. Lower the quill until the indicator reads ~0.2 mm preload on the table at 6
   o'clock (front); zero it.
3. Turn the spindle **by hand** (power off) to 12, 3 and 9 o'clock. Avoid T-slots —
   sweep over a ground parallel or a clean flat if they get in the way.
4. **X (left–right):** adjust the head's tilt bolts until 3 and 9 agree. **Y
   (front–back, nod):** adjust the nod. Re-check both; they interact.
5. Target: within 0.01–0.02 mm across the sweep. Lock everything, then re-check —
   locking often moves it.

## 2. Indicate the vice
1. Bolt the vice down lightly. Put a test indicator in the spindle against the
   **fixed jaw**.
2. Traverse X across the jaw; tap the vice round with a soft mallet until the needle
   moves < 0.01 mm over the jaw length. Tighten, re-check.

## 3. Feeds and speeds (starting point)
- Spindle rpm = (cutting speed m/min × 1000) / (π × cutter dia mm).
- HSS on mild steel: ~25–30 m/min; aluminium: 100+ m/min (machine-limited); cast
  iron ~20 m/min. So a 50 mm fly-cutter in steel ≈ 160–190 rpm.
- Chip load for HSS end mills in steel: roughly 0.02–0.05 mm/tooth. These are
  conservative generic figures — your tooling maker's charts take precedence.

## 4. The squaring sequence
Number the faces as you go with a marker.
1. **Face 1:** put the best (flattest) sawn face up on parallels; clamp; fly-cut or
   face-mill clean. Deburr.
2. **Face 2:** Face 1 against the **fixed jaw**, a **round bar** between the work and
   the moving jaw (so the moving jaw cannot tilt it), parallels under. Tighten, tap
   down lightly with a soft hammer, mill. Face 2 is now square to Face 1.
3. **Face 3:** Face 1 against the fixed jaw again, Face 2 **down** on the parallels,
   round bar behind. Mill to width. Face 3 is parallel to Face 2 and square to Face 1.
4. **Face 4:** Face 1 down on parallels, no round bar needed. Mill to thickness.
   (Check you can't pull the parallels by hand — if they move, the work isn't seated.)
5. **Ends 5 and 6:** stand the block on end with Face 1 against the fixed jaw; square
   the vertical edge with an engineer's square resting on the vice bed (or set it
   with an indicator down the face). Mill one end, flip, mill to length. Long pieces:
   side-mill the ends with an end mill instead, with the block lying down.

## Faults
- **Faces not square:** moving jaw tilting the work (no round bar), chips on the
  jaw or parallels, or the vice not tightened enough.
- **Stepped or concave face:** head out of tram.
- **Chatter:** cutter overhang, loose gib, too high rpm, or work too high in the vice.
- **Climb milling on a manual machine without backlash elimination** can grab the
  table — conventional mill on the edge passes unless you have locked the axis.

## Safety
Safety glasses always; chips from a fly-cutter fly far — use a guard. Never clear
chips with fingers or while rotating. Remove the drawbar wrench. Clamp work, never hold it.

## Verify
- [ ] Tram within 0.02 mm across the sweep, re-checked after locking.
- [ ] Fixed jaw indicated straight within 0.01 mm.
- [ ] Each face cleaned up fully; all edges deburred.
- [ ] Squareness checked with an engineer's square against a light source (no light gap).
- [ ] Opposite faces parallel within 0.02 mm measured with a micrometer at four corners.
