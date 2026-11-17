---
id: computing-software.web-development.web-accessibility.focus-visible-indicators
name: focus-visible-indicators
category: computing-software
field: web-development
product: web-accessibility
tags: [navigable, wcag-navigable, focus-indicator, focus-visible, wcag-2-4-7, wcag-2-4-13, outline, focus-ring, focus-appearance]
level: practitioner
status: verified
description: "Designing visible focus indicators (WCAG 2.4.7, 2.4.13): :focus-visible, outline styles that survive backgrounds and forced colours, and never outline:none."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus visible indicators

**Goal:** keyboard users can always see which element has focus, on every background, in every colour mode.

## 1. Baseline CSS
```css
:focus-visible {
  outline: 3px solid var(--focus, #1a5fff);
  outline-offset: 2px;
}
:focus:not(:focus-visible) { outline: none; }   /* only if you must hide rings for mouse clicks */
```
- `:focus-visible` shows the ring for keyboard focus (and for text inputs always) but not for mouse clicks on buttons - the browser heuristic is what you want.
- **Never** `outline: none` / `outline: 0` without a replacement. Removing focus styles fails 2.4.7 (AA).
- Use `outline`, not `box-shadow`, as the main indicator: forced-colors mode (Windows High Contrast) removes box-shadows but keeps outlines (run with Chromium `forcedColors: active`: computed `box-shadow` became `none` and a transparent outline became opaque; if you use box-shadow, add `outline: 2px solid transparent`).

## 2. Visible on every background
A single blue ring disappears on blue buttons. Options: two-tone ring (`outline: 2px solid #fff; box-shadow: 0 0 0 4px #000`) or `outline-color` per theme. 2.4.13 Focus Appearance (AAA) asks for an indicator whose area is at least that of a 2 CSS px thick perimeter of the unfocused component, with 3:1 contrast between the same pixels in focused and unfocused states; 1.4.11 requires 3:1 against adjacent colours.

## 3. Custom components
- Focus the actual interactive element; if a wrapper should show the ring, use `:focus-within` or `:has(:focus-visible)`.
- Elements with `overflow: hidden` clip outlines: use negative `outline-offset` or pad the container.
- Sticky headers hiding the focused element: see Focus Not Obscured skill (2.4.11).

## 4. Tailwind
`focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600`; Tailwind's preflight.css does not remove outlines (it only sets `outline: auto` on `:-moz-focusring`), but `outline-none` on components does - grep for it.

## Verify
- [ ] Tab through every page: a ring is always visible, including on dark/brand-coloured components.
- [ ] Windows forced colours (DevTools > Rendering > Emulate forced-colors: active): rings still visible.
- [ ] Grep finds no bare `outline: none` / `outline-none` without a replacement.
