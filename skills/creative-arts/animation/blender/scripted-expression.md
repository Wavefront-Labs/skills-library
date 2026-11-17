---
id: creative-arts.animation.blender.scripted-expression
name: scripted-expression
category: creative-arts
field: animation
product: blender
tags: [blender, drivers, scripted-expression, simple-expression, driver-python-functions, driver-namespace, driver-auto-run, auto-run-scripts, trusted-source]
level: practitioner
status: docs-checked
description: "Write fast Blender driver expressions: the simple-expression subset, when full Python is used, custom functions in bpy.app.driver_namespace, and Auto Run rules."
sources:
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html#simple-expressions
  - https://docs.blender.org/manual/en/latest/animation/drivers/workflow_examples.html
  - https://docs.blender.org/manual/en/latest/advanced/scripting/security.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# scripted-expression

Goal: driver expressions that evaluate without Python (fast, safe, work when scripts are disabled), and Python only when really needed.

## Simple expressions

Blender evaluates a subset of Python expressions directly (faster, and even when Python script execution is disabled). The manual's subset: variable names in ASCII; float and decimal-integer literals; the global `frame`; constants `pi`, `True`, `False`; operators `+ - * /`, `== != < <= > >=`, `and or not` and the conditional (ternary) operator; functions `min max radians degrees abs fabs floor ceil trunc round int sin cos tan asin acos atan atan2 exp log sqrt pow fmod`; and Blender's `lerp`, `clamp`, `smoothstep`. `Driver.is_simple_expression` reports whether an expression qualifies. Examples:
- `clamp(bend/radians(90), 0, 1)` — corrective weight from elbow angle.
- `smoothstep(0.2, 0.8, var)`; `lerp(0.5, 1.5, slider)`.

## Python expressions

Anything outside that subset (attribute access like `var.location`, `bpy.data...`, custom functions) runs full Python: Blender shows a "Slow Python expression" warning, and Python drivers do not run while script execution is disabled (see Auto Run below).

## Custom functions (driver namespace)

```python
import bpy
def squash(v, k): return 1.0 / max(v, 1e-4) ** k
bpy.app.driver_namespace["squash"] = squash
```
Run it from the Text Editor (*Run Script*) or tick the text block's **Register** option so it loads on start (needs Auto Run). Use `squash(stretch, 0.5)` in the driver.

## Auto Run and trust

- Preferences > Save & Load > **Auto Run Python Scripts** (scripts, including driver expressions, do not run by default) with **Excluded Paths** for untrusted folders; `-y` / `--enable-autoexec` enables it from the command line (`-Y` / `--disable-autoexec` disables it, the default).
- When a file is not allowed to run scripts, a warning dialog offers *Allow Execution* or *Ignore*.
- Prefer simple expressions for anything shipped to others, since they run even when script execution is disabled.

## Gotchas

- `frame` is available; `bpy.context.scene.frame_current` is Python and slower.
- `Use Self` (`self.location.x`) is outside the simple subset, so the driver runs full Python; dependencies reached through `self` may not be fully tracked.

## Verify

No "Slow Python expression" warning appears, and the rig works with Auto Run disabled.

## Checked

Blender 5.2 manual (blender-v5.2-release) and Python API 5.2, read 2026-10-27.
- Simple-expression subset (globals, constants, operators, standard and Blender-provided functions), the Slow Python expression warning, simple expressions running with scripts disabled, Use Self dependency note: animation/drivers/drivers_panel page. Driver namespace example (`bpy.app.driver_namespace`): workflow_examples page.
- Auto Run Python Scripts and Excluded Paths: preferences Save & Load page; Registered Text-Blocks and driver auto-execution: scripting security page; `-y/--enable-autoexec`, `-Y/--disable-autoexec`: command-line arguments. `Driver.is_simple_expression`: API 5.2.
- Corrected: `**` and `%` are not in the simple subset (the manual lists `pow`, `fmod`). Removed as unconfirmed: the Simple Expression label and the evaluate-to-0 behaviour. The Allow Execution / Ignore dialog is described on the security page.

Method: documentation only; no commands were run.
