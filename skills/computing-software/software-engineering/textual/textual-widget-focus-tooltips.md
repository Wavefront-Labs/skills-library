---
id: computing-software.software-engineering.textual.textual-widget-focus-tooltips
name: textual-widget-focus-tooltips
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets, focus, can-focus, tooltip, loading, content-size, bindings]
level: practitioner
status: docs-checked
description: "Make Textual widgets focusable with can_focus and BINDINGS, add tooltips, show the loading indicator, and override content width and height."
sources: [https://textual.textualize.io/guide/widgets/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual widget focus, tooltips, loading and content size

Goal: handle keyboard focus and common widget-level features.

## Method

**Focus and keybindings**
1. A widget handles key presses if it or a descendant has focus. Widgets are not focusable by default; set `can_focus=True` in the subclass definition. Focus by click, or Tab and Shift+Tab.
2. Style the focused state with CSS rules that apply only on focus.
3. Add a `BINDINGS` class variable linking keys (for example up, `k`, down) to an action such as `change_count`, passing an argument if needed. The final element is a user-facing label shown in the footer while the binding is active. The handler method needs the `action_` prefix (`action_change_count`).

**Tooltips**
1. Assign to the widget's `tooltip` property: text or any Rich renderable, shown on hover.
2. Do not rely on tooltips for essential information; keyboard-only users may never see them.
3. Restyle with a CSS rule targeting `Tooltip`.

**Loading indicator**
Set the widget's `loading` reactive to `True` to temporarily replace it with a `LoadingIndicator`; set it back to `False` when the data has arrived. The guide does this around a simulated fetch run with the `@work` decorator.

**Content size**
With `width` or `height` set to `auto`, Textual detects the content area from Rich renderables. Override by implementing `get_content_width()` or `get_content_height()`. When a Rich `Table` should fill the width you return, give it `expand=True`.

```python
button.tooltip = "Click to see a message"
widget.loading = True
```

## Gotchas

- A widget handles key presses only if it or a descendant has focus, and widgets are not focusable by default; set `can_focus=True` on a custom widget that needs its own bindings.
- Add the `action_` prefix to the handler method name; the guide stresses it.

## Checked
2026-11-07. Read in full: Widgets guide (focus and keybindings, tooltips, loading indicator, content size sections). Confirmed: can_focus=True in the class definition, Tab/Shift+Tab, focus-only CSS, BINDINGS with argument and footer label, action_ prefix, tooltip property and Tooltip CSS, loading reactive, get_content_width/height and expand=True. Reworded: the two gotchas to what the page states (descendant focus; prefix emphasised, no stated failure mode). Removed: the Verify section.
Method: documentation only; no commands were run.
