---
id: computing-software.web-development.web-accessibility.focus-order-and-dom-order
name: focus-order-and-dom-order
category: computing-software
field: web-development
product: web-accessibility
tags: [navigable, wcag-navigable, focus-order, wcag-2-4-3, dom-order, positive-tabindex, css-order, visual-order]
level: practitioner
status: docs-checked
description: "Keeping keyboard focus order logical (WCAG 2.4.3): DOM order matching visual order, CSS reordering pitfalls, positive tabindex, and focus placement after actions."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/order
  - https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus order and DOM order

**Goal:** Tab moves through the page in an order that matches meaning and layout, and focus lands somewhere sensible after every action.

## 1. Source order is focus order
Focus follows DOM order (for `tabindex` 0 / natively focusable elements). CSS that rearranges visually without changing DOM breaks it:
- `flex-direction: row-reverse`, `order`, `grid-area` placement, `grid-auto-flow: dense`, absolute positioning.
Fix the DOM order instead; use CSS reordering only for purely decorative differences. (The CSS `reading-flow` property is marked experimental on MDN; don't rely on it yet.)

## 2. Never positive tabindex
`tabindex="1"+` jumps elements ahead of everything else and creates an order nobody maintains. Use only `0` (make focusable in DOM order) and `-1` (focusable by script only). Lint: `jsx-a11y/tabindex-no-positive`, axe `tabindex`.

## 3. Focus after actions
| Action | Focus goes to |
|---|---|
| Open modal | First focusable element inside it, or a deliberate element such as `autofocus` target (native `<dialog>.showModal()` focuses the first focusable element by default, per MDN) |
| Close modal | The control that opened it |
| Delete item in a list | Next item, or previous, or the list heading |
| Submit form with errors | Error summary or first invalid field |
| SPA navigation | Main heading (`tabindex="-1"`) or a skip target |
| Open disclosure/menu | Stay on trigger (disclosure) or first item (menu) |
Removing the focused element leaves focus on `<body>`, so keyboard users can lose their place.

## 4. Off-screen and hidden content
Closed menus/drawers must be `hidden`/`display:none`/`inert`, not just moved off-screen, or Tab enters invisible items. `visibility:hidden` also removes from tab order.

## Verify
- [ ] Tab through each template: order matches reading order; no invisible stops (watch the focus ring).
- [ ] After closing dialogs and deleting items, `document.activeElement` is a sensible element (not body).
- [ ] No positive tabindex in the codebase.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.4.3 Focus Order (Level A); MDN confirms that positive tabindex values are focused first and that tabindex 0 follows DOM order, that the CSS order property creates a disconnect between visual and DOM order, that visibility:hidden elements and inert subtrees cannot be focused, that showModal() focuses the first focusable element, and that reading-flow is experimental. The lint rules jsx-a11y/tabindex-no-positive and axe `tabindex` exist in their repositories.

Method: documentation only; no commands were run.
