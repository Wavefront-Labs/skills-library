---
id: computing-software.software-engineering.textual.textual-custom-messages-bubbling
name: textual-custom-messages-bubbling
category: computing-software
field: software-engineering
product: textual
tags: [textual, custom-messages, message-handlers, bubbling, post-message, prevent, tui]
level: practitioner
status: docs-checked
description: "Define custom Textual messages inside a widget, post them, and control bubbling with stop and prevent so parents can react to child state changes."
sources: [https://textual.textualize.io/guide/events/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual custom messages and bubbling

Goal: let a custom widget tell its parent about a change, and control how messages travel.

## Method
- Subclass `Message` and define it inside the widget class. The constructor stores the data handlers need (the guide's example stores a `Color`).
- Nesting is recommended: importing the widget gives access to `ColorButton.Selected`, and the namespace makes the handler name `on_color_button_selected`, reducing clashes.
- Send with `post_message()`, which puts the message on the widget's queue and runs handlers. Widgets often post to themselves and let it bubble, so a subclass can add its own handler.
- Handler example from the guide:

```python
def on_color_button_selected(self, message: ColorButton.Selected) -> None:
    self.screen.styles.animate("background", message.color, duration=0.5)
```

- Bubbling: a message with `bubble` set to `True` is sent to the parent after processing, up to the App (the DOM root, nowhere further). Input events typically bubble.
- Stop bubbling by calling `stop()` on the event or message, for example when a widget has handled it authoritatively (an input widget stops the key event so it does not also invoke a key binding).
- Add a `control` property to a custom message if you want handlers to filter it with `@on(Message, "selector")`.
- Temporarily suppress a message type with `with self.prevent(Input.Changed): ...`, useful when you update a child and do not want its notification.

## Gotchas
- `prevent_default()` stops base-class handlers; `stop()` stops bubbling to parents. They are different.
- Handlers run one at a time per widget, so keep them fast.

## Verify
For a nested class `ColorButton.Selected`, the convention-derived handler name is `on_color_button_selected`; printing `ColorButton.Selected.handler_name` shows it.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/events. Nothing needed removing.

Method: documentation only; no commands were run.
