---
id: creative-arts.animation.blender.action-slots
name: action-slots
category: creative-arts
field: animation
product: blender
tags: [blender, animation, action-slots, slotted-actions, actions, layered-actions, python-api]
level: practitioner
status: docs-checked
description: "Understand Blender slotted actions (4.4+): one action animating several data-blocks via slots, assigning slots, why action.fcurves scripts break, and migrating pipelines."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/actions.html
  - https://docs.blender.org/api/current/bpy.types.Action.html
  - https://docs.blender.org/api/current/bpy.types.ActionSlot.html
  - https://docs.blender.org/api/current/bpy_extras.anim_utils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# action-slots

Goal: work with the action data model where an action contains **slots**, one per animated data-block, so a single action can hold e.g. an object's and its material's animation together.

## Concepts

- **Slot**: a named set of animation data inside an action. An animated data-block specifies both an action and a slot. A slot is not tied to any data-block; two characters can share one slot.
- Each slot has a name and an associated data-block type (object, material...), set when it is first assigned. Name plus type must be unique within an action; clashes get `.001` suffixes.
- Python `slot.identifier` is the ID-type prefix plus the name (for example `OBSuzanne` and `MESuzanne` can coexist; the name `Suzanne` is shared).
- Layers and strips exist inside actions but are not exposed in the UI; they are exposed in the Python API.

## Working in the UI

- Properties editor > Animation panel (per data-block) and the Action Editor header have action and slot selectors.
- Assign an action and leave the slot blank: a new slot is created on the first key.
- Selecting an action auto-picks a slot by name and type; if none fits the selector stays empty, so pick one, create one, or start keying. The dropdown lists only slots whose type matches the data-block.
- Action Editor Action menu: **Merge Animation** (merges selected objects' animation into the active object's action), **Separate Slots** (splits slots into separate actions), **Move Slots to new Action**.

## Python

- `action.fcurves` and `action.groups` do not exist in the 5.2 API reference; F-curves live in channelbags: `action.layers[0].strips[0].channelbag(slot).fcurves`. Scripts written for pre-4.4 actions need porting.
- Assign: `ob.animation_data.action = act` then `ob.animation_data.action_slot = act.slots[0]`; compatible slots are in `animation_data.action_suitable_slots`.
- Helpers in `bpy_extras.anim_utils`: `action_get_channelbag_for_slot(action, slot)`, `action_ensure_channelbag_for_slot(action, slot)`, `action_get_first_suitable_slot(...)`.
- Create a slot: `act.slots.new(id_type='OBJECT', name="Suzanne")` gives identifier `OBSuzanne`.
- Third-party importers, exporters and add-ons written for older versions may not handle slots: test pipelines.

## Gotchas

- Assigning a slot of the wrong type to a data-block is possible but animates nothing.
- Keying heuristics reuse one action for closely related data-blocks (object and its data, mesh and its shape keys, material and node tree) with a separate slot for each; a data-block with several users gets its own action.

## Verify

`for s in act.slots: print(s.identifier, s.users())` lists the expected slots and users; each object shows correct animation after assignment.

## Checked

2026-10-27, Blender 5.2 manual and Python API reference (current): slot concept, naming and type rules, manual assignment, Action menu operators, identifier prefix behaviour, `users()`, `action_suitable_slots`, anim_utils helpers, absence of `Action.fcurves` and `Action.groups`. Removed as unconfirmed: slot delete-menu claim, per-version layer counts, the KE prefix.
Method: documentation only; no commands were run.
