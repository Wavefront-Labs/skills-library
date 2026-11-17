---
id: creative-arts.animation.blender.extensions-addons
name: extensions-addons
category: creative-arts
field: animation
product: blender
tags: [blender, extensions, add-ons, addons, extensions-platform, extension-repositories, install-from-disk, legacy-addons, studio-addons, offline-install, pinned-versions, preferences, legacy-addon-conversion, extension-updates, offline-mode, extension-permissions, extension-cli, enable-addon]
level: practitioner
status: docs-checked
description: "Install, update, pin and distribute Blender extensions and add-ons (4.2+): online/offline install, local repositories, legacy add-on migration, script directories."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/extensions.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html
  - https://extensions.blender.org/
  - https://docs.blender.org/manual/en/latest/editors/preferences/addons.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/extension_arguments.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# extensions-addons

Goal: get the right tools into every seat without "it works on my machine": versions pinned, installs reproducible, nothing phoning home unexpectedly.

## Vocabulary (4.2+)

- **Extension**: a package (add-on *or* theme) with a `blender_manifest.toml`, distributed through a **repository**. The official one is `extensions.blender.org` (open, reviewed, GPL-compatible).
- **Legacy add-on**: pre-4.2 `bl_info`-style add-on; still installs via *Install from Disk* (pick the `.py` or `.zip`; it is not enabled automatically, tick the checkbox).
- **Bundled add-ons**: Blender ships some add-ons preinstalled under *Preferences → Add-ons*; others are installed from the Extensions platform (search *Get Extensions*).

## Preferences → Get Extensions / Add-ons

- *Get Extensions* tab: **Allow Online Access** (a Preferences option, overridable with `--online-mode` / `--offline-mode`; add-ons are expected to honour `bpy.app.online_access`). Search, filter by type, **Install**, *Install Available Updates*, *Refresh Remote*, enable/disable toggle. Extensions declare permissions (files, network, clipboard, camera, microphone) in the manifest.
- *Add-ons* tab: lists add-ons; the menu has **Install from Disk** (a `.zip` extension or legacy `.py`/`.zip`) and *Refresh Local*, with search, an *Enabled Add-ons Only* filter and tags. The checkbox enables; if an add-on does not activate, read the Console window for the Python error.
- Repositories panel (`Get Extensions` → *Repositories* dropdown → `+`): **Add Remote Repository** (URL to an `index.json` — a studio server or a GitHub Pages site), **Add Local Repository** (a folder; drop `.zip`s there and *Refresh*; good for offline machines and version-controlled tool folders). Remote repository options: *Check for Updates on Startup* and *Access Token* (may be required by some repositories). *Remove Repository & Files* also deletes the repository's files.

## Reproducible installs

- Pin: note extension IDs and versions; disable *Check for Updates on Startup* on production seats; use a **local repository** folder in the pipeline repo with the exact `.zip`s (`blender -c extension server-generate --repo-dir=<dir>` generates the listing for static hosting; add `--html` for a browsable `index.html`).
- CLI (4.2+): `blender -c extension list`, `install [-s] [-e] <ids comma-separated>`, `install-file -r <repo> [-e] <zip>`, `remove <id>`, `sync`, `update`. `blender -b --python-expr "import bpy; bpy.ops.preferences.addon_enable(module='bl_ext.<repo>.<id>')"` enables (module name = `bl_ext.<repository_module_name>.<id>` for extensions, plain module name for legacy add-ons).
- **Script Directories** (Preferences → File Paths → *Script Directories* `+`): a folder containing `addons/` (legacy add-ons auto-listed), `startup/` (modules imported at startup), `modules/`, `presets/`. Changes need a Blender restart, and the manual now recommends a local extension repository instead of script directories for add-ons. Environment variables `BLENDER_USER_RESOURCES`, `BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS` and `BLENDER_USER_EXTENSIONS` relocate user directories (see the command-line environment section).
- Portable installs: create a folder named `portable` next to the Blender executable (inside the app bundle on macOS) to keep configuration with the install.
- Python dependencies: extensions bundle wheels (`wheels = [...]` in the manifest, installed into the extension's own site-packages; see `creative-arts.animation.blender.addon-wheels`).

## Migrating / fixing add-ons

- Legacy add-on fails on 4.2+: common breakers — imports that are not package-relative, hard-coded module names for preferences (use `__package__`), and removed APIs (`Mesh.use_auto_smooth` removed in 4.1, `Mesh.calc_normals` removed in 4.0). Read the traceback (Window → *Toggle System Console*), fix, then `F3 → Reload Scripts`.
- Convert to an extension: add `blender_manifest.toml` (`schema_version`, `id`, `version`, `name`, `tagline`, `maintainer`, `type = "add-on"`, `blender_version_min`, `license = ["SPDX:GPL-3.0-or-later"]`; optional `permissions`), drop `bl_info`, replace module-name references with `__package__`, make imports relative, `blender -c extension validate <dir>` then `build` → `.zip` (`creative-arts.animation.blender.addon-development`).
- Two versions of the same add-on (legacy + extension) both enabled = duplicate menus/keymaps; disable one.

## Gotchas

- A `.zip` saved from a version-control site: the manifest may sit at the top level or inside a single folder in the archive; check the layout if the install fails.
- Update All can break a show mid-production — pin and test on one seat.
- Extensions with `network` permission can download at runtime (asset libraries); audit before deploying behind a proxy.

## Verify

- `blender -c extension list` shows the expected IDs/versions on every seat; `Preferences → Add-ons` shows no red errors.
- Launch with *Allow Online Access* off (`--offline-mode`) still has all tools (proves local/legacy installs).
- A fresh machine set up from the pipeline script/portable folder shows identical menus, keymaps and add-on versions.
- The Console window shows no add-on load errors at startup.

## Checked

Blender 5.2 manual (blender-v5.2-release branch), read 2026-10-27.
- Extension CLI sub-commands and options (list, install -s/-e, install-file -r/-e, remove, sync, update, build, validate, server-generate --html): extension command-line page. Corrected the `install --repo` form, which does not exist.
- Preferences wording (Refresh Remote/Local, Install Available Updates, Check for Updates on Startup, Access Token, Remove Repository & Files, Script Directories subfolders and restart, local-repository recommendation, portable folder, BLENDER_USER_* variables, online-access flags): preferences pages, command-line page and directory-layout page.
- Removed API names: Mesh.calc_normals (4.0) and use_auto_smooth (4.1) per the developer-docs Python API release notes.
- Removed as unconfirmed: bundled/moved add-on lists, the Essentials list, config/extension directory paths, per-version settings copy, the pip --target workaround, userpref save and network-share claims.

Method: documentation only; no commands were run.
