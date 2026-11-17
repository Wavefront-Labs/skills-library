---
id: computing-software.web-development.web-accessibility.resize-text-and-reflow
name: resize-text-and-reflow
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, reflow, resize-text, wcag-1-4-4, wcag-1-4-10, zoom]
level: practitioner
status: verified
description: "Meeting WCAG 1.4.4 Resize Text (200%) and 1.4.10 Reflow (320 CSS px): relative units, no fixed heights, no horizontal scrolling, viewport zoom, and exceptions."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
  - https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F102
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resize text and reflow

## 1. Requirements
- **1.4.4 (AA)**: text can be resized to 200% without assistive technology and without loss of content or functionality.
- **1.4.10 (AA)**: content reflows at a width equivalent to 320 CSS px (= 1280px at 400% zoom) without two-dimensional scrolling. Vertical-scroll content mustn't need horizontal scroll; horizontal-scrolling content (vertical writing modes) is tested at 256px height.
Exceptions to reflow: content needing 2D layout - data tables, maps, diagrams, video, games, toolbars needing horizontal arrangement in editors.

## 2. Build for it
- Responsive layout that works at 320px wide (it must anyway for phones).
- Font sizes in `rem`/`em`, fluid sizes with a `rem` component (`clamp(1rem, .9rem + .5vw, 1.25rem)`), never `px`-locked or pure `vw` text.
- **No fixed heights on text containers**: use `min-height`; avoid `overflow: hidden` that clips enlarged text, and `line-clamp` that hides content without a way to expand.
- Allow pinch zoom: no `maximum-scale`/`user-scalable=no` (axe `meta-viewport` reports "user-scalable=no on <meta> tag disables zooming", run).
- Sticky headers/footers: at 400% zoom a fixed header can cover most of the viewport - make them non-sticky at short heights (`@media (max-height: 30rem) { header { position: static } }`).
- Long words/URLs: `overflow-wrap: anywhere`.
- Modals: scrollable content (`max-height` + `overflow: auto`) so the close button and actions stay reachable.

## 3. Common failures
- Text in images (doesn't reflow, pixelates).
- Horizontal scrolling page at 320px due to fixed-width elements (`width: 600px`, `100vw` + scrollbar).
- Truncated labels/buttons with ellipsis and no alternative.
- Content that disappears in mobile layouts (hidden at small widths) - zoomed desktop users lose it.

## Verify
- Browser zoom 200% and 400% at a 1280px-wide window: no horizontal scroll (except exempt content), nothing overlaps or clips, all functions usable.
- Text-only zoom (where the browser offers it) at 200% for 1.4.4.
- Automated: Playwright at 320px asserting `document.documentElement.scrollWidth <= clientWidth` (a 600px-wide block gave 600 vs 320, run).
