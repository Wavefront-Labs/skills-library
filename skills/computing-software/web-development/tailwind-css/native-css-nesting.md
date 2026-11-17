---
id: computing-software.web-development.tailwind-css.native-css-nesting
name: native-css-nesting
category: computing-software
field: web-development
product: tailwind-css
tags: [css-selectors, pseudo-classes, css-nesting, nesting-selector, ampersand, postcss-nesting, sass-migration]
level: practitioner
status: verified
description: "Writing native CSS nesting: the & selector, nested at-rules, specificity effects (wraps parents in :is), and differences from Sass when migrating."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Using_CSS_nesting
  - https://www.w3.org/TR/css-nesting-1/
  - https://developer.chrome.com/docs/css-ui/css-nesting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native CSS nesting

**Goal:** use nesting in plain CSS without a preprocessor, and avoid the places it differs from Sass.

## 1. Syntax
```css
.card {
  padding: 1rem;
  & .title { font-weight: 600; }        /* descendant; '& ' optional before a class/element in current spec */
  .meta { color: gray; }                 /* same as & .meta */
  &:hover { box-shadow: 0 2px 8px #0002; }
  &.is-active { outline: 2px solid; }    /* compound - & required */
  .dark & { background: #111; }          /* parent context: .dark .card */
  @media (width >= 48rem) { padding: 2rem; }
  @container (width > 30rem) { display: grid; }
}
```
Supported in all current engines (Chrome and Edge 120, Firefox 117, Safari 17.2 per web-features; Baseline since 2023-12-11). Bare element selectors like `p { }` without `&` work in Chromium 156 (run); engines from before the relaxed syntax needed `& p` (version cut-offs not confirmed here, check MDN). For older targets, PostCSS (`postcss-nesting`) or Lightning CSS compiles it away (run: Lightning CSS with a Chrome 100 target flattened the whole example above, including the `.dark &` and `@media` forms).

## 2. Differences from Sass
- **No string concatenation**: `&__title` (BEM suffix) is invalid in native CSS - `&` is a selector, not text. Keep BEM elements flat or stay on Sass.
- **Specificity**: `&` behaves like `:is(parent)`. `#app, .card { & p {} }` becomes `:is(#app, .card) p` - every match gets ID specificity.
- Declarations after nested rules: Chromium 156 applies them in source order (a later `color` after a nested rule won over an earlier one). Older implementations may have hoisted them (not confirmed here); put declarations before nested rules to be safe.

## 3. Style guidance
Nest at most 2-3 levels; deep nesting recreates specificity and coupling problems. Nest state (`&:hover`, `&[aria-expanded=true]`) and media/container queries; avoid nesting structure.

## Verify
- [ ] Build target list (Browserslist) determines whether nesting is compiled; output checked in an old target.
- [ ] No `&__` / `&-` concatenations left after Sass migration.
- [ ] DevTools shows nested rules resolved to expected selectors.
