---
id: creative-arts.animation.blender.outliner-selection-sync
name: outliner-selection-sync
category: creative-arts
field: animation
product: blender
tags: [blender, outliner, outliner-selection-sync, outliner-context-menu, select-hierarchy, hierarchy]
level: practitioner
status: docs-checked
description: "Drive selection from Blender's Outliner: Sync Selection, range and child selection, keyboard navigation, expand/collapse, Show Active and the context-menu select operations."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/selecting.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# outliner-selection-sync

Goal: select whole hierarchies, ranges and hidden items from the Outliner and keep viewport and Outliner selection consistent.

## Sync Selection

- Filter popover > **Sync Selection** (on by default): Outliner selection is synchronised to and from the 3D Viewport and the Video Sequencer; selecting data-blocks selects the respective objects, bones and sequences there.
- With it off, the context menu entries **Select** (adds the Outliner selection to the viewport selection) and **Deselect** do the transfer on demand. Turn it off in a second Outliner used for browsing so clicks do not disturb the viewport selection.
- Clicking the icon (not the name) of an item switches the Properties editor to the relevant tab; disable with the Properties editor's *Sync with Outliner* option.

## Selection gestures

- `LMB` selects and activates a single data-block; clicking empty space below the list deselects all.
- `Ctrl-LMB` extends the selection (each added item becomes active). `Shift-LMB` selects a range from the active element; `Shift-Ctrl-LMB` selects a range without deselecting the previous selection.
- Children: click the icon displayed right of the parent's name, or double-click an item's icon, to select all its children. Context menu **Select Hierarchy** adds the children of the selected items (to the viewport too when Sync Selection is on).
- Box select: drag from anywhere that is not a name or icon, or press `B`; `Shift` adds and `Ctrl` subtracts. `A` selects all, `Alt-A` deselects all.
- Keyboard: `Up`/`Down` move, `Shift-Up`/`Shift-Down` extend, `Left`/`Right` close/open or move to parent/first child, `Shift-Left`/`Shift-Right` close/open an item and all its children.

## Navigation

- **Show Active** `.` centres the tree on the active item; **Expand/Collapse All** `Shift-A`; **Show Object Hierarchy** `Home`; **Show/Hide One Level** `Numpad +` / `Numpad -`.
- Filter options *Scroll to Active* and *Expand on Focus* do this automatically when the active item changes outside the Outliner.

## Context menu (RMB on icon or name)

- Items: Copy/Paste, Delete `X`/`Delete`, Delete Hierarchy, Select, Select Hierarchy, Deselect, Unlink.
- Collections: New, Duplicate Collections, Duplicate Linked, Instance to Scene, Visibility, View Layer, Set Color Tag.
- Data-block submenu: Unlink, Make Local, Delete, Remap Users, Add/Clear Fake User, Rename `F2`, Select Linked, Pack. (Make Single User there is documented as not functional; use the user-count button in the data-block selector.)

## Gotchas

- *Delete Hierarchy* on a collection does not delete child objects that also belong to another collection.
- Outliner *Delete* removes all usages; use *Unlink* to remove only the current one.

## Verify

After *Select Hierarchy*, `len(context.selected_objects)` equals 1 + `len(obj.children_recursive)` (for a single selected parent with Sync Selection on).

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/selecting.rst, editors/outliner/editing.rst, editors/outliner/interface.rst) and the current Python API (Object.children_recursive).
Confirmed: Sync Selection scope, click, Ctrl, Shift and Shift-Ctrl range behaviour, child selection by icon, B, A, Alt-A, arrow keys, Show Active and expand keys, context menu entries, Make Single User note, Delete Hierarchy rule. Removed unconfirmed claims: the `Shift-G` and `]` viewport equivalents, "Shift = range, Ctrl = extend" as a 4.x convention, `Ctrl`-click rename, Delete on a collection moving objects to the parent, and excluded-collection selection behaviour.
Method: documentation only; no commands were run.
