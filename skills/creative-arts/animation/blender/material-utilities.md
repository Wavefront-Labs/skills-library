---
id: creative-arts.animation.blender.material-utilities
name: material-utilities
category: creative-arts
field: animation
product: blender
tags: [blender, material-utilities, materials, material-slots, extensions, shift-q]
level: intro
status: docs-checked
description: "Use the Material Utilities extension (Shift Q): assign, select by material, copy to selected, clean slots, replace materials, set fake users and move slots across many objects."
sources:
  - https://extensions.blender.org/add-ons/material-utilities/
  - https://docs.blender.org/manual/en/4.1/addons/materials/material_utils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# material-utilities

Goal: fast batch material housekeeping in the 3D Viewport, especially on imported or kitbashed scenes.

## Install

The add-on was part of the Blender 4.1 bundled add-ons. It is now an extension on extensions.blender.org ("Material Utilities", community maintained, offered as it is with limited support, compatible with Blender 4.2 LTS and newer; version 2.2.3 when checked). Install it from Preferences > Get Extensions or drag the download into Blender. Menu: **Shift Q** in the 3D Viewport; also Properties > Materials > Specials (per the 4.1 manual).

## Main operations (as listed in the 4.1 manual)

| Command | Use |
|---|---|
| Assign Material | assign a material from a searchable list to the current selection |
| Select by Material | in Edit Mode selects faces with the material; in Object Mode selects all objects using it |
| Copy Material to Selected | copy the active object's material to selected objects |
| Clean Slots | for all selected objects, remove empty and unused slots (not assigned to any polygons); Object Mode only |
| Remove All Material Slots | remove all slots of the active object |
| Replace Material | swap one material for another, optionally for all objects in the file, otherwise selected editable objects |
| Set Fake User | give all materials a fake user, useful when saving materials for later |
| Slot to Top / Slot to Bottom | move a slot to the top or bottom of the stack |

The 4.1 manual lists **Change Material Link**, **Merge Base Names** and **Join by Material** but marks their documentation as "Todo". Read their tooltips and test on a copy of the file before relying on them.

## Typical clean-up after import (practice)

1. Run Clean Slots on the selected objects.
2. In the Outliner's Unused Data view, **Purge** deletes unused data-blocks (unused data-blocks are also dropped when the file is saved and reloaded, unless they have a fake user).
3. Inspect duplicate names such as `Wood.001` by hand and decide which to keep before replacing.

## Gotchas

- Replace Material and similar bulk tools are not undone by anything but Undo; save first.
- Edit-mode assign uses the active slot; check it before assigning.

## Verify

The material count in the Outliner Blender File view drops to the expected set, and no empty slots remain on cleaned objects.

## Checked

Checked 2026-10-27: extensions.blender.org listing (Location View3D Shift Q, community, 4.1 bundled, 4.2 LTS and newer, 2.2.3), Blender 4.1 manual page for the add-on (operation list, Clean Slots behaviour, Todo entries) and the Blender 5.2 manual Outliner Unused Data view (Purge, fake user, automatic deletion on save and reload). Removed behaviour claims for Merge Base Names, Change Material Link and Join by Material (undocumented) and the legacy Texface entries. Method: documentation only; no commands were run.
