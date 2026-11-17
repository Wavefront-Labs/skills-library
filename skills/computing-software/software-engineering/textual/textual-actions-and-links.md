---
id: computing-software.software-engineering.textual.textual-actions-and-links
name: textual-actions-and-links
category: computing-software
field: software-engineering
product: textual
tags: [textual, actions, action-methods, links, click-markup, namespaces, check-action, tui]
level: practitioner
status: docs-checked
description: "Write Textual action_ methods, call them via action strings from links and key bindings, use app, screen and focused namespaces, and gate them with check_action."
sources: [https://textual.textualize.io/guide/actions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual actions and links

Goal: expose app behaviour as allow-listed actions callable from links and keys.

## Method
- An action is a method prefixed `action_` on an App, Screen or Widget (may be `async`). Example: `action_set_background(self, color)`.
- An action string is parsed, not eval'd: `"bell"` calls `action_bell()`; `"set_background('red')"` calls `action_set_background('red')`. Parameters must be Python literals (numbers, strings, dicts, lists); variables are invalid.
- Run a string yourself with `await self.run_action("set_background('red')")` (a coroutine, so the caller must be `async`).
- Links: embed in markup with the `@click` tag; clicking runs the action.
- Keys: bind in `BINDINGS`, for example `("r", "set_background('red')", "Red")`.
- Namespaces: actions are looked up on the class where the link or binding lives (a custom widget can have its own). Prefix with `app.`, `screen.` or `focused.` to target the App, the screen, or the focused widget, e.g. `app.set_background('red')`.
- Dynamic actions (0.61.0+): implement `check_action(self, action, parameters)` and return `True` (show key, run), `False` (hide key, do not run) or `None` (show dimmed, do not run). Call `refresh_bindings()` to refresh the footer, or declare the reactive with `bindings=True` so it refreshes when the value changes.
- Built-in app actions: add_class, back, bell, focus_next, focus_previous, focus, pop_screen, push_screen, quit, remove_class, screenshot, simulate_key, suspend_process, switch_screen, toggle_class, toggle_dark.

## Verify
In the guide's examples, pressing the bound `r`, `g` or `b` key (or clicking a link) changes the background; with `check_action` the page keys disappear from the footer when they would have no effect.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/actions. Nothing needed removing.

Method: documentation only; no commands were run.
