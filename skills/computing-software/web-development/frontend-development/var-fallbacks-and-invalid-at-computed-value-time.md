---
id: computing-software.web-development.frontend-development.var-fallbacks-and-invalid-at-computed-value-time
name: var-fallbacks-and-invalid-at-computed-value-time
category: computing-software
field: web-development
product: frontend-development
tags: [css-custom-properties, var-fallback, invalid-at-computed-value-time, design-tokens, css]
level: practitioner
status: docs-checked
description: "Writing robust var() fallbacks and understanding invalid-at-computed-value-time: why bad values reset to unset rather than the earlier declaration, and safe tokens."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/var
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Syntax/Error_handling
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@property
  - https://www.w3.org/TR/css-variables-1/#invalid-at-computed-value-time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# var() fallbacks and invalid-at-computed-value-time

## 1. Fallbacks
```css
.btn { background: var(--btn-bg, var(--color-primary, #0b5fff)); }
.icon { margin: var(--icon-gap,); }          /* empty fallback = valid empty value */
```
- The fallback is used only when the custom property has the guaranteed-invalid value: not declared (and not registered with an `initial-value`), set to `initial`, or invalid at computed-value time through a cycle on an unregistered property. A defined value of the wrong type does not trigger it.
- Everything after the first comma is the fallback: `var(--font, Inter, sans-serif)` falls back to `Inter, sans-serif`.

## 2. Invalid at computed-value time (IACVT)
```css
.box { color: red; color: var(--size); }    /* --size: 20px */
```
The declaration parses fine (any `var()` is accepted at parse time), so the cascade picks it over `color: red`. At computed-value time `20px` isn't a colour - the property becomes **`unset`** (inherited colour or initial), not red. The earlier declaration is not a fallback.
Consequences:
- The classic "fallback declaration above" pattern doesn't protect against bad variable values, only against browsers without custom property support.
- Debugging: DevTools shows the declaration as applied but the computed value is the inherited/initial one.

## 3. Defences
- Register important tokens with `@property`, a `syntax` and an `initial-value`: MDN recommends this to control how custom properties fall back.
- Use `@supports` for feature fallbacks instead of declaration stacking when values come from variables.
- Keep tokens typed by naming (`--space-*` lengths, `--color-*` colours).

## 4. Other gotchas
- Custom properties are case-sensitive (`--Main` != `--main`).
- `var()` works only inside property values, not in property names or selectors; for units write `calc(var(--n) * 1px)`, not `var(--n)px`.
- Custom properties inherit by default; set them on the component root to scope.
- Cyclic references (`--a: var(--b); --b: var(--a)`) make both IACVT.
- Setting an unregistered custom property to `initial` makes it guaranteed-invalid, so the fallback applies.

## Verify
Set the token to a wrong-type value in DevTools and confirm the registered initial value applies; computed-styles pane shows the expected resolved values.

## Checked

Checked 2026-10-26 against current documentation. MDN `var()` (when the fallback applies, comma handling, empty fallback, registered properties), the error-handling guide (invalid `var()` substitution yields the inherited or initial value) and custom-property pages (case sensitivity, inheritance). Removed unconfirmed `--x: ;` and Stylelint rule claims.

Method: documentation only; no commands were run.
