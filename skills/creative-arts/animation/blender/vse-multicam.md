---
id: creative-arts.animation.blender.vse-multicam
name: vse-multicam
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-multicam, multicam, editing]
level: practitioner
status: docs-checked
description: "Edit multi-camera footage in the VSE: syncing angles on channels, the Multicam Selector strip, cutting between source channels at the playhead, and finishing the cut."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/multicam.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# vse-multicam

Goal: cut between several cameras that recorded the same event (interviews, concerts, events).

## Prepare

1. Add each camera's strip on its own channel.
2. Sync the cameras using audio waveforms or the movement of objects. Grouping each camera with its audio and effects in a Meta strip makes syncing easier.
3. Split the editor into several Previews, one per input track, and set each preview's **Display Channel** to the channel number of that track.

## Multicam Selector

1. Add a **Multicam Selector** strip (Add > Effect Strip) above all the video channels.
2. In the Sidebar the strip has **Source Channel** (the channel it takes its input from) and **Cut To** (cuts the Multicam strip at the current frame and switches Source Channel to the chosen channel).
3. With the Multicam strip selected, the number keys 1 to 9 are mapped to the cut buttons. Play and press the number of the camera you want while watching the previews.
4. The result is a small Multicam strip per cut. Fine-tune by selecting the outer handles of two neighbouring Multicam strips (A/B rolling).

## Gotchas

- Enable proxies to improve playback with several high-resolution angles (see vse-proxy-setup).

## Verify

Play the cut: each segment shows the intended angle and the sync holds across cuts.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Multicam workflow steps, Display Channel on previews, Source Channel and Cut To options, number keys 1 to 9, one strip per cut and handle fine-tuning, proxy tip. Removed the claims about overlapping transitions and the effects-show-through behaviour, which the manual does not state.
- Method: documentation only; no commands were run.
