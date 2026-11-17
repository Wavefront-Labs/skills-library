---
id: computing-software.game-programming.godot.res-and-user-paths
name: res-and-user-paths
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-save-game, user-path, res-path, diraccess, file-system, custom-user-dir, exported-files, game-programming]
level: intro
status: verified
description: "Understand Godot res:// and user:// paths: read-only exports, user:// location per OS, DirAccess listing, and loading non-imported files at runtime safely."
sources: ["https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html", "https://docs.godotengine.org/en/stable/classes/class_diraccess.html", "https://docs.godotengine.org/en/stable/tutorials/io/runtime_file_loading_and_saving.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# res:// and user:// paths

**Goal:** read game data and write player data from the right places, so code that works in the
editor also works in exported builds on every platform.

## res:// (project resources)
- Points to the project folder in the editor; inside the exported **PCK** in builds.
- Treat as **read-only** in exported projects (the Godot docs: the project file system is likely read-only while the game runs).
  Writing to `res://` worked when running from the project folder (`ResourceSaver.save(..., "res://w2.tres")` returned `OK` in a headless run), which is
  the classic bug: the save system works in testing and fails in release.
- Exported builds contain **imported** versions of assets: `res://icon.png` is loaded through
  `load()` from `.godot/imported/...ctex`; the original PNG is not in the PCK unless you add it to the
  export filter "Filters to export non-resource files" (e.g. `*.json, *.txt, levels/*.csv`).

## user:// (writable per-user data)
| Platform | Default location |
|---|---|
| Windows | `%APPDATA%/Godot/app_userdata/<Project Name>/` |
| macOS | `~/Library/Application Support/Godot/app_userdata/<Project Name>/` |
| Linux | `~/.local/share/godot/app_userdata/<Project Name>/` |
| Android/iOS/Web | App sandbox / IndexedDB-backed storage on web |
With **Project Settings > Application > Config > Use Custom User Dir** (+ Custom User Dir Name), it
becomes `%APPDATA%/<Name>/` etc., which looks more professional for shipped games.
`OS.get_user_data_dir()` returns the absolute path (run: `.../Godot/app_userdata/rv137` under `%APPDATA%` for a project named `rv137`);
`ProjectSettings.globalize_path("user://x")` converts any virtual path (run: `.../app_userdata/rv137/x`).

## Working with directories
```gdscript
func list_saves() -> PackedStringArray:
    DirAccess.make_dir_recursive_absolute("user://saves")
    var out := PackedStringArray()
    for f in DirAccess.get_files_at("user://saves"):
        if f.ends_with(".json"): out.append(f)
    return out

func delete_save(name: String) -> void:
    DirAccess.remove_absolute("user://saves/" + name)
```

## Loading non-resource files at runtime
- Text/JSON shipped with the game: include via export filter, read with
  `FileAccess.get_file_as_string("res://data/items.json")`.
- User-provided images/audio (mods, screenshots): `Image.load_from_file(path)` then
  `ImageTexture.create_from_image(img)` (both ran on a PNG written with `save_png`); `AudioStreamOggVorbis.load_from_file(path)` (exists; on a missing file it logs `Cannot open file` and returns null).
  Do not use `load()` on arbitrary user files: it expects imported resources, and `.tres/.res` from
  untrusted sources can execute scripts (run: a `.tres` with an embedded GDScript ran its `_init` on `load()`).

## Gotchas
- Godot's PCK virtual file system is case-sensitive, Windows and recent macOS are not, so a case mismatch can work in the
  editor and fail after export (Godot docs, Project organization: use `snake_case` file names).
- Web exports: `user://` is a virtual file system stored via IndexedDB, and users must allow cookies (IndexedDB) for it to persist (Godot export docs).
- Never hard-code absolute OS paths; always use virtual paths or `OS.get_*` helpers.

## Verify
- [ ] Exported build saves and loads (test the export, not the editor).
- [ ] JSON data files load in the export (export filter configured).
- [ ] File names in code match disk casing exactly.
## Checked
Ran on Godot 4.7.2 headless (Windows): `OS.get_user_data_dir()` and `globalize_path` output; `DirAccess.make_dir_recursive_absolute`, `get_files_at`, `remove_absolute`; `Image.load_from_file`; `ImageTexture.create_from_image`; `AudioStreamOggVorbis.load_from_file` error path; a `.tres` with an embedded script executing on `load()`. The `user://` location table, the custom user dir rules (`use_custom_user_dir`, `custom_user_dir_name`), the non-resource export filter and the `.godot/imported` `.ctex` behaviour, PCK case sensitivity and web IndexedDB come from the Godot docs pages "File paths in Godot projects", "Exporting projects", "Import process", "Project organization" and "Exporting for the Web", plus the 4.7.2 `ProjectSettings` reference.
