---
id: computing-software.software-engineering.textual.textual-box-model
name: textual-box-model
category: computing-software
field: software-engineering
product: textual
tags: [textual, box-model, margin, padding, border, box-sizing, outline, styles]
level: practitioner
status: docs-checked
description: "Control Textual widget spacing with margin, padding, border and box-sizing, in both CSS and Python, including the one, two and four value forms."
sources: [https://textual.textualize.io/styles/margin/, https://textual.textualize.io/styles/padding/, https://textual.textualize.io/styles/border/, https://textual.textualize.io/styles/box_sizing/, https://textual.textualize.io/guide/styles/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual box model styles

Goal: space and frame widgets with margin, padding and border, and decide how they count toward size.

## Method

Margin is spacing outside the widget; padding is spacing inside around the content. Both take integers:

- 1 value: all edges
- 2 values: top/bottom, left/right
- 4 values: top, right, bottom, left (clockwise, like a clock hand)

```css
margin: 1;
margin: 2 4;
margin: 1 2 3 4;
margin-top: 1;
padding: 1 2 3 4;
padding-left: 4;
```

Per-edge properties exist in CSS (`margin-top`, `-right`, `-bottom`, `-left`, and the same for padding). Python has no per-edge margin or padding properties, but accepts an int or a tuple of 2 or 4:

```python
widget.styles.margin = (2, 4)
widget.styles.padding = (1, 2, 3, 4)
```

Border: `border: [<border>] [<color>] [<percentage>];` where all parts are optional and the percentage blends the border with the background. Individual edges use `border-top`, `border-right`, `border-bottom`, `border-left`.

```css
border: heavy white;
border-left: outer red;
border: round orange 50%;
```

```python
widget.styles.border = ("heavy", "white")
widget.styles.border_left = ("outer", "red")
```

Run `textual borders` to explore border types interactively.

box-sizing: `box-sizing: border-box | content-box;`

- `border-box` (default): padding and border are included in width and height, so adding them leaves the size unchanged but shrinks the content space.
- `content-box`: padding and border increase the widget size, leaving the content area unaffected.
- Python: `widget.box_sizing = "content-box"`.

## Gotchas

- `border` and `outline` cannot coexist on the same edge of a widget.
- Margins of adjacent widgets overlap; the greater one is used.

## Verify

Give two widgets height 5 with border and padding, one border-box and one content-box: the content-box widget grows taller while the border-box one keeps height 5 with less content space.

## Checked

2026-11-07: every claim was read against the full text of these pages: styles/margin, styles/padding, styles/border, styles/box_sizing, guide/styles. Added the guide/styles page to sources, which is where the margin-overlap rule is stated.

Method: documentation only; no commands were run.
