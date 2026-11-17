---
id: creative-arts.animation.blender.keymap-editor
name: keymap-editor
category: creative-arts
field: animation
product: blender
tags: [blender, keymap, keymap-editor, keymap-preferences, key-config, hotkeys, industry-compatible, preferences]
level: practitioner
status: docs-checked
description: "Edit Blender's keymap safely: presets (Blender, Blender 27x, Industry Compatible), filter by name or key binding, keymap preferences, edit items, export and import key configs."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/keymap.html
  - https://docs.blender.org/manual/en/latest/interface/keymap/index.html
  - https://docs.blender.org/manual/en/latest/interface/window_system/areas.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# keymap-editor

Goal: change or add hotkeys without breaking stock behaviour, and carry the result between machines.

## Preferences > Keymap

- **Keymap presets:** *Blender* (default; used throughout the manual), *Blender 27x* (legacy keymap from 2.79 and before), *Industry Compatible* (closer to other 3D applications). Add or remove a custom keymap configuration with the plus and minus buttons.
- **Preferences** (these apply only to the *Blender* keymap): Select with Mouse Button (Left or Right), Spacebar Action (Play, Tools, Search; with a non-Play choice `Shift-Spacebar` plays), Activate Gizmo Event (Press or Drag, only with Left select), Tool Keys (Immediate or Active Tool), Alt Click Tool Prompt, Alt Tool Access, Select All Toggles, Region Toggle Pie, plus 3D Viewport options (Grave Accent / Tilde Action, Middle Mouse Action, Tab for Pie Menu, Pie Menu on Drag, Transform Navigation with Alt) and a File Browser option (Open Folders on Single Click).
- **Filtering:** *Filter Type* is Name (for example `New File`) or Key Binding (for example `ctrl n`); *Search* holds the text, blank shows all operations. Use key-binding search to spot conflicts.

## Editing items

Find the operation, choose whether it is triggered by a keyboard key, mouse button or something else, click the button on the right and press the new shortcut. Each item has:
- **Active** checkbox to disable it.
- **Map Type:** Keyboard, Mouse, NDOF, Tweak, Text Input, Timer (internal).
- **Operator ID Name:** the operator identifier (for example `object.shade_smooth`; the manual points to the `bpy.ops` reference, dropping the `bpy.` prefix).
- **Event:** Type, Value (press, release, click, drag and so on) and Modifier keys.
- **Operator Properties:** initial values for the operator.

## Export / import

- **Export** saves the current keymap configuration as a preset; with **All Keymaps** off, only modified assignments are written (a keymap "delta"), with it on the whole keymap is written.
- **Import** opens a File Browser to select a `.py` file containing a custom preset.
- Version-control the exported delta and re-import it after upgrades.

## Gotchas

- Many keyboard shortcuts depend on which editor the cursor is over, so a new binding may only work in the editor whose keymap you added it to.
- Industry Compatible changes many shortcuts, so tutorials written for the Blender keymap will not match.
- Preferences are saved automatically unless you changed Auto-Save Preferences.

## Verify

Searching by key binding shows the entry you expect for the new combination; restart Blender and confirm it persists.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/preferences/keymap.rst, interface/keymap/index.rst, interface/window_system/areas.rst, getting_started/configuration/defaults.rst).
Confirmed: preset names, preference names and values, filter types, item fields, export "All Keymaps" behaviour, import. Removed unconfirmed claims: the Industry Compatible description as "Maya-like Q/W/E/R", an `Emulate 3 Button Mouse` note placed here, an "Add New" button and RMB "Assign Shortcut" workflow, per-item Restore, the config/presets/keyconfig import location, add-on keymap behaviour, and the "narrowest map wins" rule.
Method: documentation only; no commands were run.
