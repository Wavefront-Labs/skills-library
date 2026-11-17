---
id: computing-software.web-development.tailwind-css.has-relational-selector
name: has-relational-selector
category: computing-software
field: web-development
product: tailwind-css
tags: [css-selectors, pseudo-classes, has-selector, parent-selector, relational-selector, quantity-queries, form-state-styling]
level: practitioner
status: verified
description: "Using :has() as a parent/relational selector: styling containers by children, form state, quantity queries, page-level state, and performance limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:has
  - https://webkit.org/blog/13096/css-has-pseudo-class/
  - https://developer.chrome.com/blog/has-m105
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# :has() relational selector

**Goal:** style an element based on what it contains or what follows it, replacing JS that toggled classes.

## 1. Patterns
```css
/* parent by child */
.card:has(img) { grid-template-rows: auto 1fr; }
.card:not(:has(img)) { padding-top: 2rem; }

/* form state */
.field:has(input:user-invalid) label { color: var(--danger); }
form:has(:invalid) button[type=submit] { opacity: .6; }
label:has(input[type=checkbox]:checked) { font-weight: 600; }

/* previous sibling */
h2:has(+ p.lead) { margin-bottom: .25rem; }

/* quantity query: grid changes when there are 5+ items */
.grid:has(> :nth-child(5)) { grid-template-columns: repeat(3, 1fr); }

/* page-level state without JS */
html:has(dialog[open]) { overflow: hidden; }      /* scroll lock while a modal is open */
body:has(#dark-toggle:checked) { color-scheme: dark; }
```

## 2. Rules
- Specificity of `:has()` = its most specific argument (like `:is()`).
- Can't nest `:has()` inside `:has()`, and pseudo-elements aren't allowed inside it.
- Supported in all current engines (Firefox since 121). Fallback: put enhancements inside `@supports selector(:has(*)) { … }`.

## 3. Performance
Browsers optimise most uses, but broad subject + broad argument (`*:has(*)`, `body:has(.x)` on huge DOMs with frequent mutations) can cause expensive style invalidation. Anchor to specific classes and child combinators (`:has(> .x)`) where possible; check "Recalculate Style" cost in the Performance panel.

## 4. Don't replace state that matters to assistive tech
`:has()` changes visuals only. If the visual change communicates state (selected, expanded), the markup still needs the semantics (`aria-expanded`, `aria-invalid`).

## Verify
- [ ] Removing the JS class toggles you replaced keeps behaviour identical in all target browsers.
- [ ] Performance panel shows no long style recalculations when typing in forms using `:has()`.
- [ ] Fallback layout acceptable where unsupported (if your audience needs it).
