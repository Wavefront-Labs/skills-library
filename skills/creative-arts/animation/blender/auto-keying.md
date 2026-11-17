---
id: creative-arts.animation.blender.auto-keying
name: auto-keying
category: creative-arts
field: animation
product: blender
tags: [blender, animation, auto-keying, auto-key, only-insert-available, keyframes, keying-preferences]
level: practitioner
status: docs-checked
description: "Use Blender auto keying safely: record button, Add & Replace vs Replace modes, Only Insert Available, Layered recording, keying preferences (visual keying, default channels) and avoiding stray keys."
sources:
  - https://docs.blender.org/manual/en/latest/animation/animation_editors.html
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/animation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# auto-keying

Goal: keys appear when you pose, without polluting the timeline with keys on channels you never meant to animate.

## Controls (Timeline header, record dot)

- **Record** toggle turns auto keying on. Its Auto Keying options:
  - **Mode: Add & Replace**: add or replace keyframes as needed.
  - **Mode: Replace**: only replaces existing keyframes — safe polish mode.
  - **Only Active Keying Set**: stops Auto Keying keying properties outside the active keying set (see `keying-sets`).
  - **Layered Recording**: adds a new NLA track for every pass made over the animation.
- Timeline > Keying popover: **Active Keying Set**, **New Keyframe Type**, and **Cycle-Aware Keying** (keyframes inserted into trivially cyclic curves are remapped inside the cycle and the end keys are kept in sync — useful when tweaking a walk loop).
- Preferences > Animation > Keyframes: **Only Insert Available** (only add keys to channels whose F-curves already exist; under Auto-Keyframing), **Only Insert Needed** (separate Manual and Auto toggles; skips keys that do not change the value), **Default Key Channels** (Location, Rotation, Scale, Rotation Mode, Custom Properties; used when no keying set is active), and **Visual Keying** (keys the constraint result).
- Preferences > Animation > F-Curves: **Default Interpolation**, **Default Handles**, **Default Smoothing Mode**, **XYZ to RGB**.

## Habits

- Blocking: Add & Replace, plus Only Insert Available (Preferences) after setting first keys on all controls, so no new curves appear.
- Polish: Replace mode, so tweaks never add new frames between your breakdowns.
- Turn record off before selecting/organising rigs — accidental grabs create keys.

## Gotchas

- Auto Keying only works for transform properties (Location, Rotation, Scale); changing, say, a material colour still needs a manual key. Check the Dope Sheet after scripts or snapping that move controls.

## Verify

Dope Sheet with "Only Show Selected" off: no unexpected channels; Graph Editor shows only intended curves after a session.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) plus RNA definitions in rna_scene.cc. Confirmed: the Auto Keying mode options Add & Replace and Replace, Only Active Keying Set and Layered Recording (animation/animation_editors.rst, ToolSettings.auto_keying_mode, use_keyframe_insert_keyingset, use_record_with_nla); Cycle-Aware Keying in the Keying popover; Only Insert Available, Only Insert Needed (Manual/Auto), Default Key Channels (including Rotation Mode) and Visual Keying in editors/preferences/animation.rst. Wrong in the old text: Only Insert Available and Only Insert Needed are Preferences options, not record-dropdown items, and there is no Use Keying Set item. Removed the unconfirmed claims about cancelled transforms and locked channels.

Method: documentation only; no commands were run.
