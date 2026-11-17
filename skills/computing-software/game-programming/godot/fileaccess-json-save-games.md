---
id: computing-software.game-programming.godot.fileaccess-json-save-games
name: fileaccess-json-save-games
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-save-game, fileaccess, json, persist-group, save-versioning, atomic-save, game-programming]
level: practitioner
status: verified
description: "Save and load Godot games with FileAccess and JSON: user:// paths, the persist-group pattern, type conversion pitfalls, versioning and crash-safe atomic writes."
sources: ["https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html", "https://docs.godotengine.org/en/stable/classes/class_fileaccess.html", "https://docs.godotengine.org/en/stable/classes/class_json.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FileAccess and JSON save games

**Goal:** a save system that writes human-readable data to `user://`, restores the world, survives
crashes mid-write and old save versions.

## Where
`user://` maps to a per-user writable folder (Windows `%APPDATA%/Godot/app_userdata/<project>` or a
custom dir via `application/config/use_custom_user_dir`; confirmed with `OS.get_user_data_dir()` and the data paths page). `res://` is read-only in exported games.
`OS.get_user_data_dir()` shows the real path.

## Collect state (persist group pattern from the docs)
Nodes that save themselves join a group (the docs call it `Persist`; any name works, just be consistent) and implement `save() -> Dictionary`:
```gdscript
func save() -> Dictionary:
    return {
        "scene": scene_file_path,               # to re-instantiate spawned nodes
        "parent": get_parent().get_path(),
        "pos_x": position.x, "pos_y": position.y,
        "health": health,
    }
```

## Write (atomically)
```gdscript
const SAVE_VERSION := 3
func save_game(slot: int) -> void:
    var data := {"version": SAVE_VERSION, "time": Time.get_unix_time_from_system(), "nodes": []}
    for n in get_tree().get_nodes_in_group("persist"):
        data.nodes.append(n.save())
    var path := "user://save_%d.json" % slot
    var tmp := path + ".tmp"
    var f := FileAccess.open(tmp, FileAccess.WRITE)
    if f == null: push_error("save failed: %s" % FileAccess.get_open_error()); return
    f.store_string(JSON.stringify(data, "\t"))
    f.close()                                         # flush before rename
    DirAccess.rename_absolute(tmp, path)              # replace only after a complete write
```
Writing straight to the real file risks a truncated save if the game crashes or the device powers
off mid-write.

## Read
```gdscript
func load_game(slot: int) -> void:
    var path := "user://save_%d.json" % slot
    if not FileAccess.file_exists(path): return
    var data = JSON.parse_string(FileAccess.get_file_as_string(path))
    if typeof(data) != TYPE_DICTIONARY: push_error("corrupt save"); return
    data = migrate(data)
    for n in get_tree().get_nodes_in_group("persist"): n.queue_free()   # clear current dynamic nodes
    await get_tree().process_frame
    for d in data.nodes:
        var node = load(d.scene).instantiate()
        get_node(d.parent).add_child(node)
        node.position = Vector2(d.pos_x, d.pos_y)
        node.health = int(d.health)                  # JSON numbers come back as float
```

## JSON pitfalls
- All numbers parse as `float` (`{"h": 12}` gives `12.0`); cast ints explicitly.
- Vector2/Color/etc. are not JSON types: `JSON.stringify({"a": Vector2(1, 2)})` gives the string `"(1.0, 2.0)"`, which
  does not parse back by itself. Store components (or `var_to_str`/`str_to_var` strings).
- `JSON.parse_string` on invalid text logs a parse error and returns null, which the `typeof(data) != TYPE_DICTIONARY` check catches.
- Dictionary keys become strings.
- Alternatives: `FileAccess.store_var(value)` (binary Variant, keeps types; never use
  `allow_objects=true` on untrusted files), or ConfigFile for settings.

## Versioning
`migrate(data)` upgrades step by step (`if data.version < 2: ...`); never break old saves silently.
Encrypt or checksum with `FileAccess.open_encrypted_with_pass` only if tamper-resistance matters;
it is not secure against determined players.

## Verify
- [ ] Kill the process during save: previous save remains loadable.
- [ ] Load a save from the previous version: migrates without errors.
- [ ] Integer fields keep integer type after load (no `12.0` in UI).
## Checked
Ran on Godot 4.7.2 headless: `.tmp` write then `DirAccess.rename_absolute` over an existing file replaces it on Windows (returns 0, content is the new text); `JSON.stringify` and `JSON.parse_string` behaviour quoted above; `FileAccess.get_file_as_string`; `use_custom_user_dir` table and the Persist group pattern from the Godot data paths and saving games docs. `save_game` and `load_game` ran end to end with a `persist`-group scene (one node at (3, 4), health 9: saved, freed, reloaded to the same position, health back as an int); `JSON.stringify` sorts keys alphabetically by default.
