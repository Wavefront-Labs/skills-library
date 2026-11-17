---
id: creative-arts.animation.blender.cli-environment-vars
name: cli-environment-vars
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-environment-vars, blender-env-vars, ocio, pipeline]
level: practitioner
status: docs-checked
description: "Use Blender environment variables: BLENDER_USER_CONFIG, USER_SCRIPTS, SYSTEM_SCRIPTS, extensions dirs, BLENDER_OCIO and temp paths, to give studio and farm seats the same setup."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-environment-vars

Goal: control where Blender reads configuration, scripts and add-ons, so every machine matches.

## Variables (Blender 5.2 manual)

| Variable | Effect |
|---|---|
| `BLENDER_USER_RESOURCES` | Replaces the default directory of all user files; other `BLENDER_USER_*` variables override it when set |
| `BLENDER_USER_CONFIG` | Directory for user configuration files |
| `BLENDER_USER_SCRIPTS` | Directory for user scripts |
| `BLENDER_USER_EXTENSIONS` | Directory for user extensions |
| `BLENDER_USER_DATAFILES` | Directory for user data files (icons, translations, ..) |
| `BLENDER_SYSTEM_RESOURCES` | Replaces the default directory of all bundled resource files |
| `BLENDER_SYSTEM_SCRIPTS` | Directories to add extra scripts |
| `BLENDER_SYSTEM_EXTENSIONS` | Directory for the system extensions repository |
| `BLENDER_SYSTEM_DATAFILES`, `BLENDER_SYSTEM_PYTHON` | Directory to replace bundled datafiles / Python libraries |
| `BLENDER_OCIO` | Path to override the OpenColorIO configuration file; if unset, the `OCIO` variable is used |
| `TEMP` (Windows), `TMPDIR` (Unix) | Where temporary files are stored; `TMPDIR` must reference an existing directory or it is ignored |

The `--env-system-datafiles`, `--env-system-scripts`, `--env-system-extensions` and `--env-system-python` command-line options set the matching `BLENDER_SYSTEM_*` variables.

## Studio pattern

A launcher script (bash/batch) sets:
```bash
export BLENDER_SYSTEM_SCRIPTS=/pipeline/blender/scripts
export BLENDER_USER_CONFIG=$HOME/.studio/blender/config
export BLENDER_OCIO=/pipeline/ocio/config.ocio
exec /opt/blender/blender "$@"
```
Use a startup script in your scripts directory to set preferences (GPU devices) that would otherwise depend on each user; check the Blender directory layout page for the exact startup folder.

## Gotchas

- Point variables at directories that exist; confirm what Blender actually uses (below) instead of assuming.
- On Windows, set variables in the launcher, not system-wide, so different projects can use different configs.
- Python: `bpy.utils.script_paths()` and `bpy.utils.user_resource('CONFIG')` show the paths in use.

## Verify

Launch through the wrapper and run in the Python console: `import bpy; print(bpy.utils.script_paths())`. The studio path should be listed.

## Checked

2026-10-27 against the Blender 5.2 manual, Command Line Arguments page (Environment Variables section). Corrected: `TMP` is not listed (TEMP and TMPDIR are), the OCIO override variable is `BLENDER_OCIO` with `OCIO` as fallback, user data files are icons and translations. Removed unconfirmed claims (version gate on extensions, startup-folder behaviour, silent-ignore of wrong paths). Method: documentation only; no commands were run.
