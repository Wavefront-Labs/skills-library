---
id: computing-software.game-programming.godot.save-slots-with-diraccess
name: save-slots-with-diraccess
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, save-slots, diraccess, save-games, user-path, file-io, game-programming]
level: practitioner
status: gated
description: "Build save slots in Godot 4 with DirAccess: listing user:// saves, slot metadata files, safe write-then-rename, deleting and migrating slots."
sources: ["https://docs.godotengine.org/en/stable/classes/class_diraccess.html", "https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html", "https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Save slots with DirAccess

**Goal:** a load screen that lists slots with timestamp, playtime and thumbnail, without loading
every full save.

## Layout
```
user://saves/
  slot_1.save      # full game state
  slot_1.meta      # small JSON: name, timestamp, playtime, level, version
  slot_1.png       # thumbnail (optional)
```

## List slots
```gdscript
const DIR := "user://saves"

func list_slots() -> Array[Dictionary]:
    DirAccess.make_dir_recursive_absolute(DIR)
    var out: Array[Dictionary] = []
    for f in DirAccess.get_files_at(DIR):          # static helper, no hidden/dirs
        if f.get_extension() != "meta":
            continue
        var meta = JSON.parse_string(FileAccess.get_file_as_string(DIR.path_join(f)))
        if meta is Dictionary:
            meta["slot"] = f.get_basename()
            out.append(meta)
    out.sort_custom(func(a, b): return a.timestamp > b.timestamp)
    return out
```

## Write safely
```gdscript
func save_slot(slot: String, data: Dictionary, meta: Dictionary) -> Error:
    var path := DIR.path_join(slot + ".save")
    var tmp := path + ".tmp"
    var f := FileAccess.open(tmp, FileAccess.WRITE)
    if f == null:
        return FileAccess.get_open_error()
    f.store_var(data)
    f.close()                                         # flush before rename
    var d := DirAccess.open(DIR)
    var err := d.rename(tmp, path)                    # replace old file only after a full write
    if err == OK:
        meta["timestamp"] = Time.get_unix_time_from_system()
        var m := FileAccess.open(DIR.path_join(slot + ".meta"), FileAccess.WRITE)
        m.store_string(JSON.stringify(meta))
    return err

func delete_slot(slot: String) -> void:
    for ext in ["save", "meta", "png"]:
        var p := DIR.path_join("%s.%s" % [slot, ext])
        if FileAccess.file_exists(p):
            DirAccess.remove_absolute(p)
```
Thumbnail: `get_viewport().get_texture().get_image()` then `resize()` and `save_png()` before
showing the pause menu (gated: unconfirmed, source is paywalled or blocked). The `resize()` and `save_png()` steps ran on a generated `Image`; `get_image()` on the viewport returned null under the headless dummy renderer, so it needs a real window to confirm.

## Gotchas
- `user://` maps to the OS app-data folder (configurable via `application/config/use_custom_user_dir`);
  `res://` is read-only in exports.
- On Windows `DirAccess.rename` onto an existing file replaces it (run: returned `OK` and the new content was in place, the `.tmp` file gone); still keep the previous save as
  `.bak` if corruption must be recoverable.
- Web exports store `user://` in IndexedDB and need cookies/IndexedDB allowed to persist (Godot export docs).
- Store a `version` in meta and migrate old saves on load; show "incompatible" instead of crashing.
- Don't use `store_var` with `full_objects = true` on untrusted saves (code execution risk).

## Verify
- [ ] Killing the game mid-save leaves the previous slot loadable.
- [ ] Slot list loads instantly with 50 slots (only meta files parsed).
## Checked
Ran on Godot 4.7.2 headless: `list_slots`, `save_slot` (twice on one slot, then a second slot after a 1.1 s wait) and `delete_slot` exactly as written; slots sorted newest first by `timestamp` (`["b:B", "a:A2"]`), `DirAccess.get_files_at` lists files only, `f.get_extension()`, `get_basename()`, `path_join`, and no `.tmp` left behind. Not confirmable here: the viewport thumbnail capture (marked above).
