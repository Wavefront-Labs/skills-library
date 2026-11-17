---
id: computing-software.software-engineering.textual.textual-keyboard-focus-mouse
name: textual-keyboard-focus-mouse
category: computing-software
field: software-engineering
product: textual
tags: [textual, input-guide, keyboard, focus, mouse, key-events, mouse-capture, tui]
level: practitioner
status: docs-checked
description: "Handle Textual key events, focus and mouse input: Key attributes, key_ methods, can_focus, focus(), mouse events, capture_mouse and click events."
sources: [https://textual.textualize.io/guide/input/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual keyboard, focus and mouse input

Goal: respond to key and mouse input and manage focus.

## Method
- Key events: a `Key` event has `key` (single char for letters and digits, else an identifier such as `shift+home`, `ctrl+p`), `character` (`None` for e.g. F2), `name` (valid Python identifier: `ctrl+p` becomes `ctrl_p`, shift+p becomes `upper_p`), `is_printable`, and `aliases` (Tab gives `["tab", "ctrl+i"]`).
- Key methods: define `key_<name>` (the event `name`), e.g. `key_space`, to react to one key. Prefer bindings and actions in real apps.
- Focus: only one widget gets key events. Tab moves focus to the next widget, Shift+Tab back. `can_focus` says whether a widget can take focus (a disabled widget never can). Call a widget's `focus()` to focus it; by default the first focusable widget is focused on start. The `:focus` CSS pseudo-selector styles the focused widget. Widgets get a `Focus` event on gain and `Blur` on loss.
- Mouse coordinates `x`, `y` are in character cells, relative to the screen or to the widget ((0, 0) is top left).
- `MouseMove` goes to the widget under the cursor; call `capture_mouse()` to receive all mouse events regardless of position and `release_mouse()` to restore. Captured coordinates can be negative. `MouseCapture` and `MouseRelease` events announce the change.
- `Enter` and `Leave` fire when the cursor moves onto or off a widget and bubble; compare the event's `node` with `self` to find the original widget.
- Clicks: `MouseDown`, `MouseUp`, then `Click`. Handle `Click` rather than down/up. Scroll: `MouseScrollDown` and `MouseScrollUp` (plus `Left` and `Right` where the terminal supports it); scrollable containers handle them already.

## Verify
Run `textual keys` from the command line; it shows the key events your terminal sends.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/input. Nothing needed removing.

Method: documentation only; no commands were run.
