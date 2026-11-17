---
id: computing-software.software-engineering.textual.textual-css-stylesheets
name: textual-css-stylesheets
category: computing-software
field: software-engineering
product: textual
tags: [textual, css, stylesheets, tcss, css-path, live-editing, dom, python]
level: practitioner
status: docs-checked
description: "Attach Textual CSS (.tcss) files to an App with CSS_PATH, read a rule set, and live-edit styles with textual run --dev."
sources: [https://textual.textualize.io/guide/CSS/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual CSS stylesheets

Goal: style widgets from a stylesheet instead of Python attributes, and iterate on it live.

## Method

1. A rule set is a selector followed by braces holding rules. Each rule is `name: value;` and several can share a line if separated by semicolons.

```css
Header {
  dock: top;
  height: 3;
  content-align: center middle;
  background: blue;
  color: white;
}
```

2. Put the rules in a file. Textual CSS files conventionally use the `.tcss` extension to tell them apart from browser CSS (`.css`).
3. Point the app at the file with the `CSS_PATH` class variable, set to a relative path.
4. `CSS_PATH` can also be a list of paths; Textual combines the rules from all of them.
5. Give widgets `id` and `classes` keyword arguments in their constructors so the CSS can target them.
6. Comments go between `/*` and `*/` and are ignored, which is handy for temporarily disabling a selector.
7. Live edit: run the app with the dev flag and CSS file changes are applied to the terminal instantly.

```bash
textual run my_app.py --dev
```

## Why CSS rather than Python styles

- It separates how the app looks from how it works, avoiding style code mixed into logic.
- Built-in and third-party widgets can be customised as easily as your own.
- It enables live editing.

## Gotchas

- Widgets are arranged as a tree (the DOM). The App owns an implicit `Screen`, and widgets such as `Header`, `Footer` or a `Container` are its children; a selector can address any of them.
- Not every widget accepts positional child widgets in its constructor (a `Button` does not), while a `Container` does.
- `initial` resets a value to the widget's default CSS value; inside default CSS it treats the rule as completely unstyled.

## Verify

Run `textual run my_app.py --dev`, edit and save the `.tcss` file, and confirm the running app restyles without a restart.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/CSS. Nothing needed removing.

Method: documentation only; no commands were run.
