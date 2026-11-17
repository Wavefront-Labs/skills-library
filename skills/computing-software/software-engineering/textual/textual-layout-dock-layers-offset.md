---
id: computing-software.software-engineering.textual.textual-layout-dock-layers-offset
name: textual-layout-dock-layers-offset
category: computing-software
field: software-engineering
product: textual
tags: [textual, layout, dock, layers, layer, offset, sidebar, tcss]
level: practitioner
status: docs-checked
description: "Dock widgets to container edges, order overlapping widgets with layers, and shift widgets with the offset style in Textual CSS."
sources: [https://textual.textualize.io/guide/layout/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual docking, layers and offsets

Goal: fix sidebars and headers in place, control draw order, and nudge widgets after layout.

## Method

**Dock.** `dock: <EDGE>;` where EDGE is `top`, `right`, `bottom` or `left`. Docking removes the widget from the layout and fixes it to that edge of its container; docked widgets do not scroll out of view, so they suit sticky headers, footers and sidebars. A left sidebar: `dock: left;`.

- Multiple widgets docked to the same edge overlap. The widget yielded first from `compose` is drawn below those yielded after it.
- You can dock to several edges in one container. The built-in `Header` has internal CSS that docks it to the top, so yielding it needs no extra CSS.
- To put a sidebar below the header, yield the sidebar before the header.

**Layers.** Textual draws lower layers first, so higher layers appear on top.

- Define names on a container: `layers: one two three;` (leftmost is lowest, rightmost highest).
- Assign a descendant: `layer: three;` puts it on the top layer.
- Layers override yield order: if `#box1` is yielded before `#box2` but their layers are reversed, `#box1` ends up on top.

**Offset.** A widget's offset is added after its parent's layout has placed it; the default is `(0, 0)`. `offset` takes two values: x (positive moves right, negative left) then y (positive moves down, negative up).

```css
#box { offset: 2 -1; }
```

## Verify

Dock a widget with `dock: left;` in a scrolling container and scroll the body: the docked sidebar stays in place while the body text scrolls.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/layout. Removed the unverifiable gotcha about the position style.

Method: documentation only; no commands were run.
