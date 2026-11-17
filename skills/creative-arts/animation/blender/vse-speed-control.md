---
id: creative-arts.animation.blender.vse-speed-control
name: vse-speed-control
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-speed-control, speed-control, slow-motion]
level: practitioner
status: verified
description: "Use the VSE Speed Control effect strip: multiply speed, stretch to length, frame number and length modes, frame interpolation, and when to use retiming instead."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/speed_control.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html#retiming-keys
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-speed-control

Goal: change playback speed of a clip with the Speed Control effect strip.

## Setup

Select the strip and use Add > Effect Strip > Speed Control. The effect strip's bounds are controlled by its source strip (tested: a speed strip on a 49 frame strip was also 49 frames). From Python (4.5.14): `scene.sequence_editor.strips.new_effect(name, 'SPEED', channel, frame_start, input1=source)`; the properties are `speed_control` (STRETCH, MULTIPLY, FRAME_NUMBER, LENGTH), `speed_factor`, `speed_frame_number`, `speed_length` (percentage of the input length) and `use_frame_interpolate` (default off); the older name `sequence_editor.sequences` is an alias of `strips` there.

## Speed Control modes (Sidebar > Effect Strip)

- **Stretch**: calculates the speed from the length of the input strip (scale a strip to half length and it plays at twice the speed).
- **Multiply**: multiplies the speed by a **Multiply Factor** (0.5 is half speed, 2 is double). Negative values reverse the input, so -2 plays in reverse at double speed. Readjust the strip length by hand.
- **Frame Number**: the frame to remap the current frame to. Keyframe it to recreate the animation; set the Graph Editor interpolation to Linear since the default Bezier rarely fits.
- **Length**: maps the frame range on a percentage scale (50 percent selects the frame halfway through).
- **Interpolation**: crossfades between frames to reduce tearing when the speed is slower than the original frame rate.

## Slow motion example

Use Multiply with a factor like 0.5. A strip that plays slower runs out of frames later, so lengthen the source strip: `new_length = real_length / speed_factor`. A strip that plays faster runs out of frames early and holds its last frame.

## Frame rate conversion

Multiply with a factor such as 30/24 (1.25) converts 30 fps material to 24 fps, optionally with Interpolation enabled for a film blur look.

## When to use retiming instead

Retiming keys (see vse-retiming) change speed on the strip itself without an extra strip. Use Speed Control for frame-number remapping.

## Gotchas

- If you keyframe the speed factor, run Refresh All or the changes will not take effect. Keyframing Frame Number is usually better.
- When the strip runs out of frames it repeats the last one (frozen). Place the next strip under the original where motion should continue.

## Verify

Check the frame shown at the start and end of the speed strip: the source range matches what you intended.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Speed Control modes Stretch, Multiply, Frame Number and Length, Multiply Factor behaviour including negative values, Interpolation, length formula, frame-rate conversion example, Refresh All note, retiming alternative. Removed the sound-not-retimed and source-handle claims, which the manual does not state.
- Run check, 2026-11-01, Blender 4.5.14 LTS headless: a Speed Control effect strip was created on a Color strip; the four control modes, the property names above and their defaults (STRETCH, factor 1.0, interpolation off) exist; `speed_factor` accepted -2.0 in Multiply mode; the property descriptions match the modes described; `bpy.ops.sequencer.refresh_all` and the retiming operators exist. Unrun: the playback result of each mode, the length formula, frame-rate conversion, the Refresh All requirement, Graph Editor interpolation advice.
- Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
