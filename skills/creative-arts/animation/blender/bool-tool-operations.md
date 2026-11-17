---
id: creative-arts.animation.blender.bool-tool-operations
name: bool-tool-operations
category: creative-arts
field: animation
product: blender
tags: [blender, bool-tool-operations, bool-tool-auto, bool-tool-brush, bool-tool, hard-surface, bundled-addons]
level: intro
status: docs-checked
description: "Use the Bool Tool add-on: Auto Boolean shortcuts that apply instantly, Brush Boolean that keeps live cutters, slice, and applying or removing brushes later."
sources:
  - https://extensions.blender.org/add-ons/bool-tool/
  - https://github.com/nickberckley/bool_tool
  - https://docs.blender.org/manual/en/4.1/addons/object/bool_tools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bool-tool-operations

Goal: fast boolean operations from the keyboard in Object mode.

## Install

Bundled with Blender up to 4.1 (*Object: Bool Tool*); after that it is an extension on extensions.blender.org. The current extension (2.1.0, maintained by a different author) requires Blender 4.5 or newer. Panel: sidebar `N` → *Edit* tab → *Boolean*; popup menu `Ctrl Shift B`.

Select the cutter(s) first, the base object (the canvas) last so it is active. The redo panel has *Flip*, which treats the active object as the single cutter and the other selected objects as canvases.

## Auto Boolean (destructive, applies immediately)

| Shortcut | Operation |
|---|---|
| `Ctrl Shift Numpad -` | Difference |
| `Ctrl Shift Numpad +` | Union |
| `Ctrl Shift Numpad *` | Intersect |
| `Ctrl Shift Numpad /` | Slice |
The modifiers are applied immediately (by default all modifiers on the canvas) and the cutter objects are deleted. If the canvas has shape keys or shared mesh data, a confirmation pop-up appears first.

## Brush Boolean (non-destructive)

| Shortcut | Operation |
|---|---|
| `Ctrl Numpad -` | Difference |
| `Ctrl Numpad +` | Union |
| `Ctrl Numpad *` | Intersect |
| `Ctrl Numpad /` | Slice (cuts the canvas with Difference and keeps the intersecting part as a separate object) |
Adds a Boolean modifier on the canvas for each cutter. The cutter is excluded from renders, parented to the canvas if it has no parent, and shown as bounds or wire (set in the add-on preferences), so it stays editable.

## Managing brushes

The *Cutters* panel (sidebar *Edit* tab, shown when the active object is a canvas) lists the cutters, with Apply (checkmark) and Remove (X) buttons for the selected cutter. The dropdown beside the list holds the other utility operators (toggle, select, apply, remove).

## Gotchas

- Laptops without a numpad: use the `Ctrl Shift B` menu, or enable Preferences → Input → *Emulate Numpad* (the number keys then act as numpad keys).
- Auto operations are destructive: save or duplicate before.
- The solver of the created modifiers comes from the add-on preferences.

## Verify

`Ctrl Numpad -` with a cylinder over a box adds a Boolean modifier and the cylinder displays as bounds or wire; moving it updates the hole; applying the cutter from the *Cutters* panel leaves a single mesh.

## Checked

2026-10-27. Sources: Bool Tool extension 2.1.0 (extensions.blender.org listing, blender_manifest.toml, add-on documentation pages and source in the nickberckley/bool_tool GitHub repository, read through the GitHub API) and the Blender 4.1 manual add-on page; Blender manual 5.2 Preferences > Input. Confirmed: Brush Boolean is Ctrl+Numpad and Auto Boolean is Ctrl+Shift+Numpad (the earlier text had them swapped); Ctrl Shift B menu; Edit sidebar tab with Boolean, Cutters and Helpers panels; Emulate Numpad; extension requires Blender 4.5 or newer. Removed: the Apply All/Remove All/Toggle button names, which the extension panel does not use. Note: the Blender 4.1 manual page for the bundled version lists the shortcut groups the other way round and has TODO entries; behaviour here follows the current extension documentation.

Method: documentation only; no commands were run.
