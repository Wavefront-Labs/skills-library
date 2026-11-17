---
id: computing-software.game-programming.godot.feature-tags-and-platform-overrides
name: feature-tags-and-platform-overrides
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-export, feature-tags, platform-overrides, os-has-feature, project-settings-overrides, game-programming]
level: intro
status: docs-checked
description: "Use Godot feature tags (platform, debug/release, custom) for per-platform project setting overrides and OS.has_feature checks, including custom tags per export preset."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/feature_tags.html", "https://docs.godotengine.org/en/stable/classes/class_os.html#class-os-method-has-feature"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature tags and per-platform overrides

**Goal:** platform- and build-specific behaviour without code forks: mobile settings, demo builds, debug tools.

## Built-in tags
- Platform: `pc`, `web_android`, `web_ios` and others (see the feature tags table for the full list); the table also has `mobile`.
- Build: `debug` (the docs say `debug` includes the editor), `release`, `editor`, `template`.
- Texture compression: `etc2`, `s3tc` and others listed in the table.

## Custom tags
Add custom features in the export preset (Features tab), for example `demo` or `steam`.

## Check in code
```gdscript
if OS.has_feature("demo"):
    max_level = 3
if OS.has_feature("mobile") or OS.has_feature("web_android") or OS.has_feature("web_ios"):
    show_touch_controls()
if OS.has_feature("debug"):
    add_child(preload("res://debug/dev_console.tscn").instantiate())
if OS.has_feature("editor"):
    pass   # editor-only paths
```

## Project setting overrides
Features can override Project Settings values (in `project.godot` as a `.<feature>` suffix on the setting name):
```ini
[rendering]
renderer/rendering_method="forward_plus"
renderer/rendering_method.mobile="mobile"
textures/vram_compression/import_etc2_astc=true

[display]
window/size/viewport_width=1920
window/size/viewport_width.mobile=1280
```
Works with feature tags, including custom ones. At runtime read overridden settings with `ProjectSettings.get_setting_with_override()`, as the docs state.

## Gotchas
- `debug` includes the editor; use `editor` to distinguish.
- Custom feature tags are defined per export preset and have caveats when running from the editor (the docs mention presets marked Runnable), so test the export.

## Verify
- [ ] Demo export can't access full-game content; full export can.
- [ ] Mobile export picks the mobile renderer and settings override.

## Checked

2026-10-28. Confirmed against: Feature tags tutorial and OS class (web_android, web_ios, pc, etc2, s3tc, template, debug includes the editor, features override Project Settings, get_setting_with_override, custom features in export presets).

Removed or rewritten: the complete tag lists for platforms/architectures/other texture formats, the Add-override UI path, the example setting values, resolution-at-startup claim and the statement that custom tags never exist when running from the editor (the docs mention Runnable presets).

Method: documentation only; no commands were run.
