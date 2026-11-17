---
id: computing-software.web-development.frontend-development.nth-child-of-selector-and-structural-pseudo-classes
name: nth-child-of-selector-and-structural-pseudo-classes
category: computing-software
field: web-development
product: frontend-development
tags: [nth-child-of-selector, structural-pseudo-classes, nth-of-type, quantity-queries, css-selectors]
level: practitioner
status: docs-checked
description: "Structural selectors done right: An+B formulas, :nth-child(An+B of S) for filtered zebra stripes, nth-child vs nth-of-type, last/only-child, and quantity queries with :has()."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:nth-child
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:nth-of-type
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:has
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# :nth-child(An+B of S) and structural pseudo-classes

## 1. An+B cheat sheet
| Selector | Matches |
|---|---|
| `:nth-child(odd)` / `(2n+1)` | 1, 3, 5... |
| `:nth-child(3n)` | 3, 6, 9... |
| `:nth-child(-n+3)` | first three |
| `:nth-child(n+4)` | 4th onwards |
| `:nth-last-child(-n+2)` | last two |
| `:nth-child(n+3):nth-child(-n+6)` | 3rd to 6th |

## 2. `of S`: count only matching siblings (Baseline 2023)
```css
tr:nth-child(even of :not([hidden])) { background: #f6f6f6; }   /* zebra stripes survive filtering */
li:nth-child(1 of .featured) { border-top: 0; }                  /* first featured item */
```
Plain `tr:not([hidden]):nth-child(even)` still counts hidden rows, so stripes break when you filter.

## 3. nth-child vs nth-of-type
`:nth-of-type` counts siblings of the same **element type**, not class: `.card:nth-of-type(2)` means "a `.card` that is the second `div`", which surprises people. Use `:nth-child(2 of .card)` for class-based counting.

## 4. Edge and count selectors
`:first-child`, `:last-child`, `:only-child`, `:empty`.
Quantity queries:
```css
ul:has(> li:nth-child(5)) { columns: 2; }             /* 5 or more items */
ul:has(> li:only-child) { padding: 0; }
ul:not(:has(> li:nth-child(3))) { display: flex; }    /* fewer than 3 */
```

## Gotchas
- Selectors are evaluated against the DOM, so React keys/reorders change which element is "2nd".

## Verify
- [ ] Filtering a table keeps alternating stripes; DevTools Styles shows the `of S` rule matching.

## Checked

Checked 2026-10-26 against current documentation. MDN `:nth-child()` and `:nth-of-type()` pages and browser-compat-data for the `of S` syntax (Chrome 111, Firefox 113, Safari 9; Baseline 2023). Removed unconfirmed `:empty` whitespace and `:has()` performance claims.

Method: documentation only; no commands were run.
