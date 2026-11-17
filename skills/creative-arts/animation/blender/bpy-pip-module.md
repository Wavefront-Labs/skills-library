---
id: creative-arts.animation.blender.bpy-pip-module
name: bpy-pip-module
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-pip-module, bpy-wheel, pip-install-blender, ensurepip, python-packages, pipeline]
level: advanced
status: docs-checked
description: "Use Blender as a Python module (pip install bpy) and install extra packages into Blender's bundled Python: version matching, venvs, limits and safe install paths."
sources:
  - https://pypi.org/project/bpy/
  - https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/python_wheels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bpy-pip-module

Goal: import bpy in an ordinary Python process (tests, services, notebooks), or add a package to Blender's own Python without breaking it.

## bpy from PyPI

```bash
python3.13 -m venv .venv && . .venv/bin/activate
pip install bpy==5.2.*        # the bpy version matches the Blender release
python -c "import bpy; print(bpy.app.version_string)"
```
- Each bpy release declares its supported Python in the PyPI metadata (bpy 5.2.3 requires Python 3.13.* and numpy 2.2 or newer); pip refuses another version. Check the PyPI page for the release you pin.
- Only the official wheels published on PyPI are available.
- Start each job from a clean state: `bpy.ops.wm.read_factory_settings(use_empty=True)`; open files with `bpy.ops.wm.open_mainfile(filepath=...)`.
- Only a single .blend file can be edited per process. For parallel work start separate processes (Python's `multiprocessing` helps); reloading the module with `importlib.reload` raises an exception, so reset with `bpy.ops.wm.read_factory_settings()`.

## Packages inside Blender's bundled Python

Inside Blender, `sys.executable` should point to the Python it uses; install into that interpreter:

```bash
"<BLENDER_DIR>/<ver>/python/bin/python" -m ensurepip
"<BLENDER_DIR>/<ver>/python/bin/python" -m pip install --target "<TARGET_DIR>" <package>   # TARGET_DIR must be on sys.path
```
- For distributable add-ons, ship wheels inside the extension (by convention under `./wheels/`) instead of installing into Blender's Python (`creative-arts.animation.blender.addon-wheels`).

## Gotchas

- Do not upgrade packages that Blender bundles (numpy is a bpy dependency); a different version can break Blender modules.
- The bpy wheel is large; cache it in CI.
- Add-ons are not included in the module; enable them from Python or extend `sys.path`.

## Verify

In the venv, open a .blend and print `len(bpy.data.objects)`; inside Blender, `import <package>` succeeds after restart.

## Checked

2026-10-27 against the Blender 5.2 Python API page Advanced > Blender as a Python Module (single .blend per process, no importlib.reload, read_factory_settings, multiprocessing hint), PyPI metadata for bpy (5.2.3: Python ==3.13.*, numpy>=2.2) and the 5.2 manual Python Wheels page (wheels under ./wheels/). Removed unconfirmed claims (platform list, EEVEE/Cycles behaviour, wheel size figure, modules-folder behaviour). Method: documentation only; no commands were run.
