---
id: computing-software.software-engineering.textual.textual-styles-object
name: textual-styles-object
category: computing-software
field: software-engineering
product: textual
tags: [textual, styles, colors, dimensions, widget-styles, alpha, fr-units, python]
level: practitioner
status: docs-checked
description: "Set widget appearance from Python with widget.styles: colors with alpha, width and height units, padding, border, outline, box-sizing and margin."
sources: [https://textual.textualize.io/guide/styles/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual styles object

Goal: style widgets in Python when CSS is not suitable (for example dynamic values).

## Method

Every widget has a `styles` object; setting an attribute updates the screen.

```python
self.screen.styles.background = "darkblue"
self.screen.styles.border = ("heavy", "white")
```

For a child widget, keep a reference in `compose` and set styles in the mount handler.

- Colors: `color` (text) and `background`. Accept names (`"crimson"`), hex (`#f00`, `#9932CC`), `rgb(255,0,0)`, `hsl(0,100%,50%)`, or a `Color` object.
- Alpha: hex with extra digits (`"#9932CC7f"`), `rgba(192,78,96,0.5)` (0 invisible to 1 opaque), or `Color(192, 78, 96, a=0.5)`. Alpha on a background blends with what is beneath; on text it blends with the background.
- Width and height: integers (cells) or `"auto"` to fit content. Units: `"50%"` of the parent, `vw`/`vh` of terminal width/height, `w`/`h` of available width/height, and `fr` units, which divide available space by the sum of the fr values (`"2fr"` and `"1fr"` give two thirds and one third).
- Limits: `min-width`, `max-width`, `min-height`, `max-height`.
- Padding: integer, a two-tuple (top/bottom, left/right), or four values (top, right, bottom, left).
- Border: tuple of (type, color). Preview types with `textual borders`.
- `border_title` / `border_subtitle` show in the top and bottom border; alignment via `border-title-align` (default left) and `border-subtitle-align` (default right).
- Outline: set like border but does not change widget size and may overlap content.
- `box_sizing`: default `"border-box"`; `"content-box"` adds padding and border to the dimensions.
- Margin: space outside the border; margins of adjacent widgets overlap, the greater wins.

## Gotchas

- A border adds two rows and two columns; padding and border shrink the content area, not the widget (with border-box).
- A fixed height can truncate wrapped text; use `"auto"`.

## Checked
2026-11-07. Read in full: Styles guide. Confirmed: styles object, colour formats, alpha forms, dimensions and units (%, vw/vh, w/h, fr), min/max styles, padding tuple forms, border tuple and textual borders, border title and subtitle alignment defaults, outline, box_sizing default, margin overlap. Removed: the Verify section.
Method: documentation only; no commands were run.
