---
id: computing-software.software-engineering.textual.textual-data-binding
name: textual-data-binding
category: computing-software
field: software-engineering
product: textual
tags: [textual, data-binding, data-bind, reactive, compute, mutate-reactive, compound-widgets]
level: practitioner
status: docs-checked
description: "Bind parent reactive attributes to child widget reactives with data_bind in Textual, including keyword renaming, one-way flow and mutable reactives."
sources: [https://textual.textualize.io/guide/reactivity/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual data binding

Goal: keep child widget attributes in sync with a parent's reactive without per-child update loops.

## Method

1. Declare the reactive on the parent (App or widget), for example `time: reactive[datetime] = reactive(datetime.now)`, and a reactive of the same name on the child, for example `WorldClock.time`.
2. Call `data_bind` on the child widget with the parent's reactive (class attribute) as a positional argument:

```python
def compose(self) -> ComposeResult:
    yield WorldClock("Europe/London").data_bind(WorldClockApp.time)
    yield WorldClock("Europe/Paris").data_bind(WorldClockApp.time)
    yield WorldClock("Asia/Tokyo").data_bind(WorldClockApp.time)
```

   `data_bind` returns the widget, so you can yield its return value.
3. Changes to the parent's `time` now change `time` on every bound clock. A parent-side watcher that loops over the clocks becomes unnecessary.
4. If the child's attribute has a different name, use keyword arguments: `data_bind(clock_time=WorldClockApp.time)` binds the app's `time` to the child's `clock_time`.
5. Positional arguments require both reactives to share a name; keywords map child name to parent reactive.

## Mutable reactives

Textual detects assignment but not in-place changes such as appending to a list or dict. After mutating a reactive collection call `self.mutate_reactive(Class.names)` so the reactive superpowers (such as watchers and refresh) work. Without it, a display driven by a list reactive does not update when an item is appended.

## Gotchas

- Binding is one direction only: setting `time` on the app updates the clocks, but setting it on a clock does not update the app.
- The page's example needs the `pytz` library (`pip install pytz`) for time zones.

## Verify

In the page's world clock example with `data_bind(WorldClockApp.time)`, the three clocks update as the app's `time` changes without a watcher in the app.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/reactivity. Replaced the unsupported 'bindings run' wording with the page's 'reactive superpowers'.

Method: documentation only; no commands were run.
