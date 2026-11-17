---
id: computing-software.game-programming.godot.export-presets-and-command-line-export
name: export-presets-and-command-line-export
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-export, export-presets, headless-export, export-templates, ci-builds, game-programming]
level: practitioner
status: docs-checked
description: "Export Godot 4 projects reproducibly: export templates, export_presets.cfg, resource filters, headless --export-release/--export-debug in CI, and keeping credentials out of git."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html", "https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export presets and command-line export

**Goal:** one command (locally and in CI) produces every platform build from committed presets.

## Templates and presets
- Editor > Manage Export Templates: install the templates for the platforms and architectures you need
  (a downloaded `.tpz` of all templates is functionally identical but larger). The `godot` binary used
  to export must be an editor binary, not an export template.
- Project > Export > Add preset per target (Windows Desktop, Linux, macOS, Android, Web). Saved to
  `export_presets.cfg` in the project root: **commit it**.
- Confidential options (passwords, encryption keys) are stored in `.godot/export_credentials.cfg`, which
  should generally not be committed (copy it to a new machine by hand), or come from environment
  variables that override the export menu, for Android:
  `GODOT_ANDROID_KEYSTORE_RELEASE_PATH`, `GODOT_ANDROID_KEYSTORE_RELEASE_USER`,
  `GODOT_ANDROID_KEYSTORE_RELEASE_PASSWORD` (and the `_DEBUG_` equivalents) and `GODOT_SCRIPT_ENCRYPTION_KEY`.

## Resources tab
- Export Mode: all resources, selected scenes, selected resources (both with dependencies), all except
  the checked ones, or Export as dedicated server.
- **Filters to export non-resource files** (`*.json, *.csv, data/*`): non-resource files such as `.txt`,
  `.json` and `.csv` are only exported when matched here.
- A second filter excludes every file of a type (`*.psd`). Files and folders whose name starts with a
  period are never exported.
- Feature tags (custom) per preset (`demo`, `steam`).

## Command line
```
godot --headless --path . --export-release "Windows Desktop" build/win/MyGame.exe
godot --headless --path . --export-debug "Linux" build/linux/MyGame.x86_64
godot --headless --path . --export-pack "Windows Desktop" build/patch.pck      # PCK/ZIP only
```
- Preset name must match exactly (quotes for spaces). Output directory must exist.
- `--import` starts the editor, waits for resources to import, then quits; `--export-debug` and
  `--export-pack` imply it. Running `godot --headless --path . --import` first on a fresh checkout is a
  safe step before `--export-release`.
- `--headless` is required on platforms without GPU access (such as CI) and keeps a window from
  spawning elsewhere. Relative output paths are relative to the project directory.
- On CI, install the export templates for the editor binary (for example from the `.tpz` on the download page).

## Platform notes
- Android: the keystore and key passwords currently have to be the same; `--install-android-build-template`
  used with `--export-release` or `--export-debug` installs the Android build template. See the per-platform
  export pages for signing and notarisation requirements.
- `--export-patch <preset> <path>` with `--patches <list>` exports a pack with only the changed files.

## Verify
- [ ] Fresh clone + CI script produces runnable builds for every preset.
- [ ] No credentials in `export_presets.cfg` (check git diff).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: Manage Export Templates and the `.tpz` option; `godot` must be an editor binary with templates installed; `export_presets.cfg` is safe to commit and `.godot/export_credentials.cfg` holds passwords and encryption keys that should not be committed; the five export modes, the two filters and the leading-period rule; `--export-release`, `--export-debug` (implies `--import`), `--export-pack` (extension picks PCK or ZIP, implies `--import`), `--export-patch`, `--patches`, `--install-android-build-template`, `--import`, `--headless` and `--path`; the preset name must match one in `export_presets.cfg` and the target directory must exist; the Android environment variable names; keystore and key passwords must match. Removed the unconfirmed exact-version and template-folder claim, exit-code claim, third-party CI image, rcedit, notarisation and Embed PCK notes.

Method: documentation only; no commands were run.
