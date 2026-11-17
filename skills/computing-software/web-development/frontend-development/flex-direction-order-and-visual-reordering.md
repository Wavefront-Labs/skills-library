---
id: computing-software.web-development.frontend-development.flex-direction-order-and-visual-reordering
name: flex-direction-order-and-visual-reordering
category: computing-software
field: web-development
product: frontend-development
tags: [flex-order, flex-direction, visual-reordering, focus-order, flexbox]
level: practitioner
status: docs-checked
description: "Using flex-direction, row-reverse and order without breaking accessibility: when visual reordering is acceptable, keeping DOM order meaningful, and reading-flow as the fix."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Ordering_items
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/reading-flow
  - https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html
  - https://developer.chrome.com/blog/reading-flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flex-direction, order and visual reordering

## 1. The mechanics
```css
.toolbar { display: flex; flex-direction: row; }         /* main axis: inline direction */
.stack   { display: flex; flex-direction: column; }
.chat    { display: flex; flex-direction: column-reverse; } /* visual order reversed */
.promo   { order: -1; }                                   /* default order is 0; lower goes first */
```
`row-reverse` also flips `justify-content: flex-start` to the right edge, and in RTL `row` already runs right-to-left.

## 2. The accessibility problem
`order`, `*-reverse`, and grid placement change only the visual order. Screen readers, Tab order and text selection follow the DOM. A user tabbing through a form whose fields were reordered visually jumps around the screen (WCAG 2.4.3 Focus Order, 1.3.2 Meaningful Sequence).

Safe uses:
- Purely decorative or non-interactive reordering where sequence doesn't change meaning (image before text on mobile, text first on desktop).
- `column-reverse` for chat logs where DOM order is chronological and the visual just anchors to the bottom (check the screen-reader reading order still makes sense).

Unsafe: reordering links, buttons, form fields, or steps; putting the "primary" button first visually but last in DOM in a way that changes which is reached first.

## 3. Fixes
1. Change the DOM order and keep CSS simple - most reliable.
2. For responsive swaps, render the order that is right for reading and adjust visuals with grid areas on the layout where it differs least.
3. `reading-flow: flex-visual` (Chrome 137+) makes focus and reading order follow the visual flex order; treat as progressive enhancement until other engines ship.
4. Never "fix" focus with positive `tabindex`.

## 4. Testing
Tab through the component at every breakpoint; turn on a screen reader and read linearly.

## Verify
- [ ] Tab order matches the visual order at all breakpoints for every interactive element; no positive tabindex introduced to compensate.

## Checked
2026-10-26. MDN ordering-items guide, reading-flow page and browser-compat-data (main, 2026-10-26): confirmed flex reordering affects only visual rendering while tab and speech order follow the source, row follows the writing direction (right-to-left in Arabic), and reading-flow: flex-visual is Chrome 137+ only (Firefox and Safari not supported). Removed the unconfirmed scroll-anchoring and Firefox inspector claims.
Method: documentation only; no commands were run.
