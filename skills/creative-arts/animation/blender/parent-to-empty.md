---
id: creative-arts.animation.blender.parent-to-empty
name: parent-to-empty
category: creative-arts
field: animation
product: blender
tags: [blender, parenting, parent-to-empty, parent-empty, control-empty, hierarchy, group-transform, empties]
level: practitioner
status: docs-checked
description: "Group-transform objects in Blender with empty parents: pivot placement, Ctrl P parenting, nested root/offset/ctrl hierarchies and clean exports."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/parent.html
  - https://docs.blender.org/manual/en/latest/modeling/empties.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/clear.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# parent-to-empty

Goal: animate or move a group of objects from one sensible pivot without touching their own transforms.

## Recipe

1. Place the 3D cursor at the desired pivot (`Shift S` > *Cursor to Selected / Active*, or snap to a hinge vertex).
2. `Shift A` > *Empty* > Plain Axes / Arrows / Circle (Circle for animator controls). Name it `CTRL_door` or `GRP_table`.
3. Select children, then the empty last (active), `Ctrl P` > *Object* (or *Object (Keep Transform)*).
4. Animate the empty; children follow.

Avoid *Object → Parent → Make Parent without Inverse* here: it resets the Parent Inverse matrix and the child's local location, so the child moves to the empty's location.

## Control hierarchies

`ROOT` (world placement, rarely keyed) → `OFFSET` (layout tweak) → `CTRL` (animation) → geometry. Animators key only `CTRL`; layout moves `ROOT`. Zero transforms on `CTRL` at rest so *Alt G/R/S* resets the pose.

## vs Collections

- Collections organise; empties transform. Use both: collection `PROP_door`, empty inside as parent.
- A collection instance is itself an empty with one pivot; for linked assets prefer that.

## Gotchas

- Scaling the empty non-uniformly then rotating children produces shear; keep control empties uniformly scaled.
- Deleting the empty leaves its children unparented; use *Clear and Keep Transformation* (`Alt P`) first if they must stay in place.

## Verify

Rotate the empty 90°, undo: children return exactly; `child.parent.name` is the empty.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Parent, Empties, Clear, Snap and Delete pages). Confirmed: Ctrl P Set Parent To menu with Object and Keep Transform; Make Parent without Inverse resets the Parent Inverse matrix and local location; Clear and Keep Transformation; Empties as parents for a group of objects; Plain Axes, Arrows and Circle display types; Alt G, Alt R and Alt S clear transforms; Shift S Cursor to Selected. Corrected: the without-inverse entry name. Removed as unconfirmed: Delete Hierarchy and the FBX and glTF empty-export claims.

Method: documentation only; no commands were run.
