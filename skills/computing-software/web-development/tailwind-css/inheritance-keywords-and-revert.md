---
id: computing-software.web-development.tailwind-css.inheritance-keywords-and-revert
name: inheritance-keywords-and-revert
category: computing-software
field: web-development
product: tailwind-css
tags: [css-cascade, specificity, css-inheritance, revert-layer, inherit, initial, unset, revert, all-property]
level: practitioner
status: verified
description: "Using inherit, initial, unset, revert and revert-layer plus the all property to reset or restore styles correctly, and knowing which properties inherit."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Inheritance
  - https://developer.mozilla.org/en-US/docs/Web/CSS/revert-layer
  - https://developer.mozilla.org/en-US/docs/Web/CSS/all
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance keywords (inherit, initial, unset, revert, revert-layer)

**Goal:** reset or restore a property to the right baseline instead of hard-coding values that drift.

## 1. What inherits
Inherited by default: most text properties (`color`, `font-*`, `line-height`, `letter-spacing`, `text-align`, `visibility`, `cursor`, `direction`, list styles) and custom properties. Not inherited: box model, layout, background, border, `display`, `position`, `opacity`, `transform`.

## 2. The keywords
| Keyword | Value becomes |
|---|---|
| `inherit` | Parent's computed value (forces inheritance for non-inherited props) |
| `initial` | The property's spec initial value (`display: initial` = `inline`, not `block`!) |
| `unset` | `inherit` for inherited props, `initial` otherwise |
| `revert` | The value from the **user-agent/user stylesheet** (e.g. `display: revert` on a `div` = `block`) |
| `revert-layer` | The value from the **previous cascade layer** |

## 3. Practical uses
```css
button { font: inherit; color: inherit; }              /* form controls don't inherit fonts by default */
.icon { fill: currentColor; }                          /* follow text color */
.prose ul { list-style: revert; padding-inline-start: revert; }   /* restore browser list styles after a reset */
@layer components { .btn:disabled { background: revert-layer; } }   /* fall back to the base layer's background */
.embed { all: revert; }                                /* back to UA defaults for a third-party widget */
```
`all: initial` is usually wrong (turns everything into `display: inline`, `font: Times`); `all: revert` is what people usually mean (run in Chromium 156: a `div` becomes `block`). `all: unset` also gives a `div` `display: inline`, the same as `all: initial`.

## 4. Gotchas
- `initial` for `display`, `color` etc. ignores the UA stylesheet - a common surprise when "resetting".
- Custom properties inherit; set them on `:root` for globals or on a component for theming, and use `@property` with `inherits: false` for ones that shouldn't.
- `currentColor` resolves at the element where it's used (follows `color` changes).

## Verify
- [ ] Buttons and inputs match surrounding font after `font: inherit`.
- [ ] Lists in rich-text content show bullets after a global reset via `revert`.
- [ ] DevTools Computed pane shows the expected inherited source.
