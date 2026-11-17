---
id: computing-software.game-programming.godot.inherited-scenes-and-editable-children
name: inherited-scenes-and-editable-children
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, inherited-scenes, editable-children, scenes, instancing, game-programming]
level: practitioner
status: draft
description: "Use Godot inherited scenes and Editable Children: when to inherit vs instance and compose, override behaviour, and fixing broken inheritance after renames."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html", "https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html", "https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inherited scenes and editable children

**Goal:** variants of a base scene (enemy types, level templates) that pick up base changes.

## Inherited scenes
Scene > **New Inherited Scene** (or right-click a `.tscn` > New Inherited Scene). The new scene's
root is the base scene; inherited nodes appear yellow-ish (greyed names) and can be modified but not
deleted or reordered. Saved file stores only differences:
```
[ext_resource type="PackedScene" path="res://enemies/enemy_base.tscn" id="1"]
[node name="Goblin" instance=ExtResource("1")]
speed = 140.0
[node name="Sprite2D" parent="." index="0"]
texture = ExtResource("2")
```
Change the base: every inherited scene updates, except properties it overrode.

## Editable Children
On an instanced scene in another scene, right-click > **Editable Children** exposes its internal
nodes for per-instance tweaks (e.g. move one spawn marker). Changes are stored in the parent scene
as overrides keyed by node path.

## When to use what
- **Inherit** for "is a" variants sharing structure (Goblin from EnemyBase) where the variant adds
  nodes or overrides properties.
- **Instance + exported properties** for configurable reusable parts; prefer this, since exported
  vars are an explicit API.
- **Editable Children** sparingly: per-instance overrides of internal nodes are invisible from the
  outside and break when the sub-scene renames nodes.
- Scripts: inherited scenes can attach a script that `extends "res://enemies/enemy_base.gd"` (or the
  class_name) to override methods, calling `super()`.

## Gotchas
- Renaming or moving nodes in the base breaks overrides in inherited scenes (paths no longer match);
  Godot warns about missing nodes and drops the overrides. Rename carefully, ideally early.
- Deep inheritance chains (base > variant > subvariant) get confusing; keep to one level.
- Clear Inheritance (Scene menu) makes a scene independent; irreversible.

## Verify
- [ ] Changing the base scene updates all variants; no "node not found" warnings on load.
