---
id: computing-software.software-engineering.textual.textual-center-and-align
name: textual-center-and-align
category: computing-software
field: software-engineering
product: textual
tags: [textual, center, align, content-align, text-align, layout, center-container, tcss]
level: practitioner
status: docs-checked
description: "Center widgets and text in Textual by choosing between align, text-align and content-align, and use the Center container to center widgets independently."
sources: [https://textual.textualize.io/how-to/center-things/, https://textual.textualize.io/styles/align/, https://textual.textualize.io/styles/content_align/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centering things in Textual

Goal: pick the right alignment rule for the thing being centered.

## Method

Three rules, three targets:

| Rule | Applied to | Aligns |
|---|---|---|
| `align` | the parent container (often `Screen`) | the container's child widgets |
| `text-align` | the widget | text, line by line (left is default; also right and justify) |
| `content-align` | the widget | the content as a rectangle inside the widget's border |

1. Centre a widget: put `align: center middle;` on its container. `center` is the horizontal part, `middle` the vertical part. Per-axis forms: `align-horizontal` and `align-vertical`.
2. The widget must be smaller than its container or it has no room to move. A `Static` is as wide as the screen by default, so text looks left aligned; set `width: auto;` (just wide enough for the content) or a smaller fixed width.
3. Centre wrapped text inside a narrow widget with `text-align: center;`.
4. Centre content inside a widget larger than its content with `content-align: center middle;`. Content defaults to the top. Per-axis: `content-align-horizontal` and `content-align-vertical` (for example `content-align-vertical: middle;`).
5. `align` on a parent moves all children as one group; their positions relative to each other do not change. To centre each widget independently, wrap each in the builtin `Center` container.

```css
Screen { align: center middle; }
#hello { width: auto; }
```

Python equivalents:

```python
widget.styles.align = ("center", "middle")
widget.styles.content_align = ("center", "middle")
widget.styles.align_horizontal = "right"
```

Other values from the page: `align: right top;`, `content-align: right top;`.

## Gotchas

- `align` applies to widgets, not text.
- When alignment misbehaves, add a border to the widget to see its real size.

## Verify

Run an app with `Screen { align: center middle; }` and a `Static` with `width: auto;` and a border: the bordered widget sits in the middle of the screen on both axes.

## Checked

2026-11-07: every claim was read against the full text of these pages: how-to/center-things, styles/align, styles/content_align. Nothing needed removing.

Method: documentation only; no commands were run.
