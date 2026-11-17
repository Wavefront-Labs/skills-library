---
id: computing-software.software-engineering.textual.textual-reactive-attributes
name: textual-reactive-attributes
category: computing-software
field: software-engineering
product: textual
tags: [textual, reactivity, reactive, var, smart-refresh, validate, layout, tui]
level: practitioner
status: docs-checked
description: "Declare Textual reactive and var attributes, control refresh and layout, validate assigned values, and set reactives without triggering watchers."
sources: [https://textual.textualize.io/guide/reactivity/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual reactive attributes

Goal: use `reactive` so widgets refresh automatically when data changes.

## Method

- Import `reactive` (and `var`) from `textual.reactive` and assign at class scope; no `__init__` needed. The first positional argument is the default.

```python
class Reactive(Widget):
    name = reactive("Paul")
    count = reactive(0)
    is_cool = reactive(True)
```

- Read and write like normal attributes (`self.count += 1`). The default may be a callable, for example `start_time = reactive(time)`, called to produce the default.
- Type hints are only needed when the type is wider than the default: `name: reactive[str | None] = reactive("Paul")`.
- Smart refresh: assigning a changed value makes Textual call the widget's `render()` again. Several changes yield a single refresh, and assigning an equal value does not refresh.
- `var(0)` creates a reactive that does not cause refresh or layout but keeps the other powers.
- Refresh updates content but not size. Pass `layout=True` (for example `reactive("", layout=True)`) when the change should alter the widget size.
- Validation: a method `validate_<name>(self, value)` is called on assignment and returns the value to store. Example: clamp a count to 0 to 10.

```python
def validate_count(self, count: int) -> int:
    if count < 0:
        count = 0
    elif count > 10:
        count = 10
    return count
```

- Order when several exist: compute method first, then validate, then watch.
- Set without side effects: `self.set_reactive(Greeter.greeting, greeting)` takes the reactive as a class attribute and the new value. Use it in constructors, where a watcher that queries the DOM before mount raises `NoMatches`.
- Mutable values: Textual detects reassignment but not mutation of lists or dicts. After mutating, call `self.mutate_reactive(Class.attr)` so refresh and watchers run.
- `recompose=True` removes and rebuilds children via `compose()` instead of refreshing (see textual-watch-and-compute).

## Gotchas

- Textual uses the descriptor protocol (same as `property`).
- Avoid slow or CPU-intensive work in compute methods: Textual calls them on an object whenever any reactive attribute changes.

## Checked
2026-11-07. Read in full: Reactivity guide. Confirmed: reactive/var imports and defaults, callable defaults, typing, smart refresh, layout=True, validate_<name>, compute then validate then watch order, set_reactive, mutate_reactive, recompose=True, descriptor protocol. Reworded: the performance gotcha now matches the page (compute methods). Removed: the Verify section.
Method: documentation only; no commands were run.
