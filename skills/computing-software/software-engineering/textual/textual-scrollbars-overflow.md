---
id: computing-software.software-engineering.textual.textual-scrollbars-overflow
name: textual-scrollbars-overflow
category: computing-software
field: software-engineering
product: textual
tags: [textual, styles-reference, overflow, scrollbar-size, scrollbar-gutter, scrolling, containers]
level: practitioner
status: docs-checked
description: "Control Textual scrolling with overflow, overflow-x, overflow-y, scrollbar-size and scrollbar-gutter in CSS and Python."
sources: [https://textual.textualize.io/styles/overflow/, https://textual.textualize.io/styles/scrollbar_size/, https://textual.textualize.io/styles/scrollbar_gutter/, https://textual.textualize.io/css_types/overflow/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual scrollbars and overflow

Goal: decide when scrollbars appear, how wide they are, and whether space is reserved for them.

## Method

### overflow

`overflow: <overflow> <overflow>;` sets horizontal then vertical. Per axis: `overflow-x`, `overflow-y`. Values: `auto` (decide automatically), `hidden` (no scrollbar, no overflow), `scroll` (always allow/show).

```css
overflow: auto auto;     /* default for containers */
overflow-y: hidden;
overflow-x: scroll;
```

```python
widget.styles.overflow_y = "hidden"
widget.styles.overflow_x = "scroll"
```

Python cannot set both axes at once; set each axis separately.

### scrollbar-size

`scrollbar-size: <integer> <integer>;` is horizontal then vertical, the scrollbar width (its length is always 100% of the container). Individually: `scrollbar-size-horizontal`, `scrollbar-size-vertical`.

```css
scrollbar-size: 10 4;
scrollbar-size-horizontal: 10;
scrollbar-size-vertical: 4;
```

```python
widget.styles.scrollbar_size_horizontal = 10
widget.styles.scrollbar_size_vertical = 4
```

Set the size to `0` to hide the scrollbar while still allowing scrolling by mouse wheel or keyboard. There is no Python equivalent of the combined `scrollbar-size`.

### scrollbar-gutter

`scrollbar-gutter: auto | stable;`

- `auto` (default): no space reserved for a vertical scrollbar; layout is recomputed when one becomes needed.
- `stable`: space is reserved, preventing layout shifts when the scrollbar appears.

```python
self.styles.scrollbar_gutter = "stable"
```

## Gotchas

- Built-in containers such as `Horizontal` and `VerticalScroll` override the `auto auto` default.
- `hidden` prevents a scrollbar even when content does not fit.

## Checked
2026-11-07. Read in full: overflow, scrollbar-size and scrollbar-gutter style pages and the overflow CSS type page. Confirmed: syntax and axis order, auto/hidden/scroll values, the auto auto container default and the Horizontal/VerticalScroll override warning, Python axis limitation, scrollbar-size order and no combined Python property, size 0 tip, scrollbar-gutter auto/stable. Removed: the Verify section.
Method: documentation only; no commands were run.
