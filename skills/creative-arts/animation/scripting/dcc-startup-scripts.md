---
id: creative-arts.animation.scripting.dcc-startup-scripts
name: dcc-startup-scripts
category: creative-arts
field: animation
product: scripting
tags: [startup-scripts, pipeline-python, dcc-python, usersetup, menu-py, init-py, maya-module, houdini-package, blender-startup, environment-bootstrap]
level: advanced
status: draft
description: "Bootstrap pipeline code into DCCs at launch: Maya userSetup and modules, Nuke init.py/menu.py, Houdini packages, Blender startup scripts, via environment variables."
sources:
  - https://help.autodesk.com/view/MAYAUL/2025/ENU/
  - https://learn.foundry.com/nuke/developers/latest/pythondevguide/startup.html
  - https://www.sidefx.com/docs/houdini/ref/plugins.html
  - https://docs.blender.org/api/current/info_overview.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DCC startup scripts and environment bootstrap

**Goal:** every artist's DCC opens with the studio menu, tools, plugins and show settings loaded,
controlled centrally by environment variables set by the launcher (Rez, Ayon, a wrapper script), not by
per-user files.

## Per DCC

| DCC | Mechanism | Env var |
|---|---|---|
| Maya | `userSetup.py` on `PYTHONPATH`/`MAYA_SCRIPT_PATH`; module files (`.mod`) | `MAYA_MODULE_PATH`, `PYTHONPATH`, `MAYA_PLUG_IN_PATH` |
| Nuke | `init.py` (all modes incl. render) and `menu.py` (GUI only) in plugin paths | `NUKE_PATH` |
| Houdini | package JSON files adding paths/env | `HOUDINI_PACKAGE_DIR`, `HOUDINI_PATH` |
| Blender | `scripts/startup/*.py` modules with `register()`; add-ons dirs | `BLENDER_USER_SCRIPTS`, `BLENDER_SYSTEM_SCRIPTS` (4.2+) |
| After Effects | Scripts/Startup folder, ScriptUI Panels | none (copy/symlink) |

## Maya example

```python
# <PIPELINE>/maya/scripts/userSetup.py
import maya.utils
def _boot():
    import studio_pipeline.maya.menu as m
    m.build()
maya.utils.executeDeferred(_boot)      # wait until the UI exists
```
Module file `<PIPELINE>/maya/studio.mod`:
```
+ studio 1.0 <PIPELINE>/maya
PYTHONPATH +:= python
MAYA_PLUG_IN_PATH +:= plug-ins
```

## Nuke example

`init.py` (runs in render/terminal mode too): `nuke.pluginAddPath("./gizmos")`, set formats/OCIO.
`menu.py` (GUI): build the studio toolbar. Keep heavy imports out of `init.py` to keep farm renders fast.

## Houdini package

```json
{ "env": [ {"STUDIO_HOU": "<PIPELINE>/houdini"} ],
  "path": "$STUDIO_HOU" }
```
in a folder pointed to by `HOUDINI_PACKAGE_DIR`.

## Rules

- Startup must never fail hard: wrap in try/except and log, or a broken tool blocks every artist.
- Keep show-specific values (project root, OCIO config, frame rate) in environment variables set by the
  launcher.
- Farm/batch modes load the same code paths minus UI; test headless (`mayapy`, `nuke -t`, `hython`,
  `blender -b`).

## Verify

Launch each DCC via the launcher with a clean user profile: studio menu present, `OCIO` and project env
vars set, and the same scripts in batch mode run without UI errors.
