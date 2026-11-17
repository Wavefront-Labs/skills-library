---
id: computing-software.game-programming.godot.exported-properties-and-annotations
name: exported-properties-and-annotations
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, export-annotations, export, inspector, export-range, export-group, game-programming]
level: intro
status: verified
description: "Expose GDScript properties to the inspector with @export and its variants (range, enum, flags, file, node types, groups, subgroups, tool buttons) and setters that react to edits."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html", "https://docs.godotengine.org/en/stable/classes/class_%40gdscript.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exported properties and annotations

**Goal:** designer-tunable values with sensible editors, ranges and grouping.

## Common annotations
```gdscript
@export var speed: float = 200.0
@export_range(0, 100, 1, "or_greater") var max_hp: int = 100      # "or_less", "exp", "suffix:px", "radians_as_degrees"
@export_enum("Melee", "Ranged", "Magic") var attack_type: int
enum Faction { PLAYER, ENEMY, NEUTRAL }
@export var faction: Faction = Faction.ENEMY                        # named enum = dropdown, stored as int
@export_flags("Fire", "Ice", "Poison") var immunities := 0
@export_flags_2d_physics var hit_layers := 1
@export_file("*.tscn") var next_level: String
@export_dir var save_dir: String
@export_multiline var description: String
@export_color_no_alpha var tint := Color.WHITE
@export var target: Node3D                                          # node reference (Godot 4)
@export var weapon_data: WeaponData                                 # custom Resource (class_name)
@export var drops: Array[PackedScene] = []
@export_node_path("Camera3D") var cam_path: NodePath
```

## Organising
```gdscript
@export_category("Combat")
@export_group("Damage", "dmg_")          # prefix is stripped in the inspector
@export var dmg_base := 10
@export var dmg_crit_mult := 2.0
@export_subgroup("Falloff")
@export var falloff_start := 5.0
@export_group("")                         # end group
```

## Reacting to edits
```gdscript
@tool
extends Sprite2D
@export var radius := 32.0:
    set(value):
        radius = value
        queue_redraw()                    # update in editor and game
```
- Setters run when the scene loads (before `_ready`, children may not exist); guard with
  `if not is_node_ready(): return` when touching child nodes.
- `@export_tool_button("Rebake", "Bake") var rebake := do_rebake` (the 4.4 docs page has it; the 4.3 page does not) adds an inspector button in tool scripts (property list: type 25 Callable, hint 39 with `Rebake,Bake`).
- `_validate_property(property)` to hide/disable properties conditionally; `notify_property_list_changed()` after changes.

## Gotchas
- Default value in the script vs saved value in the scene: the scene's saved value wins; changing the
  script default doesn't update existing instances that stored a value.
- Exporting a Resource shares one instance between scene copies unless "Local to Scene" is ticked or you
  `duplicate()` it.
- Untyped exports (`@export var x`) need a default to infer type: parse error "Cannot use simple "@export" annotation with variable without type or initializer, since type can't be inferred."

## Verify
- [ ] Inspector shows grouped, ranged fields; no raw ints where enums are intended.
- [ ] Editing a shared Resource on one enemy doesn't unexpectedly change all (or does, by design).
## Checked
Ran on Godot 4.7.2 headless: the whole annotation block above loaded as a `@tool` script and its `get_script_property_list()` shows each export (e.g. `@export_range(0, 100, 1, "or_greater")` gives hint string `0.0,100.0,1.0,or_greater`; `@export_flags_2d_physics` hint 8; `@export_file("*.tscn")` hint 13; `@export_dir` 14; `@export_multiline` 18; `@export_color_no_alpha` 21; `@export var target: Node3D` hint 34; `Array[PackedScene]` hint string `24/17:PackedScene`; `@export_node_path("Camera3D")` 26; category, group with prefix `dmg_`, subgroup and empty group reset all emitted as expected usage entries); suffix and `radians_as_degrees` hints; setter timing before `_ready` for a scene-stored export; untyped export parse error; shared Resource versus `resource_local_to_scene`. Group prefix hiding, `_validate_property` and `notify_property_list_changed` are from the Godot "GDScript exports" page and the 4.7.2 `Object` reference; the Inspector itself was not opened.
