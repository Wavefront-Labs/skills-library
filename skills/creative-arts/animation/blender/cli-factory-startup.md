---
id: creative-arts.animation.blender.cli-factory-startup
name: cli-factory-startup
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-factory-startup, factory-startup, add-ons]
level: practitioner
status: docs-checked
description: "Run Blender clean from the command line: --factory-startup, enabling only needed add-ons with --addons, autoexec flags -y/-Y, and isolating user config for reproducible renders."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-factory-startup

Goal: headless runs that do not depend on whatever an artist has in their preferences.

## Flags

- `--factory-startup`: skip reading the `startup.blend` in the user's home directory.
- `--addons name1,name2`: comma separated list (no spaces) of add-ons to enable in addition to any default add-ons.
- `-y` / `--enable-autoexec`: enable automatic Python script execution. `-Y` / `--disable-autoexec`: disable it (Python drivers and startup scripts); disabled is the default.
- `--env-system-scripts`, `--env-system-datafiles` and related options set the `BLENDER_SYSTEM_*` environment variables.

## Clean render pattern

```bash
blender -b --factory-startup --addons rigify -y shot.blend -P farm_setup.py -a
```
Arguments are processed in order: the blend-file loads, then `-P` runs the script, then `-a` renders.

## Why

- A user's add-on can register handlers that change scene data on load or render (a classic source of farm-only differences).
- Preferences such as GPU devices should be set explicitly in `farm_setup.py` (see cuda-setup).
- Rigs with Python driver expressions need `-y`, because Python drivers do not run when autoexec is disabled.

## Isolate config fully

Point `BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS` and `BLENDER_USER_EXTENSIONS` (see cli-environment-vars) to a controlled farm directory, so nothing from a home directory leaks in.

## Verify

Run with `--factory-startup` and print `bpy.context.preferences.addons.keys()` in a script. Only the add-ons you asked for (plus defaults) should be listed. Render a frame of a rig with Python drivers and check the pose.

## Checked

2026-10-27 against the Blender 5.2 manual, Command Line Arguments page. Confirmed: `--factory-startup` wording, `--addons` format, `-y`/`-Y` and default, `--env-system-*`. Removed unconfirmed claims (userpref.blend handling, extension module naming for `--addons`, flag position rules). Method: documentation only; no commands were run.
