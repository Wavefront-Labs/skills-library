---
id: creative-arts.animation.blender.fcurve-cycles-modes
name: fcurve-cycles-modes
category: creative-arts
field: animation
product: blender
tags: [blender, fcurve-modifiers, cycles-modes, repeat-with-offset, cycles-before-after, cycles-modifier, walk-cycle, looping]
level: practitioner
status: verified
description: "Loop animation with Blender's Cycles F-curve modifier: before/after modes, counts, cycle-aware keying, and making walk cycles travel forward."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/modifiers.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
  - https://docs.blender.org/manual/en/5.2/animation/actions.html
  - https://docs.blender.org/manual/en/5.2/animation/animation_editors.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# fcurve-cycles-modes

Goal: seamless loops and cycles that progress (walks, spinning wheels, bouncing balls travelling).

## Add

Graph Editor, select the curves, then Channel > Extrapolation Mode > Make Cyclic (adds a Cycles modifier; Clear Cyclic removes it), or Channel > Add F-Curve Modifier (Shift-Ctrl-M) > Cycles for the active curve. Settings are in Sidebar > Modifiers.

## Settings

- **Before / After Mode**: *No Cycles*, *Repeat Motion* (copies keep the same values), *Repeat with Offset* (each copy is shifted vertically so its first key matches the previous last key, giving forward travel), *Repeat Mirrored* (every other copy flipped horizontally).
- **Count**: number of copies; 0 means infinite. Python: `fcurve.modifiers.new('CYCLES')` with `mode_before` / `mode_after` (NONE, REPEAT, REPEAT_OFFSET, MIRROR) and `cycles_before` / `cycles_after`. Measured on a curve from 0 (frame 1) to 2 (frame 24) in Blender 4.5.14: Repeat Motion gave 2.0 at frame 47 and about 0 at frames 25 and 48; Repeat with Offset gave 4.0 at frame 47 (each copy shifted up by 2); Repeat Mirrored ran back down; with Count 1 after, values past the first repeat held at 2.0.
- Influence and Restrict Frame Range apply to every modifier (see `fcurve-noise-modifier`).

## Walk cycle recipe

1. Key an in-place cycle whose first and last keys are the same pose one loop apart (the action's Manual Frame Range should include the duplicated first key; tick Cyclic Animation on the action to record intent).
2. Put Cycles on the animated channels (Repeat Motion).
3. On the root's forward channel use Repeat with Offset so the character travels, or keep it in place if the game engine applies root motion.
4. Enable **Cycle-Aware Keying** (Keying popover in the Timeline/animation editor footer; `tool_settings.use_keyframe_cycle_aware`): on trivially cyclic curves a key inserted outside the cycle range is remapped inside it, and overwriting one end key updates the other. New curves in an action with Manual Frame Range and Cyclic Animation become cyclic automatically.

## Gotchas

- Cycles must be the first modifier in the stack (modifiers evaluate top to bottom), and it is not compatible with the Smooth (Gaussian) modifier. Put Noise or other modifiers below it.
- A "trivially cyclic" curve (both ends Repeat Motion or Repeat with Offset, other options default) gets cycle-aware automatic Bezier handle placement for a smooth seam.
- A first/last key mismatch shows as a pop at the loop point.
- The Cyclic Animation flag does not make an action loop by itself.

## Verify

Graph Editor with View > Show Extrapolation shows repeated shapes; playback across the loop boundary has no hitch.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source) and API reference: Cycles modifier modes and Count, first-in-stack rule and Smooth (Gaussian) incompatibility, trivially cyclic behaviour, Make/Clear Cyclic, Shift-Ctrl-M, Cyclic Animation and Manual Frame Range, Keying popover and Cycle-Aware Keying behaviour (animation editors page). Removed as unconfirmed: exporter baking claim, 24-frame figure. Corrected: Noise above Cycles is not valid because Cycles has to be first.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Cycles modifier properties and mode enums, the evaluations above, modifier type list including CYCLES and NOISE, Action `use_cyclic` (Cyclic Animation) and `use_frame_range` (Manual Frame Range) properties, `tool_settings.use_keyframe_cycle_aware` (default off). Unrun (documentation only): Make/Clear Cyclic operators and Shift-Ctrl-M, Cycles-first rule and Smooth (Gaussian) incompatibility, cycle-aware key remapping, trivially cyclic handle placement, the walk-cycle recipe, View > Show Extrapolation.

Method: manual text confirmed from documentation; modifier behaviour run headless in Blender 4.5.14.
