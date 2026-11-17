---
id: computing-software.software-engineering.textual.textual-layout-vertical-horizontal
name: textual-layout-vertical-horizontal
category: computing-software
field: software-engineering
product: textual
tags: [textual, layout, vertical, horizontal, containers, fr-units, overflow, tcss]
level: practitioner
status: docs-checked
description: "Arrange Textual widgets with the vertical and horizontal layouts, handle overflow scrolling, and compose nested utility containers with context managers."
sources: [https://textual.textualize.io/guide/layout/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual vertical and horizontal layouts

Goal: place child widgets top to bottom or left to right, and keep them visible or scrollable.

## Method

1. Vertical (top to bottom): `layout: vertical;` in CSS, or `widget.styles.layout = "vertical"` at runtime. Screens already use `vertical` by default, so the declaration is optional on `Screen`.
2. Widgets expand to the width of their parent, not its height. Give children `height: 1fr;` so they share the available height equally.
3. If children's total height exceeds the parent (for example `height: 10;`), a scrollbar is added automatically because `Screen` has `overflow-y: auto;`.
4. Horizontal (left to right): `layout: horizontal;`. Children must be given a width (for example `width: 1fr;`) and, to fill the container's height, `height: 100%;`.
5. Without a width limit each child grows to the parent width and only the first is visible; the rest are offscreen to the right. Textual does not add a horizontal scrollbar for you, so add `overflow-x: auto;` to the parent.
6. Utility containers `Vertical`, `Horizontal` and `Grid` come with the matching layout. A 2x2 arrangement is one `Horizontal` holding two `Vertical` containers.
7. Prefer context managers when composing: inside `compose`, `with Horizontal():` then `yield` children within the block; they become children of that container. You can mix this with positional-argument children.

```python
def compose(self) -> ComposeResult:
    with Horizontal():
        with Vertical():
            yield Static("One")
            yield Static("Two")
        with Vertical():
            yield Static("Three")
            yield Static("Four")
```

## Gotchas

- Do not build advanced grid-like layouts from many nested utility containers; the page recommends grid layout for that.
- Horizontal overflow never scrolls unless `overflow-x: auto;` is set.

## Verify

Run the app: with `layout: horizontal` and `width: 1fr;` all children appear side by side; delete the width and only the first remains visible until `overflow-x: auto;` adds a scrollbar.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/layout. Nothing needed removing.

Method: documentation only; no commands were run.
