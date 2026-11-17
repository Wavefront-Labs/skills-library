---
id: computing-software.software-engineering.textual.textual-css-variables-nesting
name: textual-css-variables-nesting
category: computing-software
field: software-engineering
product: textual
tags: [textual, css, css-variables, nesting, ampersand, tcss, nesting-selector]
level: practitioner
status: docs-checked
description: "Reduce repetition in Textual CSS with $variables and nested rule sets using the ampersand nesting selector."
sources: [https://textual.textualize.io/guide/CSS/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual CSS variables and nesting

Goal: keep stylesheets DRY and grouped.

## Method

### Variables

Variables are prefixed with `$`:

```css
$border: wide green;

#foo {
  border: $border;
}
```

`#foo` receives `border: wide green;`. Variables may refer to other variables: with `$success: lime;`, `$border: wide $success;` becomes `wide lime`. Variables can only appear in the values of a declaration, not inside a selector.

### Nesting (added in version 0.47.0)

A rule set inside another inherits the enclosing selector. Rules sharing a prefix such as `#questions` are good candidates:

- A nested `.button` rule inside `#questions { ... }` is equivalent to `#questions .button`.
- The ampersand `&` is the nesting selector: it combines directly with the outer selector, with no space. `&.affirmative` inside `.button` inside `#questions` is `#questions .button.affirmative`, matching a widget with both `button` and `affirmative` classes.
- Without `&`, `.affirmative` would mean `#questions .button .affirmative` (extra space), matching an `affirmative` widget inside a `button`.

Indentation is not required but makes the relationship clear.

## Why nest

- Avoids repeating the prefix (`#questions` typed once instead of four times).
- Groups related rules so they are easier to find.
- Makes the rules more specific, useful when rules apply to unintended widgets.

## Gotchas

- Forgetting `&` inserts a descendant combinator.
- Nested output matches the non-nested form exactly in the docs' example, so nesting is purely organisational apart from the specificity effect.

## Verify

Convert a flat sheet (`#questions .button.affirmative { ... }`) to nested form with `&.affirmative` and confirm the app renders identically.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/CSS. Nothing needed removing.

Method: documentation only; no commands were run.
