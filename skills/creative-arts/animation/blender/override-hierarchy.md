---
id: creative-arts.animation.blender.override-hierarchy
name: override-hierarchy
category: creative-arts
field: animation
product: blender
tags: [blender, library-overrides, library-override, override-hierarchy, override-editable, system-override, linked-character]
level: practitioner
status: docs-checked
description: "Make linked Blender assets editable with library overrides: Make, Reset, Clear, selected vs content, editable vs non-editable overrides, and the Outliner Library Overrides view."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/api/current/bpy.ops.outliner.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# override-hierarchy

Goal: animate and tweak a linked character or prop without breaking its link to the source file.

## Why hierarchy matters

An asset is a tree of dependent data-blocks (armature, geometry, controllers, materials and so on) with a root data-block that is usually the collection you link. Blender overrides the whole dependency tree so relationships stay consistent, and it identifies each data-block with one override hierarchy, which matters when the same character is in the scene several times. For this to work well, all collections the character needs should be children of the linked, instantiated root collection.

## Make an override

- Menus: `3D Viewport > Object > Library Override > Make`, `Outliner > context menu > Library Override > Make`, or the ID widget's context menu. `Shift-LMB` on the "linked" button of an ID widget also works. Object Mode; ID widget support (mainly the Properties editor) is limited.
- 3D Viewport: the selected objects count as selected. For a selected local empty instancing a linked collection, the empty is removed, the collection is overridden and its override is instanced in the same collection of the current view layer; armatures in it become user-editable, otherwise no created override is editable.
- Outliner: apply to **Selected**, **Content**, or **Selected & Content** (the operator's `selection_set`). *Selected & Content* makes all newly created overrides immediately user-editable.
- Only overrides created from selected items are user-editable; most others are marked non-editable by default to reduce unwanted edits. Running Make again on existing overrides makes them editable.

## Reset and Clear

- **Reset:** back to linked values; overrides stay fully editable and are not deleted.
- **Clear:** resets and, if possible without breaking the hierarchy, deletes the overrides and replaces them with the linked data; otherwise keeps them as non-editable.
- Troubleshoot > Resync, Resync Enforce, Delete: see `creative-arts.animation.blender.override-resync`.

## Outliner > Library Overrides display mode

- **Properties:** data-blocks with overridden properties grouped by type; expand to see and change them (the audit trail).
- **Hierarchies:** tree of overridden data-blocks including implicitly overridden parents, with a column of icons to toggle whether each override is editable.
- Filter option *System Overrides* shows properties defined or controlled automatically (such as pointers to overridden data).

## Editing an override

- Edited properties show with a teal-blue outline or background. Context menu on a property: Add Override(s), Add Single Override, Remove Override(s), Remove Single Override.
- Edit Mode is not allowed on overrides.
- New modifiers and constraints can be added anywhere in the stack.
- Animation: keyframes live in an Action; a purely local Action can replace a linked one but replaces it completely. Overridden Actions only allow very limited editing (an F-Curve can be muted, its keys cannot be edited). Drivers and NLA follow the rules in the manual's "Animation & Overrides" section.

## Gotchas

- Posed (not animated) armature objects whose Armature data is not overridden lose their pose if the library goes missing.
- Custom properties need the *Library Overridable* option to be editable (see `creative-arts.animation.blender.library-overridable-props`).
- The old proxy system was deprecated in 3.0 and removed in 3.2; files convert to overrides on load.

## Verify

Save and reopen: pose keys survive, and the Outliner Properties view lists only the intended properties.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/linked_libraries/library_overrides.rst, editors/outliner/interface.rst) and the current Python API (bpy.ops.outliner.liboverride_operation).
Confirmed: menu paths, selection rules per editor, Selected / Content / Selected & Content, Reset and Clear semantics, editable toggle column, edit restrictions, animation notes, proxy removal versions. Removed unconfirmed claims: a "Make Editable" context entry (Make is used for that), "unsupported edits are not saved", "inserting before linked modifiers is not allowed" and a list of overridable property types.
Method: documentation only; no commands were run.
