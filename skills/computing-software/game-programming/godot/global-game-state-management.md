---
id: computing-software.game-programming.godot.global-game-state-management
name: global-game-state-management
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, godot-global-state, game-state, autoload, save-data, state-reset, game-programming]
level: practitioner
status: docs-checked
description: "Manage global game state in Godot: a GameState autoload with typed data, change signals, reset for new games, separation from settings, and serialisation for saves."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html", "https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global game state management

**Goal:** progress data (inventory, flags, current level, gold) accessible everywhere, easy to save,
reset and test.

## Shape
```gdscript
# game_state.gd (autoload "GameState")
extends Node

signal gold_changed(value: int)
signal flag_set(flag: StringName)

var data := RunData.new()           # all mutable progress lives in one object

var gold: int:
    get: return data.gold
    set(v):
        data.gold = maxi(v, 0)
        gold_changed.emit(data.gold)

func set_flag(f: StringName) -> void:
    if data.flags.has(f): return
    data.flags[f] = true
    flag_set.emit(f)

func has_flag(f: StringName) -> bool: return data.flags.has(f)

func new_game() -> void: data = RunData.new()

func to_dict() -> Dictionary: return data.to_dict()
func from_dict(d: Dictionary) -> void: data = RunData.from_dict(d)
```
```gdscript
# run_data.gd
class_name RunData extends Resource
@export var gold := 0
@export var level := "res://levels/level_1.tscn"
@export var flags: Dictionary = {}
@export var inventory: Array[StringName] = []
func to_dict() -> Dictionary: return {"v": 1, "gold": gold, "level": level, "flags": flags, "inv": inventory}
static func from_dict(d: Dictionary) -> RunData:
    var r := RunData.new(); r.gold = d.get("gold", 0); r.level = d.get("level", r.level)
    r.flags = d.get("flags", {}); r.inventory.assign(d.get("inv", [])); return r
```

## Rules
- **All progress in one data object**: reset = replace it; save = serialise it; no stray vars on the
  autoload to forget.
- Setters emit signals so UI updates without polling.
- Keep **settings** (volume, keybinds) separate from **progress** (different files, different lifetimes).
- Scene-local state (enemy positions in a level) stays in the level; only persist what must survive.
- Version the save format (`"v": 1`) and migrate on load.

## Gotchas
- Resource files (`.tres`/`.res`) store the path of the script they use and load that script when loaded
  (Resources tutorial), so loading a resource is not the same as parsing plain data; for user-editable
  save files prefer JSON or `ConfigFile`, which the saving-games tutorial uses.
- Forgetting to reset on "New Game" leaks the previous run's flags; test new game after a full playthrough.

## Verify
- [ ] Save, quit, load restores every field; New Game after loading starts clean.
- [ ] UI updates via signals when state changes from anywhere.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the autoloads tutorial (autoload node with script, accessed by name), the Resources tutorial (resource files store their script path and load it), the saving-games tutorial (JSON and ConfigFile for saved data) and the Resource class page. The var_to_bytes remark was removed as unconfirmed. Remaining content is design guidance with no further checkable claims.

Method: documentation only; no commands were run.
