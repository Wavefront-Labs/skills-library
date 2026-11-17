---
id: computing-software.software-engineering.textual.textual-colors-and-opacity
name: textual-colors-and-opacity
category: computing-software
field: software-engineering
product: textual
tags: [textual, styles-reference, color, background, tint, opacity, css-types, alpha]
level: practitioner
status: docs-checked
description: "Set Textual text color, background, tint and opacity using named, hex, rgb, hsl and alpha color formats in CSS and Python."
sources: [https://textual.textualize.io/styles/color/, https://textual.textualize.io/styles/background/, https://textual.textualize.io/styles/opacity/, https://textual.textualize.io/styles/tint/, https://textual.textualize.io/css_types/color/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual colors and opacity

Goal: apply colors and blends to widgets correctly in CSS and Python.

## Method

Accepted `<color>` formats:

- named color: `red`
- hex `#RGB` / `#RRGGBB` (case ignored; `#A2F` equals `#AA22FF`)
- hex with alpha `#RGBA` / `#RRGGBBAA`
- `rgb(0, 255, 32)` with integers 0-255; `rgba(0, 255, 32, 0.5)` with alpha 0-1
- `hsl(290, 70%, 80%)` hue 0-360, saturation and lightness as percentages; `hsla(128, 100%, 50%, 0.5)`
- theme variables such as `$accent`

Styles:

- `color: (<color> | auto) [<percentage>];` is the text color. `auto` picks white or black text for best contrast with the background.
- `background: <color> [<percentage>];` the percentage sets opacity, clamped 0%-100%.
- `tint: <color> [<percentage>];` blends a color over the whole widget. Give it alpha (in the color or via the percentage) or it will obscure the content.
- `opacity: <number> | <percentage>;` blends the widget with its background (an approximation, since terminals lack true opacity). Number 0-1 or 0%-100%; 0 shows only the background. `70%` dims a widget, e.g. for a disabled state.

```css
color: blue;
color: red 20%;
color: auto;
background: hsl(290, 70%, 80%);
tint: red 20%;
tint: rgba(0, 200, 0, 0.3);
opacity: 50%;
```

```python
from textual.color import Color
widget.styles.color = "blue"
widget.styles.background = Color.parse("#FF00FF")
widget.styles.background = Color(120, 60, 100)
widget.styles.tint = Color.parse("red").with_alpha(0.2)
widget.styles.tint = "rgba(0, 200, 0, 0.3)"
widget.styles.opacity = "50%"
widget.styles.color = "$accent"
```

## Gotchas

- The `<color>` type is not the `color` rule (text color).
- `background-tint` blends a color with the background only; `tint` affects the whole widget; `text-opacity` blends only content color.

## Verify

`Color.parse("#A8F")` parses the CSS syntax into a `Color`, and `opacity: 0` leaves only the background visible.

## Checked

2026-11-07: every claim was read against the full text of these pages: styles/color, styles/background, styles/opacity, styles/tint, css_types/color. Nothing needed removing.

Method: documentation only; no commands were run.
