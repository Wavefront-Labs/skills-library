---
id: computing-software.web-development.frontend-development.css-style-queries-and-if-function
name: css-style-queries-and-if-function
category: computing-software
field: web-development
product: frontend-development
tags: [css-style-queries, css-if-function, container-queries, custom-properties, css-conditionals]
level: advanced
status: docs-checked
description: "Conditional CSS with container style queries on custom properties and the new if() function: syntax, browser support, theming and variant use cases, and fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/if
  - https://drafts.csswg.org/css-values-5/#if-notation
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style queries and the CSS if() function

## 1. Container style queries
Query the computed value of a custom property on an ancestor container. Any element is a style container by default (no `container-type` needed).
```css
.card-list { --variant: compact; }
@container style(--variant: compact) {
  .card { padding: .5rem; font-size: .875rem; }
  .card img { display: none; }
}
/* Range syntax on registered numeric properties (newer) */
@container style(--rating > 3) { .stars { color: gold; } }
```
- Support (browser-compat-data): custom-property style queries from Chrome 111, Safari 18 and Firefox 151; range syntax from Chrome 142 and Firefox 151. MDN states that queries on regular properties (for example `style(font-weight: bold)`) are not supported in any browser.
- The query matches the **parent container**, not the element itself: you can't style an element by its own `--variant`; put the property on a wrapper.

## 2. if() inline conditionals (Chrome 137+; not in Firefox or Safari per browser-compat-data)
```css
.btn {
  background: if(style(--intent: danger): crimson; style(--intent: success): seagreen; else: royalblue);
  padding: if(media(width < 40rem): .5rem 1rem; else: .75rem 1.5rem);
  inset-inline: if(supports(inset-inline: 0): 0; else: auto);
}
```
- Conditions: `style()`, `media()`, `supports()`. First true branch wins; `else` is always true, so put it last. Branches are separated by semicolons, and there must be no space between `if` and `(`.
- Unsupported browsers drop the whole declaration: put a plain declaration first as a fallback.
```css
.btn { background: royalblue; background: if(style(--intent: danger): crimson; else: royalblue); }
```

## 3. Use cases
- Component variants driven by one token (`--size: lg`) rather than many modifier classes.
- Theme-dependent tweaks inside design systems: set `--theme: dark` on a section and let nested components react.
- Avoiding JS class toggles for state already expressed as a custom property.

## 4. Fallback strategy
Ship the default styling without queries; enhance with `@container style()`/`if()`. Data attributes (`[data-variant="compact"] .card`) remain a cross-browser alternative.

## Verify
- [ ] Default styling correct in browsers without support; variants apply where supported; no style that disappears entirely because an `if()` declaration was dropped without fallback.

## Checked

Checked 2026-10-26 against current documentation. MDN style-query guide and `if()` page: any element is a style container, custom-property-only queries, `style()`/`media()`/`supports()` conditions, semicolon-separated branches, `else`, no space before `(`; support from browser-compat-data (custom-property style queries Chrome 111, Safari 18, Firefox 151; range syntax Chrome 142, Firefox 151; `if()` Chrome 137 only). Fixed: Firefox now supports style queries. Removed the unconfirmed `@supports` detection and own-property claims.

Method: documentation only; no commands were run.
