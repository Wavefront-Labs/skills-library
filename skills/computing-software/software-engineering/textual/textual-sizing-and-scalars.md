---
id: computing-software.software-engineering.textual.textual-sizing-and-scalars
name: textual-sizing-and-scalars
category: computing-software
field: software-engineering
product: textual
tags: [textual, css-types, scalar, width, height, min-width, fr-units, percent, styles]
level: practitioner
status: docs-checked
description: "Size Textual widgets with the scalar type: cells, fr, percent, w, h, vw, vh and auto, plus min-width and the width and height styles."
sources: [https://textual.textualize.io/styles/width/, https://textual.textualize.io/styles/height/, https://textual.textualize.io/styles/min_width/, https://textual.textualize.io/css_types/scalar/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual sizing and scalars

Goal: pick the right unit for `width`, `height` and their min/max limits.

## Method

`width: <scalar>;` and `height: <scalar>;`. A scalar is a number plus unit, or `auto`:

| Unit | Example | Meaning |
|------|---------|---------|
| (none) | `10` | cells (columns or lines); floats are truncated |
| `fr` | `1fr` | proportion of space; `1fr` beside `3fr` gets a third as much as the other |
| `%` | `75%` | relative to the container, in the same direction |
| `w` | `25w` | percent of the container width, even when used for height |
| `h` | `75h` | percent of the container height, even when used for width |
| `vw` | `25vw` | percent of viewport width (terminal width minus widgets docked left or right) |
| `vh` | `75vh` | percent of viewport height (terminal height minus widgets docked top or bottom) |
| `auto` | `auto` | optimal size to fit content without scrolling |

```css
Horizontal {
    width: 60;     /* 60 cells */
    height: 1fr;   /* proportional size of 1 */
}
min-width: 10;
min-width: 25vw;
```

```python
widget.styles.width = 16
widget.styles.height = "1fr"
widget.styles.width = "50%"
widget.styles.height = "auto"
widget.styles.min_width = "25vw"
```

`min-width` is a lower bound the width is never allowed to fall under; it does nothing when the width is already larger. `max-width`, `min-height` and `max-height` are the sibling limits.

By default `width` and `height` set the content area; with `box-sizing: border-box` they set the border area.

## Gotchas

- Do not confuse `<scalar>` with `<number>` or `<percentage>`.
- `w` and `h` units are cross-dimension capable: `height: 25w` is 25% of the container width.
- A label with `width: auto` is only as wide as its text if the container is big enough.

## Checked
2026-11-07. Read in full: width, height and min-width style pages and the scalar CSS type page. Confirmed: every unit and its meaning, float truncation, viewport definitions, auto, box-sizing note, min-width semantics and the max-width, max-height, min-height siblings, and the Python examples. Removed: the Verify section.
Method: documentation only; no commands were run.
