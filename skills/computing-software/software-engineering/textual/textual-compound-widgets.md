---
id: computing-software.software-engineering.textual.textual-compound-widgets
name: textual-compound-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, compound, compose, widgets, messages, post-message, data-flow, reusable]
level: practitioner
status: docs-checked
description: "Build Textual compound widgets from child widgets and keep them reusable with attributes down and messages up data flow."
sources: [https://textual.textualize.io/guide/widgets/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual compound widgets and coordination

Goal: group built-in widgets into reusable units that talk to each other without becoming dependent.

## Method

1. A compound widget is a widget built from other widgets. Instead of `render` or `render_line`, write a `compose()` method that yields child widgets. It is used like any other widget; example: `InputWithLabel` bundles an `Input` and a `Label`.
2. Split a UI into compound widgets by the rule of thumb: a widget handles one piece of data. The guide's byte editor uses `BitSwitch` (a `Label` plus a `Switch`), `ByteInput` (8 `BitSwitch` widgets), and `ByteEditor` (a `ByteInput` plus an `Input` for the decimal value).
3. Default CSS on each compound widget handles its own arrangement (horizontal layout, vertical alignment, `focus-within` accent border, stacking).
4. Follow "attributes down, messages up" (uni-directional data flow): a widget may set attributes or call methods on its children, but should only send messages to its parent or ancestors.
5. Attributes down: get the child and use it as a Python object:

```python
def action_set_true(self):
    self.query_one(Switch).value = 1
```

6. Messages up: define a custom message on the child and post it:

```python
def on_click(self):
    self.post_message(MyWidget.Change(active=True))
```

The parent handles the message. In the guide, `BitSwitch` handles the builtin `Switch.Changed` message, stores the bit, stops that event so it does not reach the parent, and posts its own `BitSwitch.BitChanged`; `ByteEditor` handles it and computes the decimal value.
7. Siblings cannot modify each other directly: send a message to the parent, which makes the change.
8. Editing the decimal `Input` sets a reactive `value` on `ByteEditor`; `watch_value` then sets each child switch's attributes directly. To avoid a feedback loop the guide prevents the `BitChanged` message from being sent while updating switches.

## Gotchas

- Reaching into siblings or parents couples widgets and makes them non-reusable.
- Clamp values to the valid range (the byte example keeps it within a byte).

## Verify

Compose `ByteEditor` and toggle a switch: the decimal `Input` updates; type a number: the switches update.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/widgets. Nothing needed removing.

Method: documentation only; no commands were run.
