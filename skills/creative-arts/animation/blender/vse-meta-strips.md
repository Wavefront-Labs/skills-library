---
id: creative-arts.animation.blender.vse-meta-strips
name: vse-meta-strips
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-meta-strips, meta-strip]
level: practitioner
status: docs-checked
description: "Group VSE strips into meta strips: making, editing inside and separating metas, using them for effects on groups, compound clips and keeping sync."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/meta.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/adjustment.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-meta-strips

Goal: treat a group of strips as one clip, like a compound clip in other editors.

## Operations

- **Ctrl G**: Make Meta Strip from the selected strips. The meta spans from the earliest start to the latest end and collapses the contained channels into one strip.
- **Tab**: enter the meta to edit its contents (only its contents are shown). Tab again exits one level; with nested metas, deselect any meta first to exit further.
- **Ctrl Alt G**: UnMeta, restoring the strips to their original relative positions and channels.

## Uses

- Apply the same effect to several strips: group them, then add the effect strips to the meta.
- Organise sections of an edit such as an intro, a montage or lower-third graphics.
- Syncing multicam: group each camera with its audio and effects (the multicam workflow in the manual suggests this).
- An **Adjustment Layer** strip is the alternative that applies effects to all strips below without grouping.

## Behaviour

- A meta strip behaves like any other strip: it can be moved, trimmed, muted or have effects applied.
- Metas can be nested.
- Strip properties set on a meta act as a group master affecting the contained strips.
- The default blend mode of a meta strip is Replace. Change it if the result looks different from the original strips.

## Gotchas

- Check the blend mode on a new meta when the output looks wrong.
- Snapping to Frame Range inside a meta uses the meta strip's display range.

## Verify

Move the meta: all its picture and sound stays in sync. Enter it with Tab and check contents are unchanged.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Ctrl G, Ctrl Alt G and Tab behaviour, nesting and exit rule, Replace default blend mode, group-master properties, Adjustment Layer alternative. Removed copy and paste of metas, the nesting depth advice and the muted-strips claims, which the manual does not state.
- Method: documentation only; no commands were run.
