---
id: computing-software.software-engineering.textual.textual-containers-scrolling
name: textual-containers-scrolling
category: computing-software
field: software-engineering
product: textual
tags: [textual, containers, scroll, vertical, horizontal, verticalscroll, groups, center]
level: practitioner
status: docs-checked
description: "Choose the right Textual container: Horizontal and Vertical, the Group variants, the Scroll variants, and Center, Right and Middle, plus a custom container template."
sources: [https://textual.textualize.io/how-to/work-with-containers/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual containers

Goal: pick a container that arranges children the way you need and scrolls when content overflows.

## Method

Containers are compound widgets with preset styles. `Horizontal` is just:

```python
class Horizontal(Widget):
    """An expanding container with horizontal layout and no scrollbars."""

    DEFAULT_CSS = """
    Horizontal {
        width: 1fr;
        height: 1fr;
        layout: horizontal;
        overflow: hidden hidden;
    }
    """
```

Use them with `with` in `compose`: widgets yielded inside `with Horizontal():` form a row (they stay in a row if added or removed later). Without a container, widgets stack vertically.

| Container | Behaviour |
|---|---|
| `Horizontal`, `Vertical` | Expand to fill remaining space; two of them split it in half, three in thirds. Good for macro layout, not tightly packed rows |
| `HorizontalGroup`, `VerticalGroup` | Similar to the non-group versions but do not expand to fill the screen; they fit to the height of their contents |
| `HorizontalScroll`, `VerticalScroll` | Add scrollbars automatically when needed |
| `Center`, `Right` | Align children horizontally (no `Left`, it is the default); expand horizontally, only as tall as needed |
| `Middle` | Aligns children on the vertical axis; expands vertically, fits horizontally |

- Horizontal, Vertical and the Group variants do not scroll; overflowing widgets are offscreen. Swap in a Scroll container, or use the `overflow` style.
- Set the layout of any compound widget with the `layout` rule; set alignment in TCSS with `align`.
- Add a border class to a container to see its real size.
- Custom container template:

```python
class MyContainer(Widget):
    """My custom container."""
    DEFAULT_CSS = """
    MyContainer {
        # Your rules here
    }
    """
```

The container reference lists more containers; new ones may be added in later versions.

## Verify

Add 10 boxes inside a `Vertical`: the extras are off-screen. Replace it with `VerticalScroll`: a draggable scrollbar appears and all boxes can be reached.

## Checked

2026-11-07: every claim was read against the full text of these pages: how-to/work-with-containers. Reworded the Group container description to match the page (do not expand to fill the screen; fit to contents height).

Method: documentation only; no commands were run.
