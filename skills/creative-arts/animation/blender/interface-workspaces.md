---
id: creative-arts.animation.blender.interface-workspaces
name: interface-workspaces
category: creative-arts
field: animation
product: blender
tags: [blender, interface, workspaces, keymap, preferences, window-system, areas, editors, startup-file, ui]
level: practitioner
status: docs-checked
description: "Set up Blender workspaces and preferences: tabs, per-workspace mode, key preferences, keymap export and import, script directories."
sources:
  - https://docs.blender.org/manual/en/latest/interface/window_system/workspaces.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/keymap.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/interface.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/input.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/navigation.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/file_paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# interface-workspaces

Goal: a Blender layout you can work in for hours and hand to a colleague. Workspaces are predefined window layouts, each a set of areas holding editors; they are saved in the blend file, and preferences are saved separately.

## Workspaces

- Workspace tabs sit in the Topbar. Click a tab to switch; double-click to rename. The `+` button adds a workspace from a template (for example Modeling, Sculpting, Compositing; also 2D Animation, VFX and Video Editing sets).
- Right-click a tab: *Duplicate* (copies the screen layout and editors), *Delete* (the last workspace cannot be removed), *Reorder to Front/Back*, *Delete Other Workspaces*.
- `Ctrl-PageUp` / `Ctrl-PageDown` activate the workspace to the left or right.
- Default workspaces: Layout (3D Viewport, Outliner, Properties, Timeline), Modeling, Sculpting, UV Editing, Texture Paint, Shading, Animation, Rendering, Compositing, Geometry Nodes, Scripting.
- **Workspace settings** (Properties editor, Tool tab > Workspace): *Mode* switches to that mode when the workspace is activated (for example a sculpt workspace entering Sculpt Mode); *Pin Scene* makes the workspace remember its scene; *Filter Add-ons* chooses which add-ons are enabled in the workspace (unchecked uses the global add-ons).
- Workspaces are saved in the blend file. When opening a file, enabling *Load UI* in the File Browser uses the file's layout instead of yours; a custom set of workspaces can be saved as part of the defaults (see the manual's Configuration > Defaults page).

## Preferences worth checking

`Edit > Preferences`.

- **Interface:** *Resolution Scale* (size of fonts and buttons relative to detected DPI). *Developer Extras* adds Operator Search, icon names in tooltips and RMB-menu entries such as Online Python Reference, Copy Python Command and Edit Source.
- **Input:** *Emulate Numpad* (number keys act as Numpad keys on keyboards without one); *Emulate 3 Button Mouse* (uses `Alt-LMB` for the middle button); tablet *Max Threshold* is the pressure needed for full intensity.
- **Navigation:** *Orbit Around Selection* (the selection centre becomes the rotation centre); *Zoom to Mouse Position* (zoom focuses on the pointer).
- **Keymap:** presets Blender (default), Blender 27x and Industry Compatible. *Spacebar Action*, *Select All Toggles* (A deselects all when anything is selected), *Tab for Pie Menu* (swaps Tab and Ctrl-Tab) and *Pie Menu on Drag* are options. *Export* saves the keymap as a preset `.py`; with *All Keymaps* off only modified shortcuts are exported (a "keymap delta"). *Import* loads a `.py` preset on another machine.
- **File Paths:** *Render Output* sets where renders are saved. *Script Directories* are extra script locations that can hold your scripts and add-ons independently of the Blender version; create subfolders matching Blender's `scripts` folder (`startup/` modules are imported on startup, `addons/` lists legacy add-ons, plus `modules/`).
- **Save & Load:** *Save Versions* sets how many backup versions are kept when saving; *Auto Save* periodically saves a temporary backup to the temp directory, with a *Timer (Minutes)*; *Default To > Load UI* sets the default for Load UI.
- **System:** *Cycles Render Devices* (choose the GPU backend) and *Undo Steps*.

## Shipping a team config

1. On one machine: build workspaces, set preferences, export the keymap `.py`.
2. Put the keymap and your scripts folder in a shared repository.
3. On other machines add the scripts folder under *Script Directories* and import the keymap.

## Gotchas

- Opening a file with *Load UI* enabled replaces your layout with the file's; untick it in the File Browser or set the default in Save & Load preferences.
- Emulate 3 Button Mouse relies on `Alt-LMB`, so check it against other `Alt` shortcuts you use.

## Verify

- Switching to a workspace with a configured Mode changes the object mode automatically.
- A second machine that imports the keymap `.py` and adds the script directory shows the same shortcuts and startup scripts.

## Checked

2026-11-09. Confirmed against the Blender manual Workspaces page (read in full) and the Preferences Keymap, Interface, Input, Navigation, Save & Load, File Paths and System pages (raw RST; partial reads of the named settings only). Removed because not on these pages: all `Shift F*` and `Ctrl Space` hotkeys, area split/join/new-window tricks, Quick Favorites, `F3`/`F9` notes, config folder paths, portable-install folder, `--factory-startup`, the startup.blend/userpref.blend file names, undo-step and auto-save default figures, and the `bpy.ops.wm.save_userpref` script.
Method: documentation only; no commands were run.
