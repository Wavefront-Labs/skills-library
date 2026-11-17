---
id: computing-software.software-engineering.textual.textual-css-selectors
name: textual-css-selectors
category: computing-software
field: software-engineering
product: textual
tags: [textual, css, selectors, combinators, pseudo-classes, id-selector, class-selector, tcss]
level: practitioner
status: docs-checked
description: "Target Textual widgets with type, id, class, universal and pseudo-class selectors plus descendant and child combinators."
sources: [https://textual.textualize.io/guide/CSS/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual CSS selectors

Goal: choose the selector that matches exactly the widgets you intend.

## Method

- Type selector: matches the Python class name and also its base classes. `Static { ... }` styles an `Alert(Static)` too. If both `Alert` and `Static` set `border`, the most recently defined sub-class wins (`Alert` over `Static` over `Widget`).
- ID selector: `#next { outline: red; }` matches `Button(id="next")`. The id should be unique within its container and cannot change after construction.
- Class selector: `.success { background: green; color: white; }` matches `Button(classes="success")`. Several classes are space separated in Python (`classes="error disabled"`). Chain classes with no space to require all: `.error.disabled { ... }`.
- Universal selector: `* { outline: solid red; }` matches everything; `VerticalScroll * { background: red; }` matches all children of a `VerticalScroll`.
- Pseudo classes are set automatically by Textual: `Button:hover { background: green; }`. Others include `:blur`, `:dark`, `:disabled`, `:empty`, `:enabled`, `:even`, `:first-child`, `:first-of-type`, `:focus-within`, `:focus`, `:inline`, `:last-child`, `:last-of-type`, `:light`, `:odd`.
- Descendant combinator (space): `#dialog Button { text-style: bold; }` matches buttons anywhere below `#dialog`; `#dialog Horizontal Button` chains more.
- Child combinator (`>`): `#sidebar > Button { text-style: underline; }` matches only immediate children; whitespace around `>` is ignored.

Classes can change at runtime, which is the recommended way to change the display: `add_class()`, `remove_class()`, `toggle_class()`, `has_class()`, `set_class()` (sets or removes by boolean), and the frozen set `classes`.

## Gotchas

- Matching base classes differs from browser CSS.
- A widget's `id` is fixed after construction; use classes for anything dynamic.

## Verify

Add `Button:hover { background: green; }` and hover a button: only the hovered button turns green and it reverts when the cursor leaves.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/CSS. Nothing needed removing.

Method: documentation only; no commands were run.
