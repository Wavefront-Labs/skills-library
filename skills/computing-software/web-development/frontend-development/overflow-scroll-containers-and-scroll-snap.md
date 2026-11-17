---
id: computing-software.web-development.frontend-development.overflow-scroll-containers-and-scroll-snap
name: overflow-scroll-containers-and-scroll-snap
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, overflow, scroll-snap, scroll-containers, overscroll-behavior, css]
level: practitioner
status: docs-checked
description: "Managing overflow and scroll containers: clip vs hidden vs auto, scrollable region accessibility, scroll-snap carousels, overscroll-behavior and scrollbar-gutter."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overflow
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-type
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-stop
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Overscroll_behavior
  - https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overflow, scroll containers and scroll snap

## 1. Overflow values
- `visible` (default) - content spills out.
- `hidden` - clips, but **creates a scroll container** (programmatically scrollable, breaks `position: sticky` for descendants, creates BFC).
- `clip` - clips without a scroll container; use it to cut horizontal overflow without breaking sticky. `overflow-clip-margin` extends the clip edge.
- `auto` - scrollbars only when needed; `scroll` - always.
With two values, a `visible` axis behaves as `auto` when the other axis is neither `visible` nor `clip`, and `clip` behaves as `hidden` in the same case.

## 2. Horizontal overflow bugs
Find the culprit: `document.querySelectorAll("*").forEach(e => e.scrollWidth > document.documentElement.clientWidth && console.log(e))`. Usual causes: `100vw`, long URLs (`overflow-wrap: anywhere`), images without `max-width: 100%`, flex items with `min-width: auto`, negative margins.

## 3. Scrollable regions and a11y
A scrolling `div` must be keyboard-scrollable: do not rely on the browser making it focusable; add `tabindex="0"`, `role="region"` and an `aria-label`. The axe rule `scrollable-region-focusable` checks this.

## 4. Scroll snap
```css
.carousel { display: flex; gap: 1rem; overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; scroll-padding-inline: 1rem; }
.carousel > * { flex: 0 0 80%; scroll-snap-align: start; }
```
- `mandatory` means the scroll container must snap to a snap position; `proximity` lets the browser decide. Prefer `proximity` when snap areas can be larger than the viewport.
- `scroll-snap-stop: always` stops fast swipes skipping items.
- Provide prev/next buttons (`el.scrollBy({ left: el.clientWidth, behavior: "smooth" })`) - not all users can swipe or shift-scroll.

## 5. Other controls
- `overscroll-behavior: contain` on modals/side panels stops scroll chaining to the page.
- `scrollbar-gutter: stable` reserves space so content doesn't jump when scrollbars appear (or when locking body scroll).
- `scrollbar-width: thin; scrollbar-color: ...` standard styling; `::-webkit-scrollbar` for older WebKit.

## Verify
Keyboard: Tab into scroll regions and arrow-scroll; narrow viewport has no horizontal page scroll; carousel reachable with buttons.

## Checked

Checked 2026-10-26 against current documentation. MDN `overflow` (which values create a scroll container, `visible`/`clip` coercion with two values, block formatting context), `scroll-snap-type` (`mandatory` versus `proximity`), `scroll-snap-stop`, `scrollbar-gutter`, overscroll-behavior guide (scroll chaining) and the axe rule `scrollable-region-focusable`. Removed unconfirmed Chromium-130 focusable-scroller, pull-to-refresh and `100vw` claims.

Method: documentation only; no commands were run.
