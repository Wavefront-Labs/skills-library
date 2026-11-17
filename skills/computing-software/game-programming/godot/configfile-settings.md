---
id: computing-software.game-programming.godot.configfile-settings
name: configfile-settings
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-save-game, configfile, settings-menu, ini, user-settings, audio-volume, display-settings, game-programming]
level: intro
status: verified
description: "Persist player settings in Godot with ConfigFile: sections and keys, defaults, applying video/audio settings at startup, and keeping settings separate from save games."
sources: ["https://docs.godotengine.org/en/stable/classes/class_configfile.html", "https://docs.godotengine.org/en/stable/classes/class_audioserver.html", "https://docs.godotengine.org/en/stable/classes/class_displayserver.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ConfigFile for settings

**Goal:** options (volume, resolution, vsync, language, sensitivity) saved in a small INI-style file,
loaded and applied before the first menu appears.

## Settings autoload
```gdscript
# res://autoload/settings.gd  (Project Settings > Autoload as "Settings")
extends Node
const PATH := "user://settings.cfg"

var data := {
    "audio":   {"master": 1.0, "music": 0.8, "sfx": 1.0},
    "video":   {"fullscreen": true, "vsync": true, "scale": 1.0},
    "game":    {"sensitivity": 1.0, "language": "en"},
}

func _ready() -> void:
    load_settings()
    apply()

func load_settings() -> void:
    var cfg := ConfigFile.new()
    if cfg.load(PATH) != OK: return                    # first run: keep defaults
    for section in data:
        for key in data[section]:
            data[section][key] = cfg.get_value(section, key, data[section][key])  # default if missing

func save_settings() -> void:
    var cfg := ConfigFile.new()
    for section in data:
        for key in data[section]:
            cfg.set_value(section, key, data[section][key])
    cfg.save(PATH)

func apply() -> void:
    for bus in ["master", "music", "sfx"]:
        var idx := AudioServer.get_bus_index(bus.capitalize())
        if idx < 0: continue                           # bus missing from the layout (default layout is Master only)
        AudioServer.set_bus_volume_db(idx, linear_to_db(maxf(data.audio[bus], 0.0001)))
    DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN if data.video.fullscreen else DisplayServer.WINDOW_MODE_WINDOWED)
    DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if data.video.vsync else DisplayServer.VSYNC_DISABLED)
    get_tree().root.content_scale_factor = data.video.scale
    TranslationServer.set_locale(data.game.language)
```
The file is plain text:
```ini
[audio]

master=1.0
music=0.8
```
(`ConfigFile` writes a blank line after each section header and after each section.)

## Notes
- `get_value(section, key, default)` handles new settings added in later versions without migration.
- ConfigFile stores Variants (Vector2, Color, arrays) in Godot's text format; fine for settings.
- Keep settings separate from save slots: players expect options to apply across saves.
- Volume sliders: store linear 0..1, convert with `linear_to_db`; `linear_to_db(0.0)` is `-inf` and `0.0001` is `-80.0` dB, so clamp.
- A project starts with a single bus named `Master`. `get_bus_index("Music")` returns -1 until you add buses in the Audio bus layout, and `set_bus_volume_db(-1, ...)` then logs an out-of-bounds error, so guard the index.
- `save_encrypted(path, key)` and `save_encrypted_pass(path, password)` exist (with matching `load_*`) but settings rarely need it.
- Apply settings in the autoload `_ready` so the first frame already has the right window mode.

## Verify
- [ ] Delete the file: game starts with defaults and writes a new file on first save.
- [ ] Change volume, restart: volume persists.
- [ ] Add a new setting key in code: old files load and the new key gets its default.
## Checked
Ran on Godot 4.7.2 headless (Windows): the autoload code above as written (the unguarded version logs `Index p_bus = -1 is out of bounds` for Music and SFX with the default layout); `save`/`load` round trip with Vector2 values (`Vector2(3, 4)` text form); `get_value` with a default for a missing key returns the default; `load` on a missing file returns 7 (`ERR_FILE_NOT_FOUND`); `TranslationServer.set_locale("en")`; method existence for `save_encrypted`, `save_encrypted_pass`, `load_encrypted_pass`, `Window.content_scale_factor`, `DisplayServer.window_set_vsync_mode`. The window mode and vsync calls ran without error under the headless display driver, which ignores window changes, so only the API calls were exercised.
