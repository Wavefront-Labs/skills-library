---
id: creative-arts.animation.blender.vse-retiming
name: vse-retiming
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-retiming, retiming, speed-keys, slow-motion]
level: practitioner
status: docs-checked
description: "Change clip speed with VSE retiming keys: showing keys, adding keys, setting segment speed, freeze frames, speed transitions, resetting, and the limits."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html#retiming-keys
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html#time
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-retiming

Goal: slow motion, speed ramps and freeze frames directly on a strip.

## Retiming keys

1. Select a strip and show its retiming keys: Strip > Retiming > **Toggle Retiming Keys** (Ctrl R), the same as the strip's Show Retiming Keys property in Sidebar > Strip > Time. Keys are visible but inactive until this is on.
2. **Add Retiming Key** (Strip > Retiming, or I and choose Add Retiming Key) adds a key at the current frame and also creates keys at the strip start and end, which must always exist.
3. Drag a key (or press G) to move a frame of the strip content to a new position, stretching or contracting time. Moving a key does not affect other keys in the strip.
4. **Set Speed** sets the speed of a segment as a rate compared to the original. **Preserve Current retiming** keeps the other segments' speed by changing the strip Duration instead.
5. **Add Freeze Frame and Slide** stops playback at a frame for any duration. There is no smooth transition into or out of a freeze frame.
6. **Add Speed Transition and Slide**: select a key between two segments of different speeds to create two linked keys for a smooth change. Moving both together changes where the transition starts and ends.
7. **Delete Retiming Keys** (Delete or X): the strip size does not change, so the speed becomes the average of the two segments.
8. **Reset Retiming** reverts all timing to the original strip.
- R quickly sets the speed of the selected strips: press R and enter the speed.
- Box select selects keys only if a key is already selected, otherwise it selects strips. Ctrl LMB selects all keys to the right.

## Limits

- Only strip content is retimed. Existing animation is not handled by the tool.
- Effect strips cannot be retimed.

## Gotchas

- The older Speed Control effect strip is a separate system (see vse-speed-control).

## Verify

Play the ramp: speed changes where intended and the total length fits the edit.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Toggle Retiming Keys menu path and Ctrl R, Add Retiming Key, Set Speed with Preserve Current retiming, Add Freeze Frame and Slide, Add Speed Transition and Slide, Delete and Reset Retiming behaviour, R quick speed, limits (content only, effect strips excluded). Removed the version gates, the optical-flow remark, the retime-sound claim and the no-ripple claim, which the manual does not state.
- Method: documentation only; no commands were run.
