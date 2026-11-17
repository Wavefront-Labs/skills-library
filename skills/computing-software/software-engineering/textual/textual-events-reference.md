---
id: computing-software.software-engineering.textual.textual-events-reference
name: textual-events-reference
category: computing-software
field: software-engineering
product: textual
tags: [textual, events-reference, event-reference, mouse-events, mount, resize, click, tui]
level: practitioner
status: docs-checked
description: "Reference for Textual Mount, Key, Click and Resize events: the attributes each carries, Click bubbling and double-click chains."
sources: [https://textual.textualize.io/events/mount/, https://textual.textualize.io/events/key/, https://textual.textualize.io/events/click/, https://textual.textualize.io/events/resize/, https://textual.textualize.io/guide/events/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual events reference

Goal: pick the right event and know its payload.

## Method
- `Mount`: sent when a widget is mounted and may receive messages. Related events: `Load`, `Unmount`.
- `Key`: created when the user presses a key (guide). Fields `key` (the key pressed), `character` (printable character or `None`); properties `name` (usable as a Python identifier), `is_printable`, `aliases` (including the key itself). Input events typically bubble (guide).
- `Click`: sent when a widget is clicked. Bubbles. Subclass of `MouseEvent`; see that class for its properties.
- `Click.chain` counts clicks in quick succession: 1 single, 2 double, 3 triple. Clicks within 500ms form a chain; change this by setting `CLICK_CHAIN_TIME_THRESHOLD` on your `App` subclass.
- `Resize`: fields `size` (new size of the widget), `virtual_size` (scrollable size), `container_size` (size of the widget's container), `pixel_size` (terminal size in pixels, `None` if unknown).
- Related mouse events: `Enter`, `Leave`, `MouseDown`, `MouseUp`, `MouseMove`, `MouseScrollDown`, `MouseScrollUp`, `MouseScrollLeft`, `MouseScrollRight`.
- Handler names are `on_` plus the class name in snake_case (guide): `on_mount`, `on_resize`, `on_click`, `on_key`.

## Gotchas
- The Mount and Click pages list "Bubbles" and "Verbose" as bullet flags; the Resize and Key pages give no bubbling flag, so check the events guide before relying on bubbling for those.

## Verify
In a handler `def on_click(self, event): ...`, `event.chain` is 2 on a double click within the 500ms threshold.

## Checked

2026-11-07: every claim was read against the full text of these pages: events/mount, events/key, events/click, events/resize, guide/events. Removed the unfetchable events/index source; removed unsupported bubbling, Load/Ready descriptions, MouseEvent field list and Resize trigger wording; added guide/events as a source.

Method: documentation only; no commands were run.
