---
id: creative-arts.animation.blender.pivot-constraint
name: pivot-constraint
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, pivot-constraint, rotation-pivot, foot-roll, rolling-objects, rigging]
level: practitioner
status: docs-checked
description: "Rotate around a different point with Blender's Pivot constraint: target or pivot point, relative offset, and the rotation range trigger (always, positive or negative axis)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/pivot.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# pivot-constraint

Goal: let an object/bone rotate around a pivot that isn't its origin — and only in certain rotation directions.

## Settings

- **Target** (object or bone, optional): the pivot point. With no target the pivot is relative to the owner or fixed in space.
- **Use Relative Offset** (only when no Target is set): whether the Pivot Point coordinates are relative to the owner or absolute in the world. With a Target the coordinates are always relative.
- **Pivot Point X/Y/Z**: the coordinates of the pivot.
- **Rotation Range**: *Always*, or only when the owner's X/Y/Z rotation is positive or zero (X/Y/Z Rotation) or negative or zero (-X/-Y/-Z Rotation). That makes direction-dependent pivots.

## Recipes

- **Foot rocking side to side**: on the foot control, two Pivot constraints — one with the pivot at the outer edge and Rotation Range Y Rotation, one at the inner edge with -Y Rotation. Result: the foot tips on the correct edge depending on rotation direction.
- **Tipping a box**: Pivot at the bottom edge with Rotation Range X Rotation; another at the opposite edge with -X Rotation.
- **Heel-toe roll** (simpler than full reverse foot): pivot at heel for backward rotation, toe for forward.

## Gotchas

- A target object or empty can be moved to change the pivot point interactively.

## Verify

Rotate the control in each direction: object pivots on the expected edge, without sliding.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Pivot constraint page: Target, Use Relative Offset, Pivot Point X/Y/Z, Rotation Range choices (Always, positive-or-zero, negative-or-zero). Removed unconfirmed remarks about translation-only effects and stack placement.

Method: documentation only; no commands were run.
