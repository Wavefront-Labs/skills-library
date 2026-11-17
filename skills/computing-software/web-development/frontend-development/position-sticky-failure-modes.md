---
id: computing-software.web-development.frontend-development.position-sticky-failure-modes
name: position-sticky-failure-modes
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, position-sticky, sticky-header, css, overflow]
level: practitioner
status: docs-checked
description: "Making position sticky work: required inset values, the overflow ancestor trap, parent height limits, table headers, scroll-padding for anchors, and detecting stuck state."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overflow
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Conditional_rules/Container_scroll-state_queries
  - https://www.w3.org/TR/css-position-3/#stickypos-insets
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-padding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# position: sticky and its failure modes

## 1. Minimal
```css
.site-header { position: sticky; top: 0; z-index: var(--z-sticky); }
th { position: sticky; top: 0; background: var(--surface); }
```

## 2. "Sticky doesn't work" checklist
1. **No inset**: needs `top`, `bottom`, `left` or `right`. Without one it behaves like relative.
2. **Ancestor with overflow**: the element sticks to its nearest scrolling ancestor. Any ancestor with `overflow: hidden | auto | scroll` becomes the scroll container - if that ancestor does not itself scroll, sticky never triggers. Replace `overflow: hidden` (used to clip horizontal overflow) with `overflow: clip`, which does not create a scroll container.
3. **Parent too short**: a sticky element can't leave its containing block. Sticky sidebar in a flex row stretched to the content? Fine. Inside a wrapper exactly its own height? It never moves. In flex/grid, `align-self: start` prevents stretching the sticky item to full height.

## 3. Anchors under sticky headers
```css
html { scroll-padding-top: var(--header-height); }
```
Fixes in-page links and focus scrolling hidden behind the header (also WCAG 2.4.11 focus not obscured).

## 4. Detect "stuck" for styling
No CSS pseudo-class widely available yet (scroll-state container queries: `container-type: scroll-state; @container scroll-state(stuck: top)` in Chromium 133+). Fallback: IntersectionObserver on a sentinel element just above the sticky item, or `top: -1px` with `threshold: [1]`:
```js
new IntersectionObserver(([e]) => header.classList.toggle("is-stuck", e.intersectionRatio < 1), { threshold: [1] }).observe(header);
```

## 5. Mobile
Sticky headers eat scarce vertical space and can obscure focused fields with the keyboard open - consider hiding on scroll down, showing on scroll up.

## Verify
Inspect ancestors for overflow values in DevTools; test with keyboard Tab that focused elements aren't hidden.

## Checked

Checked 2026-10-26 against current documentation. MDN `position` (sticky needs an inset, sticks to the nearest ancestor with a scrolling mechanism, creates a stacking context), `overflow` (`clip` is not a scroll container), container scroll-state queries (`container-type: scroll-state`, `stuck`; Chrome 133 only per browser-compat-data) and `scroll-padding`. Removed unconfirmed table, transform and DevTools-warning claims.

Method: documentation only; no commands were run.
