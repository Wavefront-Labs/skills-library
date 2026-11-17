---
id: creative-arts.animation.principles.offset-keys-in-the-graph-editor
name: offset-keys-in-the-graph-editor
category: creative-arts
field: animation
product: principles
tags: [animation, follow-through-overlap, offset-keys, graph-editor, dope-sheet, overlap, cg, maya, blender, timing-offset, cycles]
level: practitioner
status: draft
description: "Create overlapping action in CG by offsetting curves in time per control, with amounts, cycle-safe offsets, and the Maya and Blender operations to do it."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offset keys in the graph editor

Goal: turn a block of controls that all move on the same frames into overlapping action by
sliding child controls' keys later, quickly and without breaking cycles.

## Amounts (24 fps starting points)
| Child relative to parent | Offset |
|---|---|
| Chest after hips | 1-2 frames |
| Head after chest | 1-3 frames |
| Forearm after upper arm | 1-2 frames |
| Hand after forearm | 1-2 frames |
| Each tail/hair segment | 1-2 frames, more toward tip |
Heavier or looser parts get more; tense characters get less.

## Method
1. Finish the parent's motion first.
2. Select the child's keys (or curves) in the Dope Sheet/Graph Editor and move them later in
   time. Blender: select channel keys, G then type the frame offset (e.g. G 2 Enter); Maya:
   select curves in the Graph Editor and use the Move tool with time snapping or shift keys
   with `keyframe -relative -timeChange 2`.
3. For **cycles**, make sure the curve is cyclic before offsetting so the shifted keys wrap
   (Blender: Cycles F-Curve modifier, Channel > Extrapolation Mode > Make Cyclic; Maya: Curves >
   Post/Pre Infinity > Cycle). Then shifting keys loops seamlessly.
4. Fix the start: offsetting non-cyclic curves leaves the child frozen for the first frames -
   add or extend a key at the start.
5. Re-check arcs and contacts after offsetting (feet and hands in contact must not be offset).

## Failure modes
- Offsetting IK controls that are in contact (planted feet, hands on a table): they slide.
- Same offset on every control: the whole body looks delayed, not overlapping.
- Offsetting keys on non-cyclic curves inside a cycle: a pop at the loop point.

## Verify
- [ ] Children reach their extremes after parents.
- [ ] Contacts still lock.
- [ ] Cycles loop without a pop at the last frame.

Related: `creative-arts.animation.principles.layered-animation`,
`creative-arts.animation.principles.appendage-overlap`.
