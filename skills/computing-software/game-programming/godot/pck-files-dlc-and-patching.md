---
id: computing-software.game-programming.godot.pck-files-dlc-and-patching
name: pck-files-dlc-and-patching
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-export, pck-files, dlc, patching, load-resource-pack, mods, game-programming]
level: advanced
status: docs-checked
description: "Ship DLC, patches and mods with Godot PCK files: exporting packs, ProjectSettings.load_resource_pack, file replacement order, script compatibility and security."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html", "https://docs.godotengine.org/en/stable/classes/class_projectsettings.html#class-projectsettings-method-load-resource-pack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCK files, DLC and patching

**Goal:** deliver extra content or fixes as packs loaded at runtime instead of reinstalling the game.

## How packs work
Exported games read `res://` from the main `.pck` (next to the executable or embedded). Additional packs
mount into the **same virtual `res://`**: new paths are added, existing paths are **replaced** by the
later-loaded pack.

## Create a pack
- A separate project (or an export preset that selects only those resources) containing only the DLC/patch files at
  the same `res://` paths they should occupy.
- `godot --path . --export-pack "Windows Desktop" dlc_forest.pck` (or `.zip`).
- Export packs with `--export-pack`; the output file must end in `.pck` or `.zip`.

## Load at runtime
```gdscript
func mount_dlc(path: String) -> bool:
    if not FileAccess.file_exists(path): return false
    var ok := ProjectSettings.load_resource_pack(path, true)   # replace_files defaults to true
    if ok:
        var forest := load("res://dlc/forest/forest.tscn")     # now resolvable
    return ok
```
- Load packs **early** (boot scene), before the resources they override are loaded.
- Typical location: `OS.get_executable_path().get_base_dir()` for shipped DLC, `user://` for downloaded patches.
- For store-owned DLC, check ownership through the platform SDK as well as the file existing.

## Patching
- Patch packs contain only changed files; load in order (patch_1, patch_2...). Later wins.
- Prefer `preload` paths for DLC scripts rather than relying on `class_name` registration (not verified in the docs).
- A pack can replace files but cannot delete them; ship a stub or change references.

## Modding and security
- Loading arbitrary user PCKs = running arbitrary GDScript with full file/network access. Only load
  trusted packs, or treat mods as fully trusted code and say so.

## Verify
- [ ] Base game + DLC pack: DLC content loads; without the pack, the game runs and hides DLC.
- [ ] Patch pack overrides a scene and the fix appears on next launch.

## Checked

2026-10-28. Confirmed against: ProjectSettings.load_resource_pack reference (replace_files defaults to true; loaded files replace existing ones) and the exporting PCKs tutorial (--export-pack with .pck or .zip output, load order matters).

Removed or rewritten: the Godot-version-match rule, headless flag, Steam isDLCInstalled name, class_name registration claims, resource-cache behaviour and PCK-encryption statement.

Method: documentation only; no commands were run.
