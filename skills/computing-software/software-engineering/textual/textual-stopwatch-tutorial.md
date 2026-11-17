---
id: computing-software.software-engineering.textual.textual-stopwatch-tutorial
name: textual-stopwatch-tutorial
category: computing-software
field: software-engineering
product: textual
tags: [textual, tutorial, stopwatch, widgets, css, reactive, mount, tui]
level: intro
status: docs-checked
description: "Build the Textual stopwatch app step by step: App with bindings, custom widgets, a tcss file, CSS classes, reactive time and mounting widgets."
sources: [https://textual.textualize.io/tutorial/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual stopwatch tutorial

Goal: build a multi-stopwatch app with Start, Stop and Reset buttons and add/remove of stopwatches.

## Method

1. App skeleton: subclass `App`; `BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]` (key, action name, description); `compose()` yields `Header()` and `Footer()`; an `action_toggle_dark` method (actions are methods named `action_` plus the action name); finish with `app = StopwatchApp()` and `app.run()` in a `__name__ == "__main__"` block.
2. Custom widgets: a `TimeDisplay(Digits)` and a `Stopwatch(HorizontalGroup)` whose `compose()` yields `Button("Start", id="start", variant="success")`, a Stop button (variant `error`), `Button("Reset", id="reset")` and a `TimeDisplay`. `StopwatchApp.compose()` yields `VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch())`; `VerticalScroll` also supplies the scroll key bindings.
3. Style with CSS: set `CSS_PATH = "stopwatch.tcss"` on the app. Rules like `Stopwatch { background: $boost; height: 5; margin: 1; min-width: 50; padding: 1; }`, `Button { width: 16; }`, and id rules (`#start { dock: left; }`, `#stop { dock: left; display: none; }`, `#reset { dock: right; }`). `$name` picks a color from the builtin theme.
4. Dynamic state with a CSS class: rules prefixed `.started` (for example `.started #start { display: none }`) apply only inside a widget with the `started` class. Toggle with `add_class("started")` / `remove_class("started")` in `on_button_pressed(self, event: Button.Pressed)`.
5. Reactives in `TimeDisplay`: `start_time = reactive(monotonic)`, `time = reactive(0.0)`, `total = reactive(0.0)`. In `on_mount`, `self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)`; `watch_time` formats the value and calls `self.update(...)`. Add `start()` (resume the timer), `stop()` (pause) and `reset()` methods.
6. Wire buttons: in the handler read `event.button.id`, get `self.query_one(TimeDisplay)`, call the matching method, and add/remove the `started` class.
7. Add and remove at runtime: give the VerticalScroll `id="timers"`; `action_add_stopwatch` does `self.query_one("#timers").mount(new_stopwatch)` then `new_stopwatch.scroll_visible()`; `action_remove_stopwatch` does `timers = self.query("Stopwatch")` and `if timers: timers.last().remove()`. Bind `a` and `r` to them.

## Gotchas

- `monotonic` (from `time`) is used because it does not go backwards if the system clock changes.
- Both `Button` ids must match the CSS ids exactly.

## Checked
2026-11-07. Read in full: the Textual tutorial page. Confirmed: BINDINGS tuple form and action_ naming, Header/Footer, TimeDisplay(Digits) and Stopwatch(HorizontalGroup), button variants, VerticalScroll scroll bindings, CSS_PATH and the stopwatch tcss rules, $ theme colours, .started class rules with add_class/remove_class, reactive monotonic/time/total, set_interval(1 / 60, ..., pause=True), watch_time, start/stop/reset, mount/scroll_visible/query/last/remove and the a/r bindings. Removed: the Verify section.
Method: documentation only; no commands were run.
