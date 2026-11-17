---
id: creative-arts.animation.blender.graph-editor-normalize
name: graph-editor-normalize
category: creative-arts
field: animation
product: blender
tags: [blender, graph-editor, graph-editor-normalize, normalize-curves, view-all, only-selected-keyframes-handles, curve-visibility]
level: practitioner
status: docs-checked
description: "Read many F-curves at once in Blender's Graph Editor: Normalize (-1 to 1), Auto Normalization, framing, Show Only Selected, hide/reveal curves, handle display."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/introduction.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# graph-editor-normalize

Goal: compare timing and spacing across channels with very different ranges (rotation in radians vs location in metres vs custom props).

## Normalize

- Header **Normalize** scales the display of each curve so all appear to occupy the range -1 to 1. When enabled the view is zoomed accordingly and the area outside the normalized range is darkened. With a preview range defined, keys inside it are normalized and the others are scaled proportionally.
- **Auto Normalization** recalculates the normalization on every curve edit.
- Use for comparing the timing of peaks across channels and spotting which channel arrives late.
- Switch it off when you need to judge or type absolute values (for example a rotation of exactly 90 degrees).

## Focus tools

- **Frame All** (Home), **Frame Selected** (Numpad .).
- **Show Only Selected** (header): only curves of selected objects/bones. **Show Hidden** and **Show Only Errors** are next to it.
- Channel > Hide Selected Curves (H), Hide Unselected (Shift-H), Reveal Curves (Alt-H). The Hide toggle in a channel header hides one curve; Ctrl-click it to solo the channel.
- View > **Show Handles** (Ctrl-H) and **Only Selected Keyframes Handles** (handles only on selected keys) for a cleaner read.
- Channel search (Ctrl-F) filters channels by name, for example `rotation`.

## Workflow

1. Select the bone and isolate a curve with Shift-H.
2. Turn Normalize on to compare against another channel's timing (follow-through offsets).
3. Turn Normalize off to edit values precisely.

## Verify

With Normalize on, all visible curves span -1 to 1 and the peaks line up as expected.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Normalize and Auto Normalization behaviour, view shortcuts, filter names, hide/reveal shortcuts, solo with Ctrl-LMB, Show Handles and Only Selected Keyframes Handles, channel search. Removed as unconfirmed: that hidden curves are still keyed by I, per-editor normalization, midpoint remark.
Method: documentation only; no commands were run.
