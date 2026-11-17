---
id: computing-software.software-engineering.textual.textual-css-specificity
name: textual-css-specificity
category: computing-software
field: software-engineering
product: textual
tags: [textual, css, specificity, important, initial, selectors, cascade]
level: practitioner
status: docs-checked
description: "Resolve conflicting Textual CSS rules using the specificity order of ids, classes and types, !important, and the initial value."
sources: [https://textual.textualize.io/guide/CSS/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual CSS specificity

Goal: predict which rule wins when several selectors set the same style on a widget.

## Method

Textual compares selectors in this order, moving to the next step only on a tie:

1. Most IDs wins: `#next` beats `.button`, and `#dialog #next` beats `#next`.
2. Most class names wins: `.button.success` beats `.success`. Pseudo classes count as class names, so `.button:hover` counts as 2.
3. Most types wins: `Container Button` beats `Button`.

### !important

Append `!important` to a single rule to make it win regardless of specificity:

```css
Button:hover {
  background: blue !important;
}
```

Use it sparingly, if at all; it makes the CSS harder to change later.

### initial

Every rule accepts the special value `initial`, which resets it to its default.

```css
Button {
  background: green;
}
.dialog Button {
  background: initial;
}
```

Buttons inside `.dialog` return to the default colour. `initial` resets to the value from any default CSS on the widget; used inside default CSS itself, the rule is treated as completely unstyled.

### Nesting raises specificity

Nested rule sets are more specific than the flat equivalent, which helps when rules hit widgets you did not intend.

## Gotchas

- Type selectors also match base classes, so a rule on `Static` can compete with one on a subclass; the most recently defined sub-class wins ties on the same style.
- Reach for a more specific selector before `!important`.

## Verify

Define `Button { background: green; }` and `.dialog Button { background: initial; }`, then place a button inside a widget with class `dialog`: it shows the default background while other buttons stay green.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/CSS. Nothing needed removing.

Method: documentation only; no commands were run.
