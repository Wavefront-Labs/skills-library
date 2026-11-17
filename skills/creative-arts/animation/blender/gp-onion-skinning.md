---
id: creative-arts.animation.blender.gp-onion-skinning
name: gp-onion-skinning
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-onion-settings, onion-skin-mode, onion-frames, 2d-animation]
level: practitioner
status: docs-checked
description: "Configure Grease Pencil onion skinning: keyframes vs frames vs selected mode, before/after counts, colours, fade, keyframe-type filter and per-layer toggles."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/onion_skinning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-onion-skinning

Goal: see neighbouring drawings exactly as needed for inbetweening.

## Settings (Properties → Object Data → Onion Skinning)

- **Mode**: *Keyframes* (keyframes in the range set by Before/After), *Frames* (frames in that range) or *Selected* (only the keyframes you select manually in the Dope Sheet).
- **Opacity** of the ghosts; **Filter by Type** (which keyframe types are shown); **Keyframes Before/After** (how many frames or keyframes, depending on Mode).
- **Custom Colors**: *Before* and *After* colours.
- **Display**: *Fade* (ghosts fade the further from the current frame) and *Show Start Frame* (shows the first keyframe/frame as a ghost on the last frame, for loops).

## Toggles

- The main switch is in Viewport Overlays (Grease Pencil section); onion skinning visibility is per layer and can be toggled in the layer list.

## Workflows

- Inbetweening: Mode *Selected*, select the two keys around the gap.
- Timing check: Mode *Frames* with small Before/After values.
- Cycles: *Show Start Frame*.

## Verify

Scrub across a key: the ghosts update to the previous and next drawings per the mode.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Onion Skinning page). Confirmed mode names (Keyframes, Frames, Selected), opacity, filter, before/after counts, colours, fade, Show Start Frame and the overlay and per-layer switches. Removed unconfirmed claims about "Loop", the "Selected Keyframes" label, multi-object behaviour, held-frame behaviour in Keyframes mode and render exclusion.
Method: documentation only; no commands were run.
