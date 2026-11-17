---
id: computing-software.software-engineering.textual.textual-key-bindings
name: textual-key-bindings
category: computing-software
field: software-engineering
product: textual
tags: [textual, bindings, keys, binding-class, priority, footer, dynamic-actions, tui]
level: practitioner
status: docs-checked
description: "Declare Textual key bindings with BINDINGS, the Binding class, priority and show options, comma-separated keys, and conditional bindings through dynamic actions."
sources: [https://textual.textualize.io/guide/input/, https://textual.textualize.io/guide/actions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual key bindings

Goal: map keys to actions for an app or widget.

## Method
- Add a `BINDINGS` class variable: a list of tuples `(key, action, description)`. The action is an action string.
- Several keys for one action: comma-separate them, e.g. `("r,t", "add_bar('red')", "Add Red")`.
- For more options use a `Binding` instance instead of a tuple. Priority and footer visibility are set there; this is the App base-class binding:

```python
BINDINGS = [
    Binding("ctrl+q", "quit", "Quit", show=False, priority=True)
]
```

- Lookup order: the focused widget's `BINDINGS` first, then up the DOM to the App. A `priority=True` binding is checked before the focused widget's, so it cannot be disabled by binding the same key on a widget (good for app or screen hot-keys).
- `show=False` hides a binding from the Footer, which lists bindings and makes them clickable.
- Bindings cannot be modified at runtime. For conditional keys implement `check_action` returning `True` (show and run), `False` (hide, block) or `None` (dimmed, block). Call `refresh_bindings()` after state changes, or use a reactive declared with `bindings=True`.
- Key names are the `Key.key` strings: single characters for letters and digits, `shift+home`, `ctrl+p` and so on.

## Gotchas
- Not every key combination exists in terminals and some are intercepted by the OS; run `textual keys` to see what arrives.
- `key_<name>` methods exist but the docs say bindings and actions are preferable.

## Verify
Run `textual keys` from the command line and press the key; the `key` value shown is the string to use in `BINDINGS`.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/input, guide/actions. Nothing needed removing.

Method: documentation only; no commands were run.
