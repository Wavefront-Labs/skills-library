---
id: creative-arts.animation.blender.vse-channels
name: vse-channels
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-channels, mute-channel, lock-channel]
level: practitioner
status: docs-checked
description: "Organise the VSE timeline with channels: naming, muting and locking channels, channel stacking order rules, and hiding or muting individual strips."
sources:
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/channels.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html#lock-mute
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-channels

Goal: a readable, safe timeline layout.

## Channel region (left side of the sequencer)

- **Name**: double-click to rename (for example `V1 picture`, `A1 dialogue`).
- **Mute Channel**: none of the channel's strips can be seen or heard in the final video.
- **Lock Channel**: protects all strips on the channel against accidental changes.
- Toggle the region with View > Channels.

## Stacking rules

- A channel is a horizontal track like a layer: higher channels are displayed in front of lower ones.
- Strips on the same channel cannot overlap. To play two strips at once, put them in different channels.
- Use the strip's **Blend** mode and **Opacity** (Sidebar > Strip > Compositing) to control how it combines with strips in lower channels.

## Strip-level hiding and locking

- **H** mutes selected strips, **Alt H** unmutes, **Shift H** mutes the unselected strips, **Shift Alt H** unmutes them.
- **Ctrl H** locks selected strips, **Ctrl Alt H** unlocks.
- The Sidebar > Strip panel also has a Mute checkbox and the Time panel has a lock toggle in its header.

## Layout conventions

Video on lower channels, titles and graphics above, sound strips grouped by type on separate channels. Leave a spare channel between groups to work in.

## Gotchas

- Muted channels stay muted in the final render. Unmute before exporting.

## Verify

Mute the music channel and render a short range: the music should be missing. Unmute and render again.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Channel region name, Mute Channel and Lock Channel behaviour, View > Channels toggle, no overlap inside a channel, strip mute and lock shortcuts (H, Alt H, Shift H, Ctrl H, Ctrl Alt H; the old Shift L lock key was wrong). Removed the Alpha Over default claim and the locked-strips-in-meta claim, which no manual page states.
- Method: documentation only; no commands were run.
