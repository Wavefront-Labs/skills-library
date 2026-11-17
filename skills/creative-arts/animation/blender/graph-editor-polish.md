---
id: creative-arts.animation.blender.graph-editor-polish
name: graph-editor-polish
category: creative-arts
field: animation
product: blender
tags: [blender, graph-editor, f-curve, interpolation, tangents, timing, spacing, ease, slow-in, slow-out, overshoot, float, breaking-tangents, cycles-modifier, bezier, polish]
level: advanced
status: docs-checked
description: "F-curve craft in Blender: reading and cleaning curves, timing vs spacing, ease shapes, snappy vs smooth, removing float, breaking tangents, fixing overshoot."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/channels/editing.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Graph-editor polish (F-curve craft)

The Graph Editor is where motion stops being "the right poses in the right order" and
becomes *weight, snap, and life*. This is the curve-level craft that the polish pass of
`animation-blocking-to-polish` calls for. A curve is a readout of your animation's
physics: its shape IS the timing and spacing. Learn to read it and you fix at a glance
what would take an hour of scrubbing. Control names are the Rigify set from `rigging`.

The Blender menu paths, shortcuts and operator names here come from the manual; the shape, weight and timing guidance (and the frame numbers and percentages in the worked example) is animation practice, not documented values.

## Reading a curve: value is spacing, slope is speed

An F-curve plots a channel's value (Y) against time (X). Two things to read:

- **Slope = speed.** Steep = fast, flat = slow/held. A flat section is the character
  *holding*; a vertical-ish section is a snap. The eye reads the slope changes as
  acceleration — i.e. as weight.
- **Spacing of the in-betweens = the ease.** Bunched (close together in value) =
  slow; spread apart = fast. This is the old spacing chart, live. When something "feels
  floaty", look at the curve: it's a lazy S with no flat hold and no steep move — all
  mid-speed, which reads as weightless.

Turn on **View ▸ Show Handles** (`Ctrl H`) and work with the curve visible, not just the dope
sheet. Scrub while watching the curve; your eye learns to predict the motion from the
shape.

## Timing vs spacing (keep them separate)

- **Timing** = *where* the keys sit on X (which frame). Change timing by sliding keys in
  X (`G X`). This is "how long does the move take".
- **Spacing** = *how* the value moves between those keys — the tangent/handle shapes.
  This is "where's the fast part, where's the slow part". Change spacing by editing
  handles, not by moving keys.

The classic mistake is fixing a spacing problem (floaty) by moving keys (timing) and
vice versa. If the move takes the right number of frames but feels wrong, it's spacing —
leave the keys, shape the handles.

## Ease in / ease out shapes (slow-in, slow-out that reads as weight)

The default Bézier gives slow-in/slow-out on everything, which is why raw spline looks
bland. You shape it deliberately per channel:

- **Weight (heavy) = long, flat ease at both ends.** Flatten the tangents hard at the
  extremes so the curve sits near-horizontal before and after the move (handles rotated
  flat: set the handle type with `V`, then rotate the handles flat). The
  longer the flat, the heavier it reads — mass resists changing speed.
- **Light / snappy = short ease, most of the curve steep.** Barely any flat at the ends.
- **Hold = dead flat.** A moving hold is a *nearly* flat curve with the tiniest residual
  slope (never perfectly flat, or it's frozen).

## Snappy stylised curves: flat-then-fast

This is a 3D cel production — the house style wants **snap**, not buttery CG smoothing. The
signature shape is **flat-then-fast**: the character holds a pose (long flat curve),
then whips to the next pose (short steep ramp), then holds again. Hold–snap–hold. This is
what gives cel its pop.

- Build it by making the ease-out of the hold very flat and long, then letting the move
  itself be steep and short. On accents (a head snap, a finger point) you can go **near-
  vertical**, or even drop to a CONSTANT segment for one frame of true hold before the
  pop (`T` ▸ Constant on the leading key only).
- Contrast this with **smooth** (continuous rounded curves) which you reserve for slow,
  heavy, or lyrical motion — a sad slow turn, a drifting hover.
- Mixing both in one shot is correct: snap on the accents, smooth on the drifts.

## Removing float (the number-one polish fix)

Float is slow, aimless, low-amplitude wandering on channels that should be still or
should snap. It's what the default spline leaves everywhere and it reads as weightless
drift.

- **Find it:** channels with gentle, low-amplitude wiggles between your real keys and no
  clear hold. Box-select a region and look for curves that never flatten.
- **Fix it:** flatten the holds (make the curve dead-flat between meaningful keys), and
  **delete keys you didn't author** — `X` on the redundant in-betweens, or
  **Key ▸ Density ▸ Clean Keyframes**, which deletes keys with the same value as their
  neighbours (the Threshold option also removes near-equal ones; the Channels option cleans
  unselected keys too and deletes curves left with one key). The manual notes it can change
  curve shape, so run it before hand-tweaking. Fewer, more intentional keys = less float.
- **Simplify baked/noisy curves** with **Key ▸ Density ▸ Decimate (Ratio)** or
  **Decimate (Allowed Change)** (error margin) — useful after mocap or any sampled data; it
  removes the keys that influence the shape least so the curve is editable again.

## Breaking tangents (asymmetry = life)

By default a key's two handles are linked (a smooth hinge). For most expressive moves you
want them **broken** so the approach and departure speeds differ.

- Select the key ▸ `V` ▸ **Free** (or press `V` and break), then rotate each handle
  independently. Slow-in / fast-out: flat left handle, steep right handle. This is a
  *change of gear* at the pose — the character arrives gently and leaves fast, or slams
  in and eases out.
- Breaking tangents is how you put a hard accent on a pose without adding a key. A snap
  that "lands" has a flat incoming and a steep outgoing broken at the peak.
- Use **Auto Clamped** for channels you want smooth and overshoot-free; break manually
  only where you want the asymmetry.

## Fixing overshoot and gimbal

- **Unwanted overshoot** is usually plain **Auto** handles overshooting past a key on
  bouncy data — switch those keys to **Auto Clamped** (`V` ▸ Auto Clamped), which clamps
  the handle so the curve can't bulge past the key value. Then add overshoot back only
  where you *want* it, deliberately, by pulling a handle past the key or adding a key
  beyond the target and easing the return.
- **Gimbal / rotation flips:** Euler curves that jump ±360° or snap through a flip show
  as a near-vertical cliff on a rotation channel. Fix by setting the controller's
  rotation mode appropriately (often **XYZ** vs a better axis order for the joint), or
  use **Channel ▸ Discontinuity (Euler) Filter** with all three Euler rotation channels
  selected to clean up the jumps. If a curve crosses ±180 awkwardly, offset the whole channel by 360° (select
  keys ▸ `G Y 360`) so it reads as a continuous arc, not a flip.

## Cycles and sampling

- **Cycles modifier** loops a curve without copying keys: **Channel ▸ Extrapolation
  Mode ▸ Make Cyclic** (`Shift E`) adds it, or add the **Cycles** F-modifier yourself. It
  has to be the first modifier in the list. Use
  **Repeat with Offset** on a travelling channel (e.g. `root` location) so each loop
  continues from the last instead of snapping back — essential for walk/run travel and
  for the cheap crowd cycles in `crowd-animation`.
- **Bake** (`Channel ▸ Bake Channels`, with Frame Range, Frame Step, Interpolation Type
  and Bake Modifiers options; or `Key ▸ Density ▸ Bake Keyframes`, `Shift Alt O`, which
  keys every frame) converts a procedural or modified curve to real keys when you need to
  hand-edit it. Bake, then **Decimate** so you're not editing a key-on-every-frame wall.

## Worked example: a head snap with a settle

Say the head turns from screen-left to screen-right over f0→f8 and should land with a
cel snap and a small settle. On the head Z-rotation channel you want to see:

- f0: key at the start value, **flat long outgoing handle** — the head holds, then gathers.
- f8: key at (slightly past) the target — the snap. The incoming handle is **steep**
  (fast arrival), broken from the outgoing. This is flat-then-fast: nothing for 0-4, then
  a whip into f8.
- f8 value pushed ~5-8% *past* the final rest angle (the overshoot), with...
- f12: key at the true rest angle, eased return. The curve peaks at f8 and settles back
  into f12 — that little hook on the curve IS the settle you see on screen.
- The eyes' aim channel leads: its move starts ~f-2 (before the head), so the eye arrives
  first and the head follows — the single biggest "it's thinking" cue.

Read back: one hold, one steep snap with a broken peak, one small overshoot hook. If the
curve is instead a smooth symmetric S from f0 to f12, you've got CG float, not a cel snap.

## Retiming in the graph editor

- **Box-select and scale in X** (`S X` around the pivot you choose) to stretch
  or compress a move's timing without touching its spacing shape — the ease relationships
  are preserved, the move just takes more/fewer frames.
- **Slide a whole block** (`G X`) to shift a beat later/earlier against the audio.
- Snap keys to whole frames after scaling (`Key ▸ Snap`, Snap To = Frame) — sub-frame
  keys from a scale are a common source of a tiny unexplained jitter (practice).
- Use the **Normalize** toggle to see wildly different-scale channels (rotation in degrees
  vs location in BU) on one readable graph when comparing their shapes; turn it off to
  edit real values.

## Working order (big to small)

Polish curves spine-first: `root`/`torso` path, then `hips`/`chest`, then
`hand_ik`/`foot_ik`, then `head`, then face. A clean master curve makes every downstream
channel easier; polishing fingers over a floating spine wastes the work.

## Verify (pass/fail)

- [ ] **Holds are flat** and moves are steep — the curves show hold-snap-hold where the
      style wants snap, not uniform lazy S-curves everywhere. (fail = floaty mid-speed mush)
- [ ] **No float:** still/held channels are dead-flat (moving holds keep a hair of slope),
      and redundant unauthored keys are cleaned out. (fail = aimless drift)
- [ ] **Ease reads as weight:** heavy things have long flat eases, light things short;
      you can tell the weight from the curve shape alone. (fail = everything same weight)
- [ ] **Tangents broken where the move changes gear**; accents have asymmetric handles,
      not smooth hinges. (fail = no snap/accent)
- [ ] **No unwanted overshoot** (Auto-Clamped on bouncy channels) and no rotation
      flips/gimbal cliffs (Euler filter / correct rotation order). (fail = phantom bounce
      or pop)
- [ ] Baked/mocap curves **simplified** to editable keys; travelling cycles use Cycles +
      Repeat-with-Offset, not hand-copied loops. (fail = uneditable key wall / snap-back)

See `animation-blocking-to-polish` (this is its polish pass), `body-mechanics` (curve
shapes = mechanics), `twelve-principles`, `mocap-retarget` (simplify baked data),
`crowd-animation` (cycles).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Show Handles `Ctrl H`; Handle Type `V` (Auto Clamped recommended by default) and Interpolation Mode `T`; Key ▸ Density ▸ Clean Keyframes / Decimate (Ratio) / Decimate (Allowed Change) / Bake Keyframes (`Shift Alt O`); Channel ▸ Bake Channels, Extrapolation Mode ▸ Make Cyclic (adds a Cycles modifier, which must be first), Discontinuity (Euler) Filter; Cycles modifier Repeat with Offset; Normalize toggle; Key ▸ Snap. Fixed: Clean Keyframes and Decimate were given wrong menus ("Channel" and "Simplify Curves"), Euler filter is in the Channel menu, Bake Channels is in the Channel menu.
Method: documentation only; no commands were run.
