---
id: creative-arts.animation.blender.override-resync
name: override-resync
category: creative-arts
field: animation
product: blender
tags: [blender, library-overrides, override-resync, resync, override-troubleshooting, broken-overrides, pipeline]
level: practitioner
status: docs-checked
description: "Fix broken Blender library overrides: automatic resync on load, Troubleshoot > Resync / Resync Enforce / Delete, Reset and Clear, and keeping asset hierarchies stable."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html
  - https://docs.blender.org/api/current/bpy.ops.outliner.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# override-resync

Goal: when the rigger changes the source file, shot files pick it up cleanly and keep their edits where possible.

## Why resync exists

The relationships between linked data-blocks can change, which leaves existing overrides outdated. Overrides must then be resynced to match the new structure of their hierarchy.

## Automatic resync

- Overrides are resynced automatically when needed as the blend-file opens. Auto resync can be disabled in the Experimental Preferences.
- Overrides of linked-in libraries are resynced too, but this is costly and redone on every load because Blender cannot modify the external library. Keep intermediate library files up to date: opening and saving them is typically enough.

## Manual operations

Outliner > context menu > Library Override > **Troubleshoot** (Object Mode; always applies to a whole override hierarchy). The operator is `outliner.liboverride_troubleshoot_operation`.

- **Resync:** rebuild the override from its linked reference and dependency hierarchy to match the new hierarchy. Warning: edited overrides can be deleted if they were changed in the original library; a message states how many were deleted and you can undo before saving.
- **Resync Enforce:** for older files saved with broken (non-hierarchy-matching) overrides where a regular resync cannot rebuild properly (for example objects go missing). It forces the hierarchy to match the linked data, ignoring existing overrides on data-block properties, at the cost of possibly losing some overrides on ID pointer properties.
- **Delete:** removes the whole override hierarchy and replaces all of it with the original linked data-blocks; fully reverts *Make*.

Also in the Library Override menu: **Reset** (back to linked values, overrides stay editable) and **Clear** (reset and delete overrides if possible, otherwise keep them non-editable).

## Pipeline rules

- Keep **all** collections the character needs as children of the linked, instantiated root collection; otherwise some data may not be overridden automatically and operations are less reliable.
- Pose-only (not animated) armature overrides are fragile: pose bones are tied to the Armature data, and they are lost for good if that data goes missing while the Armature itself is not overridden.
- Back up shot files before Resync Enforce (it is the more aggressive option; try Resync first).

## Verify

Reopen the shot: no resync warnings are reported, and scrubbing shows the pose and animation you expect.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/linked_libraries/library_overrides.rst) and the current Python API (bpy.ops.outliner.liboverride_troubleshoot_operation, liboverride_operation).
Confirmed: auto resync on open and how to disable it, Troubleshoot menu entries and their behaviour and warnings, Reset and Clear semantics, hierarchy advice, the pose-loss warning. Removed unconfirmed claims: console/Info report details, a symptom table (red icons, renamed bones, duplicate objects), name-stability and prefixing rules, and "Resync reapplies values by name".
Method: documentation only; no commands were run.
