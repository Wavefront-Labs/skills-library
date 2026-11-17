---
id: computing-software.software-engineering.v-lang.v-ui-toolkit
name: v-ui-toolkit
category: computing-software
field: software-engineering
product: v-lang
tags: [v-ui-toolkit, terminal-gui-modules, ui, vlang ui, gui, widgets, desktop app, window, button, textbox, layout, v-lang]
level: advanced
status: draft
description: "Create desktop apps with the vlang/ui toolkit using window, widgets, layouts, event handlers and state, and know its maturity."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ui: native widget toolkit

Goal: build a desktop GUI using V's `ui` module (install separately: `v install ui`).

- Structure: an `App` struct holding state and widget refs; build with `ui.window(...)` containing `ui.column(...)`/`ui.row(...)`, `ui.button(text: 'Go', on_click: app.on_click)`, `ui.textbox(...)`, `ui.label(...)`, `ui.checkbox`, `ui.listbox`.
- Run with `ui.run(window)`; update widgets by mutating state and calling the widget setters.
- Layout: `heights`/`widths` arrays, `margin`, `spacing`, `alignment`.
- It is rendered via gg (own drawing, not native widgets), with themes and desktop dialogs.
- Examples: the `ui` repo `examples/` (todo app, calculator).

Gotchas:
- Status: alpha/beta; widget set and APIs shift between releases (confirm before committing to it).
- Keep logic in methods with `mut` receivers; ensure state structs are heap allocated (`&App{}`).

Verify: run the counter example and click the button.
