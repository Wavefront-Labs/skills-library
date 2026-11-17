---
id: computing-software.software-engineering.textual.textual-events-and-messages
name: textual-events-and-messages
category: computing-software
field: software-engineering
product: textual
tags: [textual, events, messages, message-queue, on-decorator, handlers, tui]
level: practitioner
status: docs-checked
description: "Handle Textual events and messages: how the message queue works, handler naming, the on decorator with selectors, handler arguments, and async handlers."
sources: [https://textual.textualize.io/guide/events/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual events and messages

Goal: write correct message handlers and understand how events reach them.

## Method
- Events are messages sent by Textual; custom messages work the same way. Every App and Widget has a message queue, drained by an asyncio Task started on mount. Each message is dispatched to its handler one at a time; the widget is idle when the queue is empty.
- Handler name: `on_` + namespace (the parent widget class, CamelCase to snake_case) + `_` + message class in snake_case. `Input.Changed` is handled by `on_input_changed`.
- Base-class handlers are called automatically (for a `Key` event on a `Paddle(Static)`: `Paddle.on_key`, then `Static.on_key`, then `Widget.on_key`). Call `prevent_default()` on the event to stop that.
- A handler may take the message as one positional argument, or omit it if unused.
- The `on` decorator turns any method into a handler and can filter with a CSS selector:

```python
@on(Button.Pressed, "#bell")
def play_bell(self): ...

@on(TabbedContent.TabActivated, pane="#home")
def home_tab(self) -> None: ...
```

- The decorator selector needs a `control` property on the message (built-in widget messages have one). Keyword selectors only match attributes listed in `Message.ALLOW_SELECTOR_MATCH`.
- If several decorated handlers match, all run in definition order; the naming-convention handler runs after them.
- Handlers may be `async def`; Textual awaits them.
- To silence messages while changing a child, wrap the change in `with self.prevent(Input.Changed):` (`prevent` is a context manager).

## Gotchas
- A widget cannot pick up its next message until the handler returns. Slow work (for example network access) blocks it; launch it with `asyncio.create_task` so the UI stays responsive.
- `prevent_default()` can disable core behaviour of base classes; use sparingly.

## Verify
In a Python shell, `from textual.widgets import Input; Input.Changed.handler_name` returns `'on_input_changed'`.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/events. Nothing needed removing.

Method: documentation only; no commands were run.
