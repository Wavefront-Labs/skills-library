---
id: creative-arts.animation.blender.vse-snapping-overlap
name: vse-snapping-overlap
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-snapping, overlap-mode, editing]
level: practitioner
status: docs-checked
description: "Control VSE snapping and overlap behaviour: snap targets (playhead, strip edges, markers), overlap modes overwrite, expand and shuffle, and ripple-like editing."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-snapping-overlap

Goal: predictable cuts and moves without accidental overwrites.

## Snapping

Toggle snapping with the snap icon in the header, or temporarily by holding **Ctrl** while dragging a strip. The drop-down arrow offers:

- **Snap to**: Frame Range (preview or scene range, or the meta strip's display range inside a meta), Current Frame (playhead), Hold Offset, Markers, Retiming Keys, and All Channels (without it, strips only snap to strips on the same channel).
- **Ignore**: Muted Strips and Sound Strips are not used as snap targets.

## Overlap Mode (sequencer tool setting)

What happens when a transformed strip lands on another:
- **Expand**: strips to the right of the transformed strip are shifted forward to make room (an insert edit).
- **Overwrite**: the overlapped strip is overwritten, trimmed or split by the overlapping strip.
- **Shuffle**: the overlapping strip is moved to the nearest free space so nothing overlaps.

## Gaps (Strip > Transform)

- **Remove Gaps** (Backspace): removes blank frames between the current frame and the first strip to the left, regardless of selection or lock state. Enabling All Gaps also removes gaps to the right. **Remove Gaps (All)** is the same with All Gaps on.
- **Insert Gaps** (Shift Equals): inserts blank frames between the current frame and the first strips to the right.
- **Move/Extend from Current Frame** (E) changes strip handles on the mouse side of the playhead together, useful for adjusting an animatic.

## Gotchas

- Overwrite trims or splits other strips. Check the result after big moves.
- Sound strips as snap targets can pull a picture strip onto a beat. Turn them off in Ignore when snapping picture.
- Move linked picture and sound together by selecting both, or group them in a meta strip.

## Verify

Drag a clip onto another with each overlap mode: Overwrite trims, Expand pushes, Shuffle finds a free spot.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Snap toggle and Ctrl while dragging, Snap to entries, Ignore entries, Overlap Mode Expand/Overwrite/Shuffle definitions, Remove Gaps (Backspace, All Gaps), Insert Gaps (Shift Equals), Move/Extend (E). Removed the Strips target, the Shift Backspace key and the default-mode claim, which the 5.2 manual does not give.
- Method: documentation only; no commands were run.
