---
id: computing-software.web-development.tailwind-css.where-and-is-specificity-control
name: where-and-is-specificity-control
category: computing-software
field: web-development
product: tailwind-css
tags: [css-cascade, specificity, where-selector, is-selector, zero-specificity, forgiving-selectors, css-selectors]
level: practitioner
status: verified
description: "Controlling specificity with :where() (zero) and :is() (highest argument), writing low-specificity defaults and grouping selectors without bloat."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:where
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:is
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# :where() and :is() for specificity control

**Goal:** write defaults that are trivially overridable and group selectors without accidentally raising specificity.

## 1. The difference
| Selector | Specificity |
|---|---|
| `:where(.card, #main) a` | `0,0,1` - `:where()` contributes **zero** |
| `:is(.card, #main) a` | `1,0,1` - takes the **most specific** argument (`#main`) for every match |
Both accept a forgiving selector list: an invalid selector in the list doesn't invalidate the whole rule (unlike plain comma lists).

## 2. Low-specificity defaults with :where
```css
/* design-system base styles anyone can override with a single class */
:where(.prose) :where(h2) { margin-block: 2em .5em; }
:where(button):where(:not([class])) { font: inherit; }
```
Resets differ here: Tailwind 4.3.3 `preflight.css` uses `:where()` in a handful of selectors (6 lines, e.g. `abbr:where([title])`), and modern-normalize 3.0.1 uses none, so do not assume a reset is low-specificity everywhere; Tailwind v4 relies on cascade layers for that. Checked in Chromium 156: `:where(.q,#idm) p` lost to `.a .b .c p`, `:is(.q,#idm) p` beat it (ID specificity), an invalid selector inside `:is()`/`:where()` did not drop the rule, and a plain comma list with an invalid selector dropped the whole rule.

## 3. Grouping with :is
```css
:is(article, section, aside) :is(h1, h2, h3) { line-height: 1.2; }
```
replaces nine selectors. Watch for the "most specific argument" effect: `:is(.btn, #legacy-btn)` makes every `.btn` match carry ID specificity.

## 4. Specificity hacks you no longer need
- Doubling a class (`.btn.btn`) to bump specificity - prefer layers.
- `!important` to beat a library - use `@layer` or wrap the library in `:where`.
- Raising your own specificity with IDs - avoid IDs in selectors entirely.

## 5. Calculation reminder
(IDs, classes/attributes/pseudo-classes, elements/pseudo-elements). `:not()`, `:has()`, `:is()` take their most specific argument; `:where()` is 0; the universal selector and combinators add nothing; inline styles beat all selectors; `!important` flips the game.

## Verify
- [ ] DevTools hover over a selector shows the expected specificity tuple.
- [ ] A single utility class overrides every `:where`-based default.
- [ ] No IDs or doubled classes in new CSS (stylelint `selector-max-id: 0`, `selector-max-specificity`).
