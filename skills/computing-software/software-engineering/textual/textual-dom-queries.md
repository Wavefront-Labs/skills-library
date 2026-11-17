---
id: computing-software.software-engineering.textual.textual-dom-queries
name: textual-dom-queries
category: computing-software
field: software-engineering
product: textual
tags: [textual, queries, query-one, query, dom, selectors, filter, exclude]
level: practitioner
status: docs-checked
description: "Find and update Textual widgets with query_one and query, using CSS selectors or types, first and last, filter and exclude, and loop-free bulk methods."
sources: [https://textual.textualize.io/guide/queries/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual DOM queries

Goal: locate widgets in Python with CSS selectors and update them in bulk.

## Method

`query_one` returns a single widget:

```python
send_button = self.query_one("#send")
send_button = self.query_one("#send", Button)   # type-checked
my_button = self.query_one(Button)              # by type
```

- No match raises `NoMatches`. If the optional second argument is given and the widget is a different type, `WrongType` is raised. The type argument also tells MyPy the return type.
- It searches below the node it is called on. For the whole DOM call it on the App or Screen, such as `self.screen.query_one("#send-email")`.

`query` returns a list-like `DOMQuery`; it is recursive (`self.query()` with no argument returns all widgets below):

```python
for button in self.query("Dialog Button.disabled"):
    print(button)
```

- Any CSS selector works. Everything works on both App and Widget subclasses.
- `.results(Button)` iterates only objects of that type (and types them for MyPy): `self.query(".disabled").results(Button)`.
- A DOMQuery supports list operations (`query[0]`, `len(query)`, `reverse(query)`).
- `first()` and `last()` return the first or last match; `NoMatches` if empty. Pass `expect_type`, e.g. `self.query(".disabled").last(Button)`; a different type raises `WrongType`.
- `filter(".disabled")` returns a new query of matches that also fit the selector; `exclude(".disabled")` removes matches that fit it.

Loop-free methods act on every matched widget, e.g. `self.query("Button").add_class("disabled")`, equivalent to looping over the widgets. The list on the page: `add_class`, `blur`, `focus` (first matching widget), `refresh`, `remove_class`, `remove`, `set_class`, `set` (common attributes), `toggle_class`.

## Gotchas

- Call `query_one` on a widget and you only find its descendants.
- Selectors are the same ones used in CSS, so `Dialog Button.disabled` means Buttons with class `disabled` inside a Dialog.

## Verify

`self.query("Button").add_class("disabled")` gives the same result as looping over `self.query("Button")` and calling `add_class` on each widget.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/queries. Nothing needed removing.

Method: documentation only; no commands were run.
