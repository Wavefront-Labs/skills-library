---
id: computing-software.software-engineering.textual.textual-border-titles
name: textual-border-titles
category: computing-software
field: software-engineering
product: textual
tags: [textual, border, border-title, border-subtitle, alignment, markup, box-model-styles]
level: practitioner
status: docs-checked
description: "Show and style Textual border titles and subtitles with border_title, border_subtitle, border-title-align, border-subtitle-align and border-title-color."
sources: [https://textual.textualize.io/styles/border_title_align/, https://textual.textualize.io/styles/border_subtitle_align/, https://textual.textualize.io/styles/border_title_color/, https://textual.textualize.io/guide/styles/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual border titles

Goal: label a bordered widget with a title and subtitle and control their alignment and color.

## Method

Widgets have `border_title` and `border_subtitle` attributes; when set they appear within the border.

```python
widget.border_title = "Title"
widget.border_subtitle = "Subtitle"
```

Alignment styles take left, center or right:

```css
border-title-align: left;      /* default */
border-subtitle-align: right;  /* default */
border-title-align: center;
```

```python
widget.styles.border_title_align = "center"
widget.styles.border_subtitle_align = "left"
```

Color: `border-title-color: (<color> | auto) [<percentage>];`

```css
border-title-color: red;
```

```python
widget.styles.border_title_color = "red"
```

Alignment places the text along the edge so the border corners stay visible.

## Gotchas

- If the widget has no border, or the border is `none`/`hidden`, the title and subtitle are not shown.
- An empty title or subtitle is not displayed.
- Long titles are truncated and take as much space as possible; setting an alignment then has no effect until the text is shortened or the widget widened.
- If the aligned side has no border edge, the title is flush to that side of the widget.
- Padding affects title positioning.
- Titles may contain Rich markup, nested markup and Rich links.

## Verify

Create a Label with `border_title`, a border, and `border-title-align: center`: the title appears centered in the top edge with both corners visible.

## Checked

2026-11-07: every claim was read against the full text of these pages: styles/border_title_align, styles/border_subtitle_align, styles/border_title_color, guide/styles. Nothing needed removing.

Method: documentation only; no commands were run.
