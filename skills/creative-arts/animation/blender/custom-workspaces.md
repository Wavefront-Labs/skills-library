---
id: creative-arts.animation.blender.custom-workspaces
name: custom-workspaces
category: creative-arts
field: animation
product: blender
tags: [blender, workspaces, custom-workspaces, workspace-tabs, workspace-settings, interface, pipeline]
level: practitioner
status: docs-checked
description: "Build task-specific Blender workspaces: add from templates, duplicate, reorder tabs, set Mode, Pin Scene and Filter Add-ons, then save them in the startup file."
sources:
  - https://docs.blender.org/manual/en/latest/interface/window_system/workspaces.html
  - https://docs.blender.org/manual/en/latest/getting_started/configuration/defaults.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# custom-workspaces

Goal: one tab per job (layout, rigging, lookdev, review) that opens in the right mode with only the tools that job needs.

## Create and order

- Workspace tabs sit in the Topbar. Click to switch; double-click to rename.
- `+` (Add Workspace) creates one from a template. The manual lists defaults Modeling, Sculpting, UV Editing, Texture Paint, Shading, Animation, Rendering, Compositing, Geometry Nodes, Scripting (plus Layout at startup), and additional templates: 2D Animation, 2D Full Canvas, Masking, Motion Tracking, Video Editing.
- Right-click a tab: **Duplicate** (copy including screen layout and editors), **Delete** (the last workspace cannot be removed), **Reorder to Front/Back**, **Delete Other Workspaces**.
- `Ctrl-PageUp` / `Ctrl-PageDown`: previous/next workspace.

## Workspace settings (Properties editor > Tool tab > Workspace panel)

- **Mode:** switch to this mode when the workspace is activated.
- **Pin Scene:** the workspace remembers the currently selected scene and switches back to it whenever it is activated.
- **Sequencer Scene** and **Sync Scene Time:** tie the Video Sequencer to a scene (see the video editing pages).
- **Filter Add-ons:** when unchecked, the global add-ons apply; when checked, you enable individual add-ons for this workspace from the list.

## Save and share

- Workspaces are saved in the .blend. `File > Defaults > Save Startup File` stores the scene and UI setup used at startup and for `File > New`; preferences (keymap, add-ons, themes) are stored separately and saved automatically unless you changed Auto-Save.
- When opening a file, **Load UI** in the File Browser decides whether the file's screen layout replaces the current one. Preferences > Save & Load > Default To > Load UI sets its default.

## Gotchas

- With Load UI enabled, opening a file brings its workspaces; disable it to keep yours.

## Verify

Restart Blender or use `File > New`: the tabs appear in order, and switching enters the declared mode and pinned scene.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (interface/window_system/workspaces.rst, getting_started/configuration/defaults.rst, editors/preferences/save_load.rst).
Confirmed: tab controls and context menu entries, template names, shortcuts, workspace setting names and meanings, startup file and Load UI behaviour. Removed unconfirmed claims: a "General" template group and "Sculpting / VFX" grouping, drag-to-reorder tabs, Filter Add-ons affecting UI only, Append of a Workspace data-block and app-template shipping advice, screen data size remarks, and failing silently on unsupported modes.
Method: documentation only; no commands were run.
