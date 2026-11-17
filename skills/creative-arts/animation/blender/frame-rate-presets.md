---
id: creative-arts.animation.blender.frame-rate-presets
name: frame-rate-presets
category: creative-arts
field: animation
product: blender
tags: [blender, frame-rate, frame-rate-presets, custom-fps, fps-base, time-stretching, ntsc]
level: practitioner
status: docs-checked
description: "Set Blender's frame rate right for film, broadcast and games: the Frame Rate menu, Custom FPS with Base for 23.976/29.97, changing fps mid-project and Time Stretching (Old/New)."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/format.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/frame_range.html
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/movie.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# frame-rate-presets

Goal: match the delivery spec before animating, because changing fps later shifts every key.

## Output Properties > Format > Frame Rate

- The **Frame Rate** menu lists common rates; pick **Custom** to expose **FPS** and **Base**. The actual rate is FPS / Base (FPS is the numerator, Base the denominator).
- Fractional rates follow from that: 23.976 is 24 / 1.001, 29.97 is 30 / 1.001, 59.94 is 60 / 1.001. Use the menu entry if it exists; use Custom otherwise.
- Choose the rate from the delivery spec (film 24, PAL 25, NTSC-derived 23.976, 29.97 or 59.94, games and web 30 or 60). Practice, not a Blender rule.

## Duration

Frame Range panel: duration is frames divided by the frame rate; the manual's example is 250 frames at 30 fps lasting 8.3 seconds. **Step** above 1 skips frames when rendering.

## Changing fps on an existing animation

- Changing the rate alone keeps keys on the same frame numbers, so the animation plays faster or slower in real time.
- To keep real-time duration, rescale the keys by new/old (24 to 30 is 1.25) in the Dope Sheet or Graph Editor.
- **Time Stretching** (Output Properties > Frame Range): **Old** is the length in frames of the original animation and **New** the length it will last. Old 2 and New 1 runs twice as fast. It does not change Start or End, so check the animation is not cut off or padded with still frames.

## Audio and video sync

- Set the scene frame rate before importing audio or video you must keep in sync.
- Movie strips have a **Set Scene Frame Rate** import option that copies the movie file's frame rate into the scene.

## Gotchas

- Physics caches are baked per frame, so rebake after changing fps (practice).
- 23.976 versus 24 in editing apps: deliver exactly what the editor's timeline expects.

## Verify

In the Timeline, View > **Use Timecode** (Ctrl T) shows the playhead as a timestamp; the last frame should land at the expected duration.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/output/properties/format.rst (Frame Rate menu, Custom FPS and Base as FPS/Base), frame_range.rst (duration example, Step, Time Stretching Old/New and the warning), editors/timeline.rst (Use Timecode, Ctrl T), video_editing/edit/montage/strips/movie.rst (Set Scene Frame Rate). Removed the hard-coded preset list, the snapping menu path, and claims about caches and audio under Time Stretching that the manual does not state. Method: documentation only; no commands were run.
