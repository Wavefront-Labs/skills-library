---
id: computing-software.game-programming.godot.themes-and-theme-overrides
name: themes-and-theme-overrides
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-ui, godot-theme, theme-overrides, theme-type-variations, stylebox, game-programming]
level: practitioner
status: docs-checked
description: "Style Godot UI with Theme resources: theme inheritance down the tree, StyleBoxes, fonts and constants, type variations, per-node overrides and the project-wide default theme."
sources: ["https://docs.godotengine.org/en/stable/tutorials/ui/gui_skinning.html", "https://docs.godotengine.org/en/stable/tutorials/ui/gui_theme_type_variations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Themes and theme overrides

**Goal:** consistent UI styling from one Theme resource, with variants instead of hundreds of overrides.

## How themes apply
- A `Theme` resource holds items per **control type**: colors, constants, fonts, font sizes, icons, StyleBoxes.
- Assign a Theme to a Control: it applies to that control and **all descendants** (until another Theme).
- Project Settings > GUI > Theme > **Custom** sets the project-wide theme and **Custom Font** the default
  fallback font. The built-in default theme is constant; a custom theme overrides items of it.
- Lookup order: node's theme overrides -> nearest ancestor Theme -> project theme -> default engine theme.

## Theme editor
Open the .tres: add types (Button, Label, PanelContainer...), then items:
- StyleBox types: `StyleBoxFlat`, `StyleBoxTexture` and `StyleBoxEmpty` (see the class reference for their properties).
- Button StyleBoxes: `normal`, `hover`, `pressed`, `hover_pressed`, `disabled`, `focus` (keep `focus`
  visible for gamepad users).
- Fonts and font sizes are theme items too (`font`, `font_size`).

## Type variations (named styles)
Create a type "HeaderLabel" with **Base Type = Label**, set its font size and color, then on a Label set
`theme_type_variation = "HeaderLabel"`. Use for primary/secondary buttons, title labels, danger buttons.
Far better than per-node overrides.

## Per-node overrides
Inspector > Theme Overrides, or code:
```gdscript
label.add_theme_color_override("font_color", Color.RED)
label.add_theme_font_size_override("font_size", 32)
button.add_theme_stylebox_override("normal", preload("res://ui/danger_normal.tres"))
label.remove_theme_color_override("font_color")
var c := get_theme_color("font_color", "Label")
```
Use overrides for runtime state (flashing red), not for static design.

## Gotchas
- StyleBoxes are resources: modifying one at runtime changes every control sharing it; `duplicate()` first.
- With stretch mode `canvas_items`, 2D elements (including UI) are scaled from the base size.
- A type variation must be defined in the project theme or the default theme to appear in the inspector
  (you can type another name manually, but keep variations in the project theme). A theme set on a Control
  also applies to its descendants and is looked up before the project and default themes.

## Verify
- [ ] Changing one Theme item restyles every screen consistently.
- [ ] Scenes contain few static theme overrides (use them for layout constants and runtime state).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: lookup order (local override, then themes on the control and its ancestors, then the project theme, then the default theme); local overrides do not affect children; Project Settings > GUI > Theme > Custom and Custom Font; type variations with a Base Type and `theme_type_variation`, chaining and the project-theme recommendation; `add_theme_*_override`, `remove_theme_color_override` and `get_theme_color` exist on Control; Button theme styles `normal`, `hover`, `pressed`, `hover_pressed`, `disabled`, `focus`. Removed the unconfirmed focus-draw-order, FontVariation, pixel-size and case-sensitivity claims.

Method: documentation only; no commands were run.
