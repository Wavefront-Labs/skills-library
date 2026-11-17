---
id: creative-arts.animation.blender.python-console-autocomplete
name: python-console-autocomplete
category: creative-arts
field: animation
product: blender
tags: [blender, python-console-autocomplete, console-autocomplete, info-editor, python-console, python-tooltips, copy-data-path, bpy]
level: intro
status: docs-checked
description: "Explore bpy interactively: Python Console autocomplete and history, C and D shortcuts, Info editor operator log, Python tooltips and copying data paths into scripts."
sources:
  - https://docs.blender.org/manual/en/latest/editors/python_console.html
  - https://docs.blender.org/manual/en/latest/editors/info_editor.html
  - https://docs.blender.org/manual/en/latest/interface/controls/buttons/menus.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/interface.html
  - https://docs.blender.org/api/current/info_quickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# python-console-autocomplete

Goal: find the exact Python for any UI action in seconds instead of guessing from the API reference.

## Python Console (Scripting workspace, or any area → Python Console)

- **Autocomplete:** type a partial name and press `Tab` (*Console → Autocomplete*); submodules are listed in green, and methods are shown with a trailing `(`. It works on live objects, so `C.object.modifiers["Subdivision"].` + `Tab` lists that modifier's properties.
- Convenience names: `C` = `bpy.context`, `D` = `bpy.data`, and `bpy`; `dir()` lists everything else in the console's globals.
- **History:** `Up` / `Down` (*Backward / Forward in History*); *Console → Copy as Script* (`Shift Ctrl C`) copies the full history buffer to the clipboard so it can be pasted into a text file as a script. `Shift Return` adds a line to the history without executing it.
- *View → Zoom In / Zoom Out* changes the font size.
- The console's context is the console area: `C.area.type == 'CONSOLE'`, so `bpy.ops.view3d.*` operators fail their poll here. Use `bpy.context.temp_override` (see `creative-arts.animation.blender.bpy-ops-temp-override`).

## Info editor: the operator log

The Info editor logs executed operators as well as errors, warnings and informational messages.
- Select entries (click, `Shift` click to add, `B` box select, `A` all), `Ctrl C` copies them to the clipboard; paste into the Text Editor as a starting macro.
- `X` / `Delete` removes the selected entries from the log.

## Tooltips and data paths

- *Preferences → Interface → Python Tooltips* displays a property's Python information below the tooltip.
- Right-click a property → *Copy Data Path* (`Shift Ctrl C`) gives the relative path (`modifiers["Bevel"].width`); *Copy Full Data Path* (`Shift Ctrl Alt C`) gives `bpy.data.objects["Cube"].modifiers["Bevel"].width`.
- *Preferences → Interface → Developer Extras* adds *Online Python Reference*, *Copy Python Command* and *Edit Source* (edit the Python source that defines the button) to the right-click menu.

## Gotchas

- Logged operator calls can depend on UI context and may fail when replayed from a script elsewhere (practice); trim the arguments you do not need.

## Verify

Type `C.active_object.` + `Tab` and see the property list; run an operator from a menu and find its exact call in the Info editor; paste a Copy Full Data Path result into the console and get the live value back.

## Checked

Blender 5.2 manual (blender-v5.2-release), read 2026-10-27.
- Python Console menu items and shortcuts (Autocomplete Tab, Backward/Forward in History Up/Down, Copy as Script Shift-Ctrl-C, Shift-Return adds to history, Zoom In/Out), aliases C/D/bpy, auto-completion colours: editors/python_console page.
- Info editor selection, box select, copy, delete: editors/info_editor page. Copy Data Path Shift-Ctrl-C and Copy Full Data Path Shift-Ctrl-Alt-C: interface menus page. Python Tooltips and Developer Extras menu entries (Online Python Reference, Copy Python Command, Edit Source): preferences interface page.
- Removed as unconfirmed: Ctrl Space and Ctrl Up/Down, mathutils pre-imports, Report Types filter, claims about which UI actions log, and print() routing.

Method: documentation only; no commands were run.
