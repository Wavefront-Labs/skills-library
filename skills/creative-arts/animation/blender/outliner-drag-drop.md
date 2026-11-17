---
id: creative-arts.animation.blender.outliner-drag-drop
name: outliner-drag-drop
category: creative-arts
field: animation
product: blender
tags: [blender, outliner, outliner-drag-drop, move-to-collection, link-to-collection, parenting, collections]
level: practitioner
status: docs-checked
description: "Reorganise Blender scenes by Outliner drag and drop: move vs link to collections, parent by drop, copy modifier stacks, drop into the viewport, and M / Shift-M."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/usage.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# outliner-drag-drop

Goal: restructure hierarchies without breaking parenting, transforms or render membership.

## Moving and linking

- **Move:** drag an object or collection onto another collection.
- **Link:** hold `Ctrl` while dropping onto a collection. The same object or collection is then part of several parent collections at once (same data, not a copy).
- Drag-and-drop applies to the whole current selection; selected items that are incompatible with the operation are left unchanged.
- 3D Viewport equivalents (Object > Collection): **Move to Collection** `M` (menu offers existing collections, a new collection, or the Scene Collection) and **Link to Collection** `Shift-M`. To take objects out of collections: **Remove from Collection** `Ctrl-Alt-G`.

## Parenting by drop

- **Parent to object:** drag an object onto another object to make it a child. The manual says to hold `Alt` while dropping to *not* keep the transform relationship (the child retains its world position).
- **Clear parent:** drag the child out of its parent hierarchy; `Alt` while dropping clears the parent while preserving the parent's transform on the child.
- **Parent across collections:** hold `Shift` while dragging to parent an object that lives in a different collection.
- The manual's wording on the Alt modifier is terse; test on a throwaway object and compare `matrix_world` before and after (see Verify).

## Modifiers, constraints, visual effects

- Drag individual items inside the stack to reorder, or onto another object to copy them.
- Drag the group item (for example *Modifiers*) to copy the whole stack to another object; the target's existing stack is replaced.
- Apply and delete items from the context menu.

## Dropping into the 3D Viewport

- An object dragged from the Outliner creates a duplicate with its own copy of the object data.
- Object data dragged from the Outliner creates a linked duplicate that references the same object data.

## Gotchas

- Moving an object into an excluded collection removes it from the view layer (it is not deleted).
- Objects in several collections can confuse exporters that walk collections; prefer collection instances for repeated placement.
- Outliner *Delete* removes all usages of the data-block; use *Unlink* (or `Remove from Collection`) to leave other usages alone.
- Linked (library) data cannot be rearranged this way; make a library override first.

## Verify

`obj.users_collection` lists exactly the intended collections; children keep their world position (`matrix_world` unchanged).

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/usage.rst, editors/outliner/editing.rst, scene_layout/collections/collections.rst) and the current Python API (Object.users_collection).
Confirmed: move and Ctrl-link, parenting and Alt and Shift modifiers (as worded in the manual), modifier stack drag behaviour, viewport drop behaviour, M, Shift-M and Ctrl-Alt-G, Delete vs Unlink. Removed unconfirmed claims: drag a material onto an Outliner row, Shift-drag as "parent without moving collection" and a quoted tooltip, parenting keeping the object in the parent's collection by default, dropping into empty space to clear parent.
Method: documentation only; no commands were run.
