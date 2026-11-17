---
id: creative-arts.animation.pipeline.ayon-launcher-environments
name: ayon-launcher-environments
category: creative-arts
field: animation
product: pipeline
tags: [ayon-launcher, ayon, openpype, application-environments, applications-addon, tool-environments, launch-context, studio-env]
level: advanced
status: draft
description: "Configure Ayon launcher applications and tool environments: executables per OS, environment variables per app/version/project, and launching DCCs in context."
sources:
  - https://ayon.ynput.io/docs/admin_settings_system/
  - https://ayon.ynput.io/docs/artist_getting_started/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ayon launcher and application environments

**Goal:** artists pick project, shot and task in the launcher and the right DCC version opens with the right
plugins, OCIO config and pipeline menu: no manual setup per machine.

## Applications addon

Studio settings - Applications: for each app (Maya, Blender, Nuke, Houdini, Harmony, AE...):
- **Variants** (e.g. Maya 2024, 2025) with executables per platform (list several install paths; first that
  exists is used).
- **Arguments** per variant.
- **Environment** (JSON) per app and per variant, with `{AYON_...}`/existing env var expansion, e.g.
```json
{ "OCIO": "{STUDIO_ROOT}/ocio/show_aces_v2/config.ocio",
  "MAYA_MODULE_PATH": ["{STUDIO_ROOT}/maya/modules", "{MAYA_MODULE_PATH}"] }
```
Project settings can enable a subset of applications and override environments for that production.

## Tools

Tools (Studio settings - Tools) are extra environment groups (renderers like Arnold/Redshift versions,
plugins) that artists or projects enable per task; they merge into the app environment at launch.

## Launch context

When launching from a task, Ayon sets context variables (project, folder path, task, fps, frame range,
resolution from attributes) so the DCC integration opens the right work file area and applies scene settings
(`creative-arts.animation.scripting.dcc-startup-scripts` covers what the DCC side does with them).

## Gotchas

- Variables are merged; a path variable overwritten instead of appended removes the DCC's defaults. Include
  the existing value (`{MAYA_MODULE_PATH}`) when appending.
- Executables missing on a machine show the app greyed out; check per-platform paths.
- Keep secrets (licence server credentials, tokens) out of environment JSON committed to settings history.

## Verify

Launch an app from a task on two workstations: `os.environ` inside the DCC shows the expected OCIO and
context variables, the Ayon menu is present, and the work file dialog opens in the task's folder.
