---
id: computing-software.software-engineering.textual.textual-header-footer-list-widgets
name: textual-header-footer-list-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-header-footer, header, footer, list-view, collapsible, toast, notify]
level: practitioner
status: docs-checked
description: "Use Textual Header, Footer, ListView with ListItem, Collapsible, and toast notifications via notify, including title sources, key display and toast CSS."
sources: [https://textual.textualize.io/widgets/header/, https://textual.textualize.io/widgets/footer/, https://textual.textualize.io/widgets/list_view/, https://textual.textualize.io/widgets/list_item/, https://textual.textualize.io/widgets/collapsible/, https://textual.textualize.io/widgets/toast/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Header, Footer, ListView, Collapsible and toasts

Goal: add app chrome, lists, expandable sections and notifications.

## Method
- `Header`: docks to the top. Text comes from `App.title` and `App.sub_title`. Reactive `tall` (the tall variant is 3 cells, the non-tall 1 cell; clicking the header toggles it; the page's table says default `True` but its API entry says `False`).
- `Footer` (0.63.0+): docks to the bottom and shows the bindings of the focused widget. Reactives `compact` (False) and `show_command_palette` (True). Hide a key with `Binding(..., show=False)`; change its footer text with the `key_display` argument of `Binding`.
- `ListView` (0.6.0+): vertical list of `ListItem`s that can be highlighted and selected, with keyboard navigation. Reactive `index` (highlighted index). Messages `ListView.Highlighted` and `ListView.Selected`. `ListItem` has reactive `highlighted` and posts no messages.
- `Collapsible` (0.37+): container with a title; click it, or focus it and press Enter, to toggle. Children via constructor or the preferred `with` form:

```python
with Collapsible(title="An interesting story.", collapsed=False):
    yield Label("Interesting but verbose story.")
```

  Reactives `collapsed` (default `True`) and `title` (default `"Toggle"`). Customise symbols with `collapsed_symbol=">>>"` and `expanded_symbol="v"`. Message `Collapsible.Toggled`.
- `Toast` (0.30.0+): not used directly; `App.notify(message, title=, severity=, timeout=)` shows one (Rich console markup is allowed in the message). Severity classes: `-information`, `-warning`, `-error`. Style with `Toast { padding: 3; }`, `Toast.-error { ... }`, the title via `Toast.-information .toast--title { text-style: italic; }`, and position via `ToastRack { align: right top; }`.

## Verify
Docs example: set `self.title` and `self.sub_title` on the App and the Header shows them; a Footer in an app with one binding lists that key automatically.

## Checked

2026-11-07: every claim was read against the full text of these pages: widgets/header, widgets/footer, widgets/list_view, widgets/list_item, widgets/collapsible, widgets/toast. Removed the focusable-container claims, the ListView index default (page tables disagree), the notify markup= parameter, and flagged the Header tall default conflict.

Method: documentation only; no commands were run.
