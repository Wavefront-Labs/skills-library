---
id: creative-arts.animation.blender.cli-python-expr
name: cli-python-expr
category: creative-arts
field: animation
product: blender
tags: [blender, command-line, cli, cli-python-expr, python-expr, python-script-arg, bpy]
level: practitioner
status: docs-checked
description: "Run Python from the Blender command line: --python-expr one-liners, -P scripts, --python-text, --python-exit-code for CI, and changing settings before a render."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cli-python-expr

Goal: change scene settings or run automation in headless Blender without editing the .blend.

## Options

```bash
blender -b shot.blend --python-expr "import bpy; bpy.context.scene.cycles.samples = 64" -a
blender -b shot.blend -P setup_render.py -a
blender -b shot.blend --python-text MyTextBlock -a        # run a text block stored in the .blend
blender -b --python-exit-code 1 -P checks.py             # exit code 1 if the script raises
blender -b --factory-startup -P build_scene.py            # skip startup.blend
```
- `-P` / `--python <filepath>` runs a script file. `--python-expr <expression>` runs a string; it may be a complete multi-line script, limited by the platform's maximum argument length.
- `--python-text <name>` runs a text block.
- Arguments run **in the order given**, so put them after the blend-file and before `-a`/`-f`.
- `--python-exit-code <code>` (0-255, 0 disables): the exit code used if a Python exception is raised, for scripts executed from the command line. Use it in CI and farm jobs.
- `--python-use-system-env` lets Python use system environment variables such as `PYTHONPATH` and the user site-packages directory.
- `--python-console` starts an interactive console; `-y`/`-Y` enable or disable auto-execution of scripts stored in files.

## Typical setup script

```python
import bpy
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.samples = 256
sc.render.resolution_percentage = 100
sc.render.filepath = "//../render/sh010/sh010_####"
```

## Gotchas

- Quoting: in bash use double quotes outside, single inside. In PowerShell the rules differ, so prefer `-P` scripts for anything beyond one line.
- A script that calls `bpy.ops.render.render(animation=True)` itself plus `-a` on the command line renders twice.
- Background mode has no window or area, so operators that need a 3D view fail (see bpy-ops-temp-override).

## Verify

`blender -b shot.blend --python-expr "import bpy; print(bpy.context.scene.cycles.samples)"` prints the value. With `--python-exit-code 1`, a script that raises returns exit code 1 (`echo $?`).

## Checked

2026-10-27 against the Blender 5.2 manual, Command Line Arguments page (Python Options) and the 5.2 Python API (`Scene.cycles` via the Cycles add-on source, `RenderSettings`). Confirmed all options above, argument ordering and exit-code range. Removed an unconfirmed claim about default exit status. Method: documentation only; no commands were run.
