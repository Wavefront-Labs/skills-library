---
id: computing-software.software-engineering.textual.textual-log-widgets
name: textual-log-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-logs, log, rich-log, streaming-output, auto-scroll, tui]
level: practitioner
status: docs-checked
description: "Stream output into Textual with Log (plain text lines) or RichLog (Rich renderables): write methods, max_lines, auto_scroll, markup, wrap and highlight options."
sources: [https://textual.textualize.io/widgets/log/, https://textual.textualize.io/widgets/rich_log/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Log and RichLog

Goal: append output in realtime to a scrollable widget.

## Method
**Log** (added in 0.32.0): plain text lines.
- `Log.write_line("text")` writes one line, `Log.write_lines(iterable)` several, `Log.write(data)` writes a string, `Log.clear()` empties it. Each write takes `scroll_end=` (`None` means use `auto_scroll`) and returns the Log.
- Reactives: `max_lines` (`None` = no maximum) and `auto_scroll` (scroll to end on new lines; the docs table lists default `False`, while the constructor signature has `auto_scroll=True`, so set it explicitly if it matters).
- Constructor: `Log(highlight=False, max_lines=None, auto_scroll=True, name=, id=, classes=, disabled=)`. Read-only properties: `lines`, `line_count`.

**RichLog**: accepts strings or any Rich renderable.
- `RichLog.write(content, width=None, expand=False, shrink=True, scroll_end=None, animate=False)`; `RichLog.clear()`.
- Reactives: `highlight` (False), `markup` (False, applies Rich console markup), `max_lines` (None), `min_width` (78, minimum width of renderables), `wrap` (False, word wrapping).
- Writes made in `compose` or `on_mount` are not rendered immediately; rendering waits until the widget size is known.

Both widgets post no messages and have no bindings or component classes. Use Log for simple text and RichLog for tables, syntax and other renderables.

```python
log = self.query_one(Log)
log.write_line("started")
```

## Gotchas
- Set `max_lines` for long-running streams to keep the buffer bounded.
- RichLog does not apply markup unless `markup=True`.

## Checked
2026-11-07. Read in full: the Log and RichLog widget pages. Confirmed: 0.32.0, write_line/write_lines/write/clear, scroll_end semantics, reactive names and defaults, constructor parameters, deferred rendering note, no messages/bindings/component classes. Removed: focusability claims (the page only prints a generic bullet) and the invented Verify step about key output.
Method: documentation only; no commands were run.
