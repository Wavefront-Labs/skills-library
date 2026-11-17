---
id: creative-arts.animation.blender.jump-animation
name: jump-animation
category: creative-arts
field: animation
product: blender
tags: [blender, character-animation, jump-animation, jump, landing, body-mechanics, ballistic-arc]
level: practitioner
status: docs-checked
description: "Animate a character jump in Blender: anticipation, push-off, parabolic COG arc in the Graph Editor, airborne overlap, contact and landing compression/recovery, with frame counts at 24 fps."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html
  - https://studio.blender.org/training/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# jump-animation

Goal: a believable standing jump with weight. General principles are in `body-mechanics`; this is the Blender execution.

## Key poses (24 fps; the frame numbers are practice guidelines, not from documentation)

1. **Stand** (f1) → **Anticipation crouch** (f8-12): COG down, arms back, spine compressed.
2. **Push-off / extension** (f14-15): legs extended, toes last contact, arms swinging up.
3. **Apex** (f20-22): body tucked or extended per style.
4. **Contact** (f27-28): heels/balls hit, legs nearly straight.
5. **Compression** (f30-32): deepest absorb, arms forward for balance.
6. **Recovery/settle** (f40-50).

## Blender execution

- Block with Constant interpolation, Whole Character keying set (see `keying-sets`).
- **COG/root Z curve** (Graph Editor): between push-off and contact it must be a parabola — symmetric arc, fastest at takeoff/landing, slowest at apex. With Bezier keys at takeoff, apex, landing: apex key flat handles (Auto Clamped), takeoff/landing keys with steep straight-ish handles (Vector, or Free/Aligned handles you shape yourself) — no ease into the ground. Auto Clamped is the manual's recommended default handle type because it avoids overshoot at extremes.
- **COG forward (Y)**: linear during airtime (no air resistance) — set interpolation Linear between takeoff and contact.
- Feet: IK controls follow the COG in air (or switch child-of; see `child-of-dynamic-parenting`), planted with Constant before takeoff and after contact.
- Overlap: arms/head/spine trail 1-2 frames (offset keys in the Dope Sheet).
- Motion path on the COG (see `motion-path-settings`) to check the arc.

## Gotchas

- Easing into the ground (slow-in on landing) makes characters float — impacts need speed.
- Airtime too long reads as low gravity: with g = 9.81 m/s² a jump whose apex is 1 m above takeoff is airborne for 2·√(2·1/9.81) ≈ 0.9 s (about 22 frames at 24 fps); the 8-12 frame range for small hops is practice.
- Hips lead, chest follows; check torso arcs, not only COG.

## Verify

Graph Editor Z curve is a clean parabola; playback at real speed (see `timeline-playback`) reads weight on both takeoff and landing.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: handle types Auto Clamped, Vector, Aligned, Free and Linear/Constant/Bezier interpolation in editors/graph_editor/fcurves/properties.rst, and the Whole Character keying set (animation/keyframes/keying_sets.rst). Computed: airtime for a 1 m apex at 9.81 m/s2 is about 0.9 s. The pose frame numbers, overlap offsets and parabola advice are animation practice; no documentation covers them and they are labelled as such.

Method: documentation only; no commands were run.
