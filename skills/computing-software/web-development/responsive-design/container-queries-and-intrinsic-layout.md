---
id: computing-software.web-development.responsive-design.container-queries-and-intrinsic-layout
name: container-queries-and-intrinsic-layout
category: computing-software
field: web-development
product: responsive-design
tags: [container-queries, clamp, fluid-typography, intrinsic-sizing, media-queries, css, cqw, responsive-design, web-development]
level: advanced
status: verified
description: "Container queries for component-level responsiveness (vs viewport media queries), and fluid sizing with clamp() instead of breakpoint jumps."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries
  - https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container queries and intrinsic/fluid layout

**Goal:** a component that responds to the space it's actually given (a sidebar
slot vs a full-width slot) rather than only the viewport — and sizing that
scales smoothly instead of jumping at breakpoints.

## 1. Why media queries aren't enough for component-based UI
A `@media (min-width: 768px)` query only knows the viewport size — a card
component placed in a wide main column looks different from the same component
dropped into a narrow sidebar, but a media query can't tell them apart; it only
sees "the screen is 1440px," not "this particular box is 280px." This is the
core limitation container queries exist to fix — true component-level
responsiveness independent of where it's placed on the page.

## 2. Container queries — set up and use
```css
.card-grid { container-type: inline-size; container-name: card-grid; }

@container card-grid (min-width: 400px) {
  .card { grid-template-columns: 1fr 2fr; }   /* only when THIS container is ≥400px wide */
}
```
`container-type: inline-size` opts an element in as a query container along its
inline axis (width, in horizontal writing mode) — a component inside it can now
query *that* container's width regardless of the viewport. `container-name` is
optional but avoids ambiguity when containers nest (without it, `@container`
targets the nearest ancestor container, which can be the wrong one in deeply
nested layouts; run in Chromium 156: an unnamed `@container (min-width: 250px)` matched the inner 300px container, and a rule naming the outer 300px container with `min-width: 400px` did not match). An element cannot query itself (a `.s` with `container-type` and a matching `@container` rule did not change), and `container-type: inline-size` ignores content width, so in a shrink-to-fit parent the container collapsed to 0px: give it an explicit or stretched width.

## 3. Container query units — sizing relative to the container, not the viewport
`cqw`/`cqh`/`cqi`/`cqb` (container query width/height/inline/block) work like
`vw`/`vh` but relative to the nearest query container instead of the viewport —
useful for text/padding that should scale with the component's own box
regardless of where it sits on the page (run: in a 400px container `5cqi` resolved to 20px; in a 300px one, `clamp(1rem, 5cqi, 1.5rem)` clamped to the 16px minimum):
```css
.card-title { font-size: clamp(1rem, 5cqi, 1.5rem); }
```

## 4. Browser support and the fallback posture
Container queries are Baseline newly available since 2023-02-14 (Chrome 105, Firefox 110, Safari 16; per MDN compat data) — verify against your actual support target before relying on them as
the only layout mechanism; provide a sane default layout outside the
`@container` block so unsupported browsers get *a* usable layout, just not the
adaptive one.

## 5. Fluid sizing with `clamp()` instead of breakpoint jumps
```css
h1 { font-size: clamp(1.75rem, 1.25rem + 2vw, 3rem); }
```
`clamp(min, preferred, max)` scales smoothly between the min and max bounds as
the viewport (or container, with `cqw`) changes, instead of a heading jumping
abruptly from 28px to 48px at exactly one breakpoint. This replaces most of the
"define font-size at 4 different media query breakpoints" pattern with one
line that's continuous at every width in between. The preferred value needs a
relative unit (`vw`/`cqw`) to actually scale — a clamp with only fixed units in
the middle term just picks a constant (run: `clamp(1rem, 10px, 1.5rem)` gave 16px).

## 6. When to reach for which tool
- **Media query**: page-level layout decisions tied to actual viewport/device
  class (show a mobile nav vs desktop nav).
- **Container query**: a reusable component (card, widget) that must adapt to
  whatever slot it's placed in, independent of viewport.
- **`clamp()`/fluid units**: continuous scaling of type size, spacing, or
  dimensions — anywhere a breakpoint jump would look like an obvious seam.

## Verify
- [ ] Components meant for reuse in varying-width slots use container queries, not viewport media queries, for their internal layout.
- [ ] Every `@container` rule has an unambiguous `container-name` where containers can nest.
- [ ] A default (non-adaptive) layout exists outside the container-query block for unsupported browsers.
- [ ] Type/spacing scales use `clamp()` with a relative preferred unit rather than discrete per-breakpoint values.
- [ ] Container query unit (`cqw`/`cqi`) usage is verified against the actual container, not assumed to behave like `vw`.
