---
id: computing-software.web-development.web-accessibility.apg-tooltip-and-toggletip
name: apg-tooltip-and-toggletip
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-tooltip, toggletip, aria-describedby, popover-hint, wcag-1-4-13, apg-patterns]
level: practitioner
status: docs-checked
description: "Accessible tooltips: role=tooltip with aria-describedby, showing on hover and focus, Escape to dismiss, hoverable and persistent per WCAG 1.4.13, and toggletips for touch."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
  - https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tooltip and toggletip patterns

## 1. When a tooltip is appropriate
Short, non-essential, non-interactive supplementary text for a focusable element (icon button hint, keyboard shortcut). If it contains links/buttons or essential instructions, use a toggletip, disclosure or dialog instead.

## 2. Tooltip
```html
<button type="button" aria-describedby="tip-del" class="icon-btn">
  <svg aria-hidden="true">...</svg><span class="visually-hidden">Delete</span>
</button>
<div role="tooltip" id="tip-del" hidden>Delete permanently (Shift+Del)</div>
```
```js
const show = () => tip.hidden = false, hide = () => tip.hidden = true;
btn.addEventListener("mouseenter", show); btn.addEventListener("focus", show);
btn.addEventListener("mouseleave", () => setTimeout(() => { if (!tip.matches(":hover")) hide(); }, 100));
btn.addEventListener("blur", hide);
document.addEventListener("keydown", e => { if (e.key === "Escape") hide(); });
```
- The accessible **name** comes from the button text/label; the tooltip is a **description** (`aria-describedby`). For icon-only buttons the name must exist independently.
- WCAG 1.4.13: dismissible without moving focus (Escape), hoverable (pointer can move onto the tooltip without it vanishing), persistent (stays until dismissed or trigger loses hover/focus).
- A small show delay on hover is typical (APG: a tooltip "typically appears after a small delay"); show immediately on focus.
- Do not rely on `title` attributes as the tooltip: they give you no control over dismissal, hover or persistence behaviour.

## 3. Toggletip (works on touch)
```html
<button type="button" aria-expanded="false" aria-controls="tt1">More info<span aria-hidden="true">?</span></button>
<div id="tt1" role="status"></div>   <!-- inject text on click so it is announced -->
```
Click toggles; Escape and outside click close.

## 4. Platform help
The Popover API (`popover="hint"`, which does not close `auto` popovers, per MDN) gives top-layer rendering and light dismiss; still add `aria-describedby`, focus triggers and Escape handling as needed.

## Verify
- [ ] Tooltip appears on keyboard focus, stays while hovering it, closes on Escape; the screen reader exposes it as the description of the trigger.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG tooltip pattern: role tooltip, trigger references it with aria-describedby, Escape dismisses, focus stays on the trigger, tooltip dismissed on blur, small delay before display, tooltips do not receive focus (a hover that contains focusable elements should be a non-modal dialog). WCAG 1.4.13 Content on Hover or Focus requires dismissible, hoverable and persistent content (Level AA). MDN confirms the hint popover state. Removed the 300 ms figure and the title-attribute claims.

Method: documentation only; no commands were run.
