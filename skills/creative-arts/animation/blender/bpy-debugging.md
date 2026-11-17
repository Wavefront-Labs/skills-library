---
id: creative-arts.animation.blender.bpy-debugging
name: bpy-debugging
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-debugging, script-debugging, vscode-blender, debugpy, traceback, system-console]
level: practitioner
status: verified
description: "Debug Blender Python: read tracebacks in the system console, print and logging, pdb from a terminal, debugpy attach from VS Code, and the Blender Development extension."
sources:
  - https://docs.blender.org/api/current/info_tips_and_tricks.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://github.com/JacquesLucke/blender_vscode
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-debugging

Goal: stop debugging by guessing; get a traceback, a breakpoint, and inspectable variables.

## Where errors go

- `print()` output and uncaught tracebacks go to the process's stdout/stderr (the system console), not the Python Console. Launch Blender from a terminal to see them.
- `blender --debug-python` enables debug messages for Python; `--python-exit-code <code>` sets the exit code used when a command-line script raises (essential for CI): in 4.5.14 a raising script gave exit status 7 with `--python-exit-code 7` and status 0 without it.

## Logging instead of prints

```python
import logging
log = logging.getLogger("mytool")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")
log.debug("processing %s", ob.name)
```
In operators, `self.report({'WARNING'}, "...")` reaches the user; logging reaches the developer.

## Breakpoints

- **pdb:** only when Blender runs from a terminal: put `breakpoint()` in the script and step in the terminal (`n`, `s`, `p var`, `c`). `blender -d` keeps Python's `sys.stdin` instead of setting it to None (the manual's statement; in 4.5.14 a background run under a pipe already had a text `sys.stdin`).
- **Quick REPL:** `import code; code.interact(local=locals())` drops into an interactive shell at that line (terminal again).
- **VS Code, debugpy:** install `debugpy` into the Python Blender uses, then in your script/add-on:

```python
import debugpy
debugpy.listen(("localhost", 5678))   # call once per session
debugpy.wait_for_client()
```
and attach with a VS Code "Python: Remote Attach" config on `localhost:5678` with a `pathMappings` entry if the add-on folder differs.
- **Blender Development extension** (id `JacquesLucke.blender-development`): *Blender: Start* launches a Blender session from VS Code, *Blender: Reload Addons* reloads after edits, *Blender: Run Script* runs a script.

## Common causes

- `AttributeError` on a context member: it is not available in the current context or area; see `creative-arts.animation.blender.bpy-context-vs-data`.
- `ReferenceError` on a datablock: you kept a Python reference across an undo, file load or `data.remove`; re-fetch by name.
- Values not updating: call `view_layer.update()` (updates data tagged from earlier access) after changing data (tested: after `ob.location.x = 5` the `matrix_world` translation read 0.0 until `view_layer.update()`, then 5.0).

## Gotchas

- `wait_for_client()` blocks the UI until VS Code attaches; remove it in shipped code.
- Breakpoints in drawing code interrupt redraw; debug the logic outside `draw`.

## Verify

Raise a deliberate exception and see the traceback in the terminal; hit a VS Code breakpoint and inspect `bpy.context.object.name` in the debug console.

## Checked

2026-10-27 against the Blender 5.2 manual (command line `-d`, `--debug-python`, `--python-exit-code`), the 5.2 Python API (View Layer update) and the blender_vscode README (commands *Blender: Start*, *Reload Addons*, *Run Script*, extension id). debugpy `listen` and `wait_for_client` are named in the debugpy README. Removed unconfirmed claims (status bar behaviour, debugpy install path, double-listen behaviour, exact error texts). Run check, 2026-11-01, Blender 4.5.14 LTS headless: a script that raises printed the traceback followed by `Error: script failed, file: 'fail.py', exiting.` and exited with status 7 under `--python-exit-code 7` and 0 without it; `--help` lists `-d or --debug`, `--debug-python` and `--python-exit-code`; the `logging` snippet printed `DEBUG mytool: hello x` to the terminal; `print` to stdout and stderr appeared in the terminal; `breakpoint` and `code.interact` exist; `import debugpy` raised ModuleNotFoundError in the bundled Python, so it must be installed first; a removed object raised ReferenceError; an unknown context member raised AttributeError; `context.area` is None in background mode. Unrun: interactive pdb, VS Code attach and the Blender Development extension commands (documentation and README only).
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
