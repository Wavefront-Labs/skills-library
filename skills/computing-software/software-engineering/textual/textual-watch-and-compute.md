---
id: computing-software.software-engineering.textual.textual-watch-and-compute
name: textual-watch-and-compute
category: computing-software
field: software-engineering
product: textual
tags: [textual, reactivity, watch, compute, recompose, data-binding, always-update]
level: practitioner
status: docs-checked
description: "React to Textual reactive changes with watch_ methods and dynamic watch, derive values with compute_ methods, and rebuild children with recompose=True."
sources: [https://textual.textualize.io/guide/reactivity/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual watch methods, compute methods and recompose

Goal: respond to reactive changes and derive reactive values.

## Method

Watch methods:
- Name a method `watch_<attribute>`; Textual calls it when the reactive changes. One positional parameter receives the new value; two receive old then new.
- It is called only if the value actually changed. Pass `always_update=True` to `reactive` to call it even for an equal value.
- Add watchers in code with `self.watch(widget, "attr", callback)`, useful for reactives on widgets whose code you cannot edit. The page keeps a progress bar in sync with `Counter.counter` this way, using a custom callback.

Compute methods:
- Name a method `compute_<attribute>`; it calculates the reactive's value, is cached, and is re-run when any other reactive on that object changes.
- Example: `red`, `green`, `blue` reactives plus `color = reactive(Color.parse("transparent"))`:

```python
def compute_color(self) -> Color:
    return Color(self.red, self.green, self.blue).clamped

def watch_color(self, color: Color) -> None:
    self.query_one("#color").styles.background = color
```

- `watch_color` fires when the result of `compute_color` changes. Order is compute, then validate, then watch.
- Keep compute methods fast: they run whenever any reactive on the object changes.

Recompose:
- `reactive("name", recompose=True)` removes all child widgets and calls `compose()` again when the value changes, in a single update. For a clock this removes duplicated formatting between `compose()` and `watch_time()`.
- Do not store references to children; use queries when needed.
- Child state is reset, so avoid it for stateful widgets (DataTable, Input, TextArea).
- It is slightly less efficient than a refresh; avoid it for rapid updates or many children.

## Gotchas

- A watcher that queries the DOM breaks if the reactive is assigned before mount; use `set_reactive` in constructors.

## Checked
2026-11-07. Read in full: Reactivity guide (watch methods, dynamic watch, recompose, compute methods, set_reactive). Confirmed: watch_ one or two arguments, always_update=True, self.watch(widget, attr, callback), compute_ caching, compute then validate then watch order, recompose=True behaviour and its caveats. Removed: the DOMNode.watch class name (not on the page) and the Verify section.
Method: documentation only; no commands were run.
