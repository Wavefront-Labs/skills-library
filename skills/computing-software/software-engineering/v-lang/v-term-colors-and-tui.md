---
id: computing-software.software-engineering.v-lang.v-term-colors-and-tui
name: v-term-colors-and-tui
category: computing-software
field: software-engineering
product: v-lang
tags: [v-term-colors-and-tui, terminal-gui-modules, term, term.ui, tui, ansi colors, terminal size, cursor, red, bold, terminal ui, v-lang]
level: practitioner
status: docs-checked
description: "Colour output with term, detect terminal size, and build text user interfaces with the term.ui event loop."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# term colors and term.ui terminal apps

Goal: pleasant console output and TUIs.

- Colour: `import term; println(term.green('ok')); term.bold('x'); term.bg_blue('y')`; `term.strip_ansi(s)`; check `term.can_show_color_on_stdout()` (true when colours are allowed on stdout).
- Size/cursor: `w, h := term.get_terminal_size()`, `term.clear()`, `term.hide_cursor()`, `term.set_cursor_position(x: 1, y: 1)`.
- TUI: `import term.ui as tui`; create `ctx := tui.init(user_data: app, event_fn: on_event, frame_fn: frame, hide_cursor: true)` (returns `&Context`, no `!`) then `ctx.run()!`; draw with `ctx.draw_text(x, y, s)`, `ctx.draw_rect`, `ctx.flush()`; handle `tui.Event` kinds (`typ` is an `EventType`: key_down, key_up, mouse_down, mouse_up, mouse_move, mouse_drag, mouse_scroll, resized).

Gotchas:
- Test `term.can_show_color_on_stdout()` before colouring; avoid colours in pipes.
- `tui.Config` has `cleanup_fn` and `fail_fn` callbacks and a `reset` list of signals; put teardown in `cleanup_fn` rather than managing raw mode yourself.

Verify: run a small TUI that quits on `q`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: term.green/bold/bg_blue/strip_ansi/can_show_color_on_stdout/get_terminal_size/clear/hide_cursor/set_cursor_position(Coord x, y) (vlib/term), term.ui init returning &Context, Context.run/draw_text/draw_rect/flush, Config fields user_data, event_fn, frame_fn, cleanup_fn, fail_fn, hide_cursor, reset and the EventType enum (vlib/term/ui/input.v, input_nix.c.v, ui.c.v).
Removed or corrected: `tui.init(...)!` (init does not return a result), the `NO_COLOR` claim (not in the module), and the unverified `examples/term.ui` pointer.
Method: documentation only; no commands were run.
