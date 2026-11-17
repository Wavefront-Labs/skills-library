---
id: computing-software.software-engineering.textual.textual-display-widgets
name: textual-display-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-display, static, label, digits, pretty, rule, placeholder, link]
level: practitioner
status: docs-checked
description: "Pick and use Textual display widgets: Static, Label, Digits, Pretty, Rule, Placeholder and Link, with their constructors, reactives and update calls."
sources: [https://textual.textualize.io/widgets/static/, https://textual.textualize.io/widgets/label/, https://textual.textualize.io/widgets/digits/, https://textual.textualize.io/widgets/pretty/, https://textual.textualize.io/widgets/rule/, https://textual.textualize.io/widgets/placeholder/, https://textual.textualize.io/widgets/link/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual display widgets

Goal: choose the simplest widget that shows non-interactive content. None of these post messages.

## Method
- `Static`: shows static content, including Rich renderables, and is the base for other widgets. `yield Static("Hello, world!")`. No reactives.
- `Label` (0.5.0+): static text, may contain richer Rich renderables; the docs suggest it for plain text display.
- `Digits` (0.33.0+): tall multi-line characters. Supports 0-9, A-F, `+`, `-`, `^`, `:` and the multiplication sign; other characters use a normal font. Set text in the constructor or call `update()` after mounting, e.g. `self.query_one(Digits).update(f"{clock:%T}")` for a clock. Respects the `text-align` rule.
- `Pretty`: pretty-formats any Python object: `yield Pretty(DATA)`.
- `Rule`: separator like HTML `<hr>`. Reactives `orientation` (`"horizontal"` default, or vertical) and `line_style` (`"solid"` default; examples use `heavy`, `thick`, `dashed`): `Rule(line_style="heavy")`.
- `Placeholder` (0.6.0+): stand-in while designing layout; `Placeholder("custom label", id="p1")`. Reactive `variant`: `default`, `size`, `text`. Clicking cycles through the variants.
- `Link` (0.84.0+): text that opens a URL in a web browser when clicked; Enter also opens it. Reactives `text` and `url` (both default `""`). Constructor takes the text then the URL: `Link("Go to textualize.io", url="https://textualize.io", tooltip="Click me")`.

## Gotchas
- Call `Static.update` or `Digits.update` to change content after mount; the clock example finds the widget with `query_one`.

## Verify
Docs example: `Digits("", id="clock")` updated with `update(f"{clock:%T}")` shows the current time in tall digits.

## Checked

2026-11-07: every claim was read against the full text of these pages: widgets/static, widgets/label, widgets/digits, widgets/pretty, widgets/rule, widgets/placeholder, widgets/link. Removed 'only Link is focusable' (every widget page lists the same Focusable flag) and reworded the update/query_one gotcha.

Method: documentation only; no commands were run.
