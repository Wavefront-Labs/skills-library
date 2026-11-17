---
id: creative-arts.animation.blender.background-script
name: background-script
category: creative-arts
field: animation
product: blender
tags: [blender, background-script, background-python, headless, command-line, python-exit-code, bpy]
level: practitioner
status: docs-checked
description: "Write Blender Python scripts that run reliably in -b background mode: what context is missing, operator overrides, saving, exit codes and logging for unattended jobs."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://docs.blender.org/api/current/info_gotcha.html
  - https://docs.blender.org/api/current/bpy.ops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# background-script

Goal: a script that works in the UI and also as `blender -b file.blend --python job.py -- args` on a farm or CI box.

## Invocation

```bash
blender -b scene.blend --factory-startup --python-exit-code 1 --python job.py -- --out /renders/x
```
- Arguments are processed left to right (a `-f` before `--python` renders before the script runs).
- `--python-exit-code 1` sets the exit code used when a command-line script raises an exception.
- `--factory-startup` skips reading `startup.blend`; enable the add-ons you need with `--addons name1,name2` or in the script.
- Parse your own args after `--` (see `creative-arts.animation.blender.cli-argument-parsing`).

## What is different in background mode

- `bpy.app.background` is True: there is no user interface, so window, screen and area based context members are not meaningful and operators that need a 3D view fail their poll. Prefer data API calls; where an operator is unavoidable, pass needed members with `bpy.context.temp_override(...)`.
- Do not rely on modal operators, draw handlers or UI timers.
- EEVEE and Workbench need a GPU context; check what your host provides.
- Set the active object and selection explicitly rather than relying on what the file was saved with.

## Skeleton

```python
import bpy, sys, logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("job")

def main(args):
    sc = bpy.context.scene
    ...                                      # data-API work
    bpy.ops.wm.save_as_mainfile(filepath=args.out_blend, copy=False)

if __name__ == "__main__":
    import argparse
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(); p.add_argument("--out-blend", required=True)
    try:
        main(p.parse_args(argv))
    except Exception:
        log.exception("job failed")
        sys.exit(1)
```

## Gotchas

- `sys.exit()` inside Blender ends the whole process: guard it with `bpy.app.background` so it never runs in the UI.
- Relative `//` paths resolve against the blend-file; use absolute paths when running on a new, unsaved file.
- Check `bpy.data.libraries` and image file paths yourself instead of assuming linked data loaded.
- Add `flush=True` to prints if you pipe the output and need it in order.

## Verify

Run the script in the UI via the Text Editor and headless: both produce the same output. Force an error with `--python-exit-code 1` and confirm the shell sees exit code 1 (`echo $?`).

## Checked

2026-10-27 against the Blender 5.2 manual (Command Line Arguments: argument order, `--python-exit-code`, `--factory-startup`, `--addons`) and the 5.2 Python API (bpy.app.background, Context.temp_override). Removed unconfirmed claims (exact None values and error text, GPU-module and asset-preview failures, buffering behaviour). Method: documentation only; no commands were run.
