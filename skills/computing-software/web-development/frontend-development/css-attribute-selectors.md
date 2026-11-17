---
id: computing-software.web-development.frontend-development.css-attribute-selectors
name: css-attribute-selectors
category: computing-software
field: web-development
product: frontend-development
tags: [attribute-selectors, css-selectors, data-attributes, aria-selectors]
level: intro
status: docs-checked
description: "CSS attribute selectors: presence, exact, prefix, suffix, substring and word matches, the i/s flags, styling via ARIA and data attributes, specificity and performance notes."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Attribute_selectors
  - https://www.w3.org/TR/selectors-4/#attribute-selectors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attribute selectors

## 1. The operators
| Selector | Matches |
|---|---|
| `[disabled]` | attribute present (any value, even empty) |
| `[type="email"]` | exact value |
| `[class~="card"]` | whitespace-separated word list contains `card` |
| `[lang\|="en"]` | `en` or starts with `en-` |
| `[href^="https://"]` | starts with |
| `[href$=".pdf"]` | ends with |
| `[href*="example.com"]` | contains |
| `[data-state="open" i]` | case-insensitive value |
| `[type="a" s]` | force case-sensitive |

Values with spaces or special characters need quotes; always quoting is simplest.

## 2. Practical uses
```css
/* Style by ARIA state: one source of truth for JS and assistive tech */
[aria-expanded="true"] > .chevron { rotate: 180deg; }
[aria-current="page"] { font-weight: 600; text-decoration: underline; }
[aria-invalid="true"] { border-color: var(--danger); }
[aria-disabled="true"] { opacity: .5; cursor: not-allowed; }

/* Component state via data attributes (also what Radix/Headless UI expose) */
.tab[data-state="active"] { border-bottom: 2px solid; }

/* External and file links */
a[href^="http"]:not([href*="example.com"])::after { content: " (external)"; }
a[href$=".pdf" i]::after { content: " (PDF)"; }

/* Inputs without a type default to text */
input:not([type]), input[type="text"] { ... }
```
Styling off ARIA attributes forces the attributes to be correct: if the chevron doesn't rotate, the screen reader isn't told either.

## 3. Specificity
- Attribute selectors have the same specificity as a class (0,1,0).

## 4. Gotchas
- `[class="btn"]` fails when the element has multiple classes; use `.btn` or `~=`.

## Verify
- [ ] State styles follow ARIA/data attributes toggled by JS.

## Checked
2026-10-26. MDN attribute selectors and specificity pages (main, 2026-10-26): confirmed the present, =, ~=, |=, ^=, $=, *= forms, the i and s case flags, and that attribute selectors share class-level specificity. Removed unconfirmed performance and boolean-attribute remarks.
Method: documentation only; no commands were run.
