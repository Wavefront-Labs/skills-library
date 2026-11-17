---
id: computing-software.software-engineering.textual.textual-widget-line-api
name: textual-widget-line-api
category: computing-software
field: software-engineering
product: textual
tags: [textual, line-api, render-line, strip, segment, scrollview, component-classes, widgets]
level: advanced
status: docs-checked
description: "Implement a Textual widget with the line API: render_line returning Strips, component classes, ScrollView virtual size and region refreshes."
sources: [https://textual.textualize.io/guide/widgets/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual line API widgets

Goal: build widgets that redraw only what changes, so large or frequently updated widgets stay responsive. Renderable-returning widgets are redrawn in full on every change or resize. `DataTable`, `RichLog` and `Tree` use the line API.

## Method

1. Implement `render_line(self, y: int)` instead of `render`. `y` is the row offset from the top of the widget; return a `Strip` for that row. Textual calls it for each row.
2. A `Segment` (from Rich; a named tuple) is a string plus a Rich `Style`: `Segment("Hello, World!", Style(bold=True))`.
3. A `Strip` is built from a list of segments for one line:

```python
segments = [
    Segment("Hello, "),
    Segment("World", Style(bold=True)),
    Segment("!")
]
strip = Strip(segments)
```

Segments without a style use the widget default style. An optional second argument is the cell length (`Strip(segments, 13)`), counted in terminal cells, not characters (wide characters take two). Omit it if unsure and Textual calculates it.
4. Component classes let CSS style parts of a line API widget: set `COMPONENT_CLASSES` to a set of class-name strings (convention: widget name then two hyphens, for example `checkerboard--white-square`). Set defaults in `DEFAULT_CSS`; the app can override them. In `render_line` use `get_component_rich_style` to turn them into `Style` objects.
5. Scrolling: extend `ScrollView` instead of `Widget`. Set the `virtual_size` property to the size of the scrollable content (larger than the widget adds scrollbars; it can be updated dynamically). In `render_line`, add `scroll_offset.y` to `y`, and crop with `strip.crop(scroll_x, scroll_x + self.size.width)` for the horizontal scrollbar.
6. Region updates: pass `Region` objects to `refresh` to redraw only those cells; multiple regions are merged into as few non-overlapping regions as possible. Use `var` (not `reactive`) for state such as a cursor square so the whole widget is not refreshed, and refresh old and new regions in the watcher. Add `self.scroll_offset` to `event.offset` in mouse handlers to get content coordinates.

## Gotchas

- `Strip` objects are immutable; methods return a new Strip.
- Line API takes more work than renderables.

## Checked
2026-11-07. Read in full: Widgets guide (Line API section: render_line, Segment and Style, Strip, component classes, scrolling, region updates, examples). Confirmed: render_line(y) returning a Strip, Segment as Rich named tuple, Strip construction and cell-length argument, COMPONENT_CLASSES and get_component_rich_style, ScrollView virtual_size, scroll_offset and crop, Region refresh merging, var versus reactive, DataTable/RichLog/Tree as line API widgets, Strip immutability. Removed: the Verify section.
Method: documentation only; no commands were run.
