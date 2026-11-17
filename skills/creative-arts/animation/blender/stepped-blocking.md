---
id: creative-arts.animation.blender.stepped-blocking
name: stepped-blocking
category: creative-arts
field: animation
product: blender
tags: [blender, character-animation, stepped-blocking, stepped-keys, constant-interpolation, blocking-plus, spline-pass]
level: practitioner
status: docs-checked
description: "Run a stepped blocking workflow in Blender: default Constant interpolation, whole-character keys, key types, blocking-plus breakdowns, then converting to Bezier and fixing the spline pass."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/animation.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html
  - https://docs.blender.org/manual/en/latest/animation/in_betweens.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# stepped-blocking

Goal: review poses and timing cleanly before any interpolation. Process-level advice is in `animation-blocking-to-polish`; this is the Blender mechanics.

## Setup

- Preferences > Animation > F-Curves > **Default Interpolation = Constant** (new keys stepped) — or select all keys and T > Constant.
- Keying set **Whole Character** (Pose Mode) so every key pose keys every control — no drifting channels when you convert to spline later.
- Auto keying Add & Replace (Auto Keying options, Mode) plus key types: the Timeline Keying popover sets the New Keyframe Type, and in the Dope Sheet **R** changes the type of selected keys — Keyframe for key poses, Extreme, Breakdown, Moving Hold (see `keyframe-types`).

## Blocking passes

1. **Story poses** only, timing by moving key columns in the Dope Sheet (Summary row).
2. **Extremes and breakdowns** (blocking plus): Pose Breakdowner (Shift E) for favoured inbetweens; still stepped.
3. **Moving holds**: duplicate the pose a few frames later and push it slightly (key type Moving Hold).
4. Review: View > Render Playblast in the 3D Viewport for real-time playback.

## To spline

1. Select all keys, T > **Bezier** (keep Auto Clamped handles).
2. Expect floaty inbetweens: add **holds** (duplicate keys), adjust spacing with breakdowns, use Graph Editor to fix overshoots.
3. Optional intermediate (practice): key on twos before converting.

## Gotchas

- Keys missing on some controls at a pose (not whole-character) → after splining those controls interpolate across poses unexpectedly.
- IK/FK switches keyed with Bezier blend between values — keep switch properties Constant (practice).
- Constant interpolation holds each value until the next key, which the manual says is normally only used during the initial blocking stage of pose-to-pose workflows; use it in a final render only for deliberately stepped styles (see `fcurve-stepped-generator`).

## Verify

Dope Sheet columns are complete (every control keyed on every pose); after spline conversion, the motion keeps the pose timing.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) plus space_view3d.py from the same branch. Confirmed: Preferences > Animation > F-Curves > Default Interpolation; Constant interpolation described as normally used for blocking (fcurves/properties.rst); keyframe types Keyframe, Breakdown, Moving Hold, Extreme, Jitter, Generated (keyframes/introduction.rst) and Keyframe Type on R in the Dope Sheet (dope_sheet/editing.rst); Pose Breakdowner Shift E (in_betweens.rst); the Whole Character keying set. Wrong in the old text: the playblast command is View > Render Playblast in this release (the old name was Viewport Render Animation). Removed the nonexistent Bezier-with-Linear-ease intermediate; workflow passes are practice.

Method: documentation only; no commands were run.
