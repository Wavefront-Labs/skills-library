---
id: computing-software.web-development.web-accessibility.apg-toast-and-alert-notifications
name: apg-toast-and-alert-notifications
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, toast-notifications, alert-pattern, live-regions, wcag-4-1-3]
level: practitioner
status: docs-checked
description: "Announcing toasts and alerts accessibly: role=status vs role=alert, pre-rendered live regions, timing (no auto-dismiss for actionable toasts), focus rules and stacking."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/alert/
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
  - https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA19
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toast and alert notifications

## 1. Roles
- `role="status"` (implicit `aria-live="polite"`): non-urgent confirmations - "Saved", "Item added to cart", "3 results".
- `role="alert"` (implicit `aria-live="assertive"`): urgent, time-sensitive - "Session expires in 2 minutes", "Payment failed". Interrupts speech; use sparingly.
- Status messages must be programmatically determinable through role or properties so they are announced without receiving focus (WCAG 4.1.3, Level AA).

## 2. Implementation
Put the live region in the DOM first and inject the message into the empty container afterwards (the pattern in W3C technique ARIA19 for role=alert).
```html
<div id="toasts" class="toast-region" role="status" aria-live="polite" aria-atomic="false"></div>
<div id="alerts" class="visually-hidden" role="alert"></div>
```
```js
function toast(msg, { timeout = 6000 } = {}) {
  const el = document.createElement("div");
  el.className = "toast"; el.textContent = msg;
  region.append(el);
  if (timeout) setTimeout(() => el.remove(), timeout);
}
```
- Place regions outside any element that may become `inert`/`aria-hidden` (modals).
- Keep messages short and self-contained ("Draft saved", not "Done").

## 3. Timing and actions
- WCAG 2.2.1 (Timing Adjustable, Level A): for a time limit set by the content the user must be able to turn it off, adjust it (at least ten times the default), or extend it (warned first, with at least 20 seconds to extend). If a toast contains an action (Undo, Retry, View), do not auto-dismiss it, or provide one of those options. Auto-dismissing text-only toasts and pausing on hover/focus is a common design choice.
- Provide a keyboard path to toast actions (e.g. focusable region via shortcut, or duplicate the action in the UI like "Undo" in the item list).
- Don't move focus to the toast (disruptive), except for critical alerts requiring a decision - then use an alertdialog.

## 4. Visual
- Position consistently (bottom/top corner); don't cover primary actions or entirely hide the focused element (2.4.11 Focus Not Obscured (Minimum), AA).
- Text contrast 4.5:1 (1.4.3, AA); name the dismiss button clearly (for example "Dismiss notification").
- Stack multiple toasts, cap the count; avoid duplicates for repeated events.
- `popover="manual"` renders toasts in the top layer and they are not light-dismissed, so you show and hide them yourself.

## Verify
Screen readers announce the message once without focus moving; actionable toasts remain until dismissed; toasts remain visible and announced while a dialog is open.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed: role=status has implicit aria-live polite and aria-atomic true, role=alert implicit assertive (ARIA 1.2); WCAG 4.1.3 Status Messages is AA, 2.2.1 Timing Adjustable is A (turn off, adjust at least ten times, extend with 20 seconds), 2.4.11 Focus Not Obscured (Minimum) is AA, 1.4.3 is 4.5:1; technique ARIA19 injects text into an alert container already present in the DOM; MDN popover manual state is not light-dismissed. APG alert page says alert is a live region and focus is not moved. Removed the 5-10 s timing and the above-modals claim.

Method: documentation only; no commands were run.
