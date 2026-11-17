---
id: creative-arts.animation.blender.themes-ui-scale
name: themes-ui-scale
category: creative-arts
field: animation
product: blender
tags: [blender, preferences, themes, ui-scale, resolution-scale, interface-preferences, hidpi, accessibility]
level: practitioner
status: docs-checked
description: "Tune Blender's look for the monitor and task: Resolution Scale, Line Width, tooltips, text rendering and fonts, translation, and theme presets saved as XML."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/interface.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/themes.html
  - https://docs.blender.org/api/current/bpy.types.PreferencesView.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# themes-ui-scale

Goal: a readable UI on 4K, laptops and projectors, and theme colours that make selection and keyframes obvious.

## Preferences > Interface

- **Resolution Scale:** adjusts the size of fonts and buttons relative to the automatically detected DPI (Python `preferences.view.ui_scale`, range 0.5 to 6, default 1.0). The manual notes that zoom is available in many parts of the interface and may be preferable in normal use.
- **Line Width:** thickness of outlines, lines and dots (including edges and vertices in the 3D Viewport): Thin, Default (automatic, based on UI scale), Thick.
- **Splash Screen**, **Developer Extras** (operator search, Preferences developer tools tab, icon names in tooltips, extra context-menu items such as Copy Python Command), **Tooltips** (User Tooltips; **Python Tooltips** shows a property's Python information under the tooltip).
- **Text Rendering:** Anti-Aliasing, Subpixel Anti-Aliasing, Hinting, **Interface Font** and **Mono-space Font** replacements (the latter used in the Text editor and Python Console).
- **Language** section: Language, Translate (Tooltips, Interface, New Data), date and time format. Accessibility: Reduce Motion.

## Preferences > Themes

- Choose a theme from the Theme Presets list; Blender bundles a small selection (the manual's example is Blender Light).
- **Add Theme**, **Remove Theme**, **Save Theme** (writes an XML file to the `scripts/presets/interface_theme/` subdirectory of a configuration directory), **Install** (load and apply a Blender XML theme file and add it to the presets), **Reset** (back to default theme colours).
- Colours are set per editor: pick the editor in the list on the left and adjust; changes show in real time. Some details such as dot size in the 3D Viewport or Graph Editor are also editable.

## Gotchas

- The Gizmo Size preference is separate from Resolution Scale (API: `gizmo_size`, range 10 to 200, default 75); use it for viewport gizmos alone.
- Preferences are saved automatically unless Auto-Save Preferences was changed; share a theme as its XML file via Save Theme and Install.

## Verify

Restart Blender: settings persist; install the exported XML on another machine and confirm the colours match.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/preferences/interface.rst, editors/preferences/themes.rst, getting_started/configuration/defaults.rst) and the current Python API (PreferencesView.ui_scale, ui_line_width, gizmo_size).
Confirmed: option names and meanings, Line Width values, Python property ranges and defaults, theme preset buttons and save location. Removed unconfirmed claims: a 0.25 to 4.0 scale range, 4K scale recommendations by OS DPI percentage, the "Auto" label for Line Width (the UI label is Default), a Navigation Controls gizmo option, a "New Data translation off in studios" recommendation, specific theme colour fields to tweak, and the claim that older theme XML falls back silently.
Method: documentation only; no commands were run.
