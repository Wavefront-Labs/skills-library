---
id: creative-arts.animation.blender.bone-collections-management
name: bone-collections-management
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, bone-collections, bone-collections-management, bone-collection-solo, bone-collection-assign, rig-organisation]
level: practitioner
status: docs-checked
description: "Organise rig bones with Blender bone collections: create and nest, assign (M / Shift M), visibility and solo, library override limits for linked rigs."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/properties/bone_collections.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/bone_collections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bone-collections-management

Goal: animators see only controls; riggers can isolate MCH/DEF bones instantly.

## Basics (Armature Properties > Bone Collections)

- Bone collections were introduced in Blender 4.0 as a replacement for armature layers and bone groups; they belong to the Armature, so they exist in all modes, and names are unique within the armature. The panel is a tree view: create, delete and re-arrange; rename by double-clicking or right-click > Rename.
- Nest by dragging a name onto another collection, or right-click > Add Child Collection.
- **Assign / Remove** put the selected bones into or out of the active collection; **Select / Deselect** act on the bones in the active collection. A bone can be in several collections.
- In Pose or Edit Mode, **M** = Move to Collection (unassigns the selection from all other collections, then assigns); **Shift M** = Bone Collections menu where entries prefixed + assign and - unassign the selection.
- Eye icon = visible; **Solo** (star) shows only soloed collections. A dot marks collections that hold bones. Specials menu: Show All, Un-Solo All, Remove Unused.
- Visibility rules: a hidden bone is always invisible; hidden parent collection hides its children; a bone is visible when in any visible collection; a soloed collection is visible regardless of its hidden flag; a bone in no collection is visible.

## Conventions

- Keep animator-facing collections in a predictable order and name them consistently (for example `Controls`, `Face`, `Fingers`).
- Bone colours are stored on the bone, not the collection: assign them consistently per collection, with a script or the Bone Properties colour fields.

## Linked rigs

- New bone collections can be added on a library-overridden rig, but both the armature object and the Armature data must be overridden. Only collections local to the current file are editable; collections from the linked armature are read-only, and their visibility can be toggled but those changes are not saved. Custom properties of overridden collections cannot be edited in the UI (Python is fine).
- Collections added by overrides are anchored to the preceding collection by name.

## Gotchas

- A bone that is hidden itself, or only in hidden collections, will not show in the viewport; check the bone's Hide flag and its collections' visibility.
- Move to Collection and the Bone Collections menu only list editable collections, so linked rigs need overrides first.

## Verify

Toggle each collection: only its bones hide/show; solo isolates; animators' default view shows only controls.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bone Collections (armature properties and bones) pages: introduction in 4.0, nesting, M and Shift-M menus, Assign/Remove/Select/Deselect, Solo, Specials, visibility rules, library override limitations. Removed unconfirmed 4.1 nesting gate, layer migration naming, Python collections API note, Rigify layout and hidden-by-default conventions, and corrected the claims about overrides and unassigned bones.

Method: documentation only; no commands were run.
