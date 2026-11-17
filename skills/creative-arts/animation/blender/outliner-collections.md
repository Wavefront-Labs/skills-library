---
id: creative-arts.animation.blender.outliner-collections
name: outliner-collections
category: creative-arts
field: animation
product: blender
tags: [blender, outliner, collections, collection-hierarchy, view-layers, scene-organisation, visibility, holdout, indirect-only, exclude, orphan-data, naming]
level: practitioner
status: docs-checked
description: "Organise a Blender scene with the Outliner: collection hierarchy, Object > Collection shortcuts, restriction toggles, display modes, view-layer settings and unused-data purge."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# outliner-collections

Goal: a scene where anyone can find, hide, render-isolate and link any part of it without hunting. Collections are Blender's organisational primitive; the Outliner is where you drive them.

## Collection model

- All scene objects belong to the special *scene collection*; you can make your own collections, nest them like folders, and an object can belong to several collections (a Venn-diagram arrangement).
- Object > Collection menu (Object Mode): **Move to Collection** `M`, **Link to Collection** `Shift-M` (keeps existing collections), **Create New Collection** `Ctrl-G`, **Remove from Collection** `Ctrl-Alt-G`, **Remove from All Collections** `Shift-Ctrl-Alt-G`, **Add Selected to Active Objects Collection** `Shift-Ctrl-G`, **Remove Selected from Active Collection** `Shift-Alt-G`, **Hide Other Collections** `Ctrl-H`.
- Collection properties tab: Visibility (Selectable, Show In Renders), View Layer (Include, Holdout, Indirect Only), Instancing (Instance Offset), Importer, Exporters, Line Art, Custom Properties.
- Linking collections between files works at collection level, so a character should be one top collection containing everything (see `creative-arts.animation.blender.append-vs-link`). Prefix naming (`CH_`, `SET_`, `FX_`) is a team convention, not a Blender feature.

## Restriction toggles (enable more via the filter popover)

| Icon | Name | Scope |
|---|---|---|
| checkbox | Exclude from View Layer | per view layer; contents hidden in viewport, render and Outliner |
| arrow | Disable Selection | collection/object |
| eye | Hide in Viewports (`H` over the viewport) | per view layer; still evaluated |
| screen | Disable in Viewports | all view layers; no longer evaluated |
| camera | Disable in Renders | all view layers |
| holdout | Holdout (collections) | per view layer |
| indirect | Indirect Only (collections, Cycles) | per view layer |

`Shift-LMB` on an icon applies it to the item and its children; `Ctrl-LMB` on a collection isolates it. See `creative-arts.animation.blender.collection-visibility` for details.

## Display modes (header)

- **Scenes**, **View Layer**, **Video Sequencer**.
- **Blender File:** all data in the file; the shield column shows user counts and toggles a fake user.
- **Data API:** every data-block with its properties.
- **Library Overrides:** Properties and Hierarchies view modes.
- **Unused Data:** data-blocks that are unused or have only a fake user; unused data-blocks are deleted when the file is saved and reloaded, or manually with **Purge**.
- **Purge** dialog options: Local Data-Blocks, Linked Data-Blocks, Recursive Delete. It cannot be undone. `File > Clean Up` holds **Purge Unused Data...** and **Manage Unused Data...**.

## Filter popover

Restriction Toggles, Sort Alphabetically, Sync Selection, Scroll to Active, Expand on Focus, Show Mode Column; under Search: Exact Match, Case Sensitive; under Filter: All View Layers, Collections, Objects, Object State, Object Contents, Object Children and per-type toggles. `Ctrl-F` focuses the search box, `Alt-F` clears it.

## Working in the Outliner

- Context menu (RMB): Delete, Delete Hierarchy, Select, Select Hierarchy, Deselect, Unlink; for collections New, Duplicate Collections (deep), Duplicate Linked (reuses object data), Instance to Scene, Visibility and View Layer submenus, Set Color Tag.
- Drag object or collection onto a collection: move; `Ctrl` while dropping: link. Drag object onto object: parent (see `creative-arts.animation.blender.outliner-drag-drop`).
- View: Show Active `.`, Expand/Collapse All `Shift-A`, Show Object Hierarchy `Home`, Show/Hide One Level `Numpad +` / `Numpad -`.
- Delete on an Outliner object removes all usages; the same keys over the 3D Viewport only unlink from the current scene.

## View layers

Each view layer has its own Exclude, Holdout and Indirect Only flags. Show all layers in the Outliner with the *All View Layers* filter (combine with Objects off for a compact overview).

## Cleanup before publishing a file

1. Outliner > Blender File: inspect Materials, Images, Actions and Node Groups for duplicates.
2. `File > Clean Up > Purge Unused Data...` with Recursive Delete on; give a fake user first to anything you want to keep (shield icon).
3. `File > External Data > Report Missing Files`; fix with Find Missing Files.

## Gotchas

- Fake user protects a data-block from being dropped on save; zero-user data is not written.
- Purge removes data you made but never assigned (for example a painted image).
- Linked data cannot take a fake user.

## Verify

- The needed restriction columns are visible and each collection has the intended flags.
- Unused Data mode is empty after a purge.
- Reopening the file shows no missing-file warnings.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/interface.rst, editors/outliner/editing.rst, editors/outliner/usage.rst, scene_layout/collections/*.rst, files/data_blocks.rst) and Blender 5.3 release source (scripts/startup/bl_ui/space_topbar.py for the File > Clean Up and External Data menus).
Confirmed: display mode names (including "Unused Data", not "Orphan Data" in this release), restriction toggle names and scopes, Object > Collection shortcuts, context menu entries, purge dialog options, filter options, keys. Removed unconfirmed claims: an `E` exclude shortcut, Alt-H and parent-checkbox behaviour, version-specific 4.2 notes, a File > Clean Up recursive entry, batch rename and Material Utilities hints, Compress advice, frame-time checks, collection drag into the viewport.
Method: documentation only; no commands were run.
