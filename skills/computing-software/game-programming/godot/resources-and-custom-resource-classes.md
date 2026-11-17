---
id: computing-software.game-programming.godot.resources-and-custom-resource-classes
name: resources-and-custom-resource-classes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, resource, custom-resource, tres, export, duplicate, resourceloader, resourcesaver, data-driven-design, unique-shared, inspector, game-programming]
level: practitioner
status: verified
description: "Model shared game data in Godot with custom Resource classes (.tres), and avoid the shared-instance bug that corrupts save data across objects."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resources and custom Resource classes in Godot

**Goal:** define reusable, Inspector-editable game data (weapon stats, enemy
configs, dialogue) without hardcoding it in scripts or scattering it across
scene instances — Godot's `Resource` is the equivalent of Unity's
ScriptableObject, with the same shared-instance trap.

## Defining a custom Resource
```gdscript
# weapon_data.gd
extends Resource
class_name WeaponData

@export var name: String = "Sword"
@export var damage: int = 10
@export var cooldown: float = 0.5
@export var icon: Texture2D
```
Save an instance as a `.tres` file (right-click in FileSystem → New Resource →
pick `WeaponData`), fill in values in the Inspector, and reference it from any
node:
```gdscript
@export var weapon: WeaponData
func fire():
    deal_damage(weapon.damage)
```
`.tres` is a human-readable text format (diffable in version control); `.res`
is binary — prefer `.tres` for anything hand-edited and version-controlled.

## The shared-instance bug (the Unity SO trap, Godot edition)
A `Resource` loaded from disk is **one shared instance** across every node that
references the same `.tres` file (Godot caches resources by path by default; run: two `load()` calls returned the same
object and `a1.damage = 99` was visible through `a2`).
If one enemy mutates `weapon.damage` at runtime (a buff, a debug tweak), **every
other node referencing that same resource sees the change** — because they're
the same object, not copies. Fixes:
- Call `.duplicate(true)` (deep duplicate, recurses into sub-resources) when you
  need a per-instance mutable copy: `weapon = base_weapon_data.duplicate(true)` (run: changing the copy left the
  original at 99).
- For a resource stored inside a scene that should be unique per instantiation, set `resource_local_to_scene = true`
  on it (run: a `WeaponData` sub-resource with that flag in a `.tscn` was a different object in each instance, and
  changing one left the other at 5). A resource saved in its own `.tres` file is shared unless duplicated.
- Treat any `Resource` you load via `load()`/`preload()` as read-only by
  convention unless you've explicitly duplicated it — this is the single most
  common "why did every enemy's health change when I hit one" bug report.

## Saving at runtime
`ResourceSaver.save(my_resource, "user://save_slot_1.tres")` writes a Resource
out (returns 0 / `OK`; run) — useful for save games built from custom Resource classes (a `SaveData`
resource holding player stats) rather than hand-rolled JSON/dict serialization.
Caveat: don't save to `res://` at runtime (the Godot docs say the project file system is likely read-only while the game runs);
always `user://` for anything written during play. The saved text file records the
script by path (`[ext_resource type="Script" path="res://wd.gd" ...]`) and lists changed properties
(`damage = 20`); referenced assets are stored by path too, so moving or renaming them breaks the reference.
**Security:** `load()` of a `.tres` runs any script embedded in it (run: a `.tres` with a built-in GDScript printed from
its `_init` on `load()`), so never `load()` resources from untrusted sources such as downloaded save files.

## Resources vs autoloads vs plain dictionaries
- **Autoload singleton**: runtime global *state* (score, current scene manager).
  Not for data definitions — it's one instance, not a swappable asset.
- **Dictionary/JSON**: fine for genuinely external data (a CSV of localization
  strings) but loses type safety, Inspector editing, and `class_name` polymorphism.
- **Custom Resource**: the right choice for designer-tunable, typed, reusable
  definitions — the Godot analogue of a data table.

## Verify
- [ ] Any Resource mutated at runtime is explicitly `.duplicate()`d first, or
      marked local-to-scene/unique; two instances sharing a `.tres` never see
      each other's runtime changes.
- [ ] Save data uses `user://`, never writes back to `res://`.
- [ ] Custom Resource classes declare `class_name` so they're selectable by type
      when creating a new resource in the editor, not just via a generic
      "Resource" picker.
## Checked
Ran on Godot 4.7.2 headless: `class_name WeaponData` resource with exports; `ResourceSaver.save` to `user://w.tres` and its text output (also succeeded to `res://` in a headless run from the project folder, which is not an export); `load()` caching and shared mutation; `duplicate(true)`; `resource_local_to_scene` sub-resource in a scene instanced twice; embedded-script `.tres` executing on `load()`. `.tres` text versus `.res` binary and `class_name` visibility in the New Resource dialog are from the Godot "Resources" docs page; the read-only note from the "File paths in Godot projects" page.
