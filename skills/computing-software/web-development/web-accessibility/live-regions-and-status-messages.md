---
id: computing-software.web-development.web-accessibility.live-regions-and-status-messages
name: live-regions-and-status-messages
category: computing-software
field: web-development
product: web-accessibility
tags: [name-role-value, wcag-robust, live-regions, status-messages, wcag-4-1-3, aria-live, role-status, role-alert, screen-reader-announcements]
level: practitioner
status: verified
description: "Announcing status messages without moving focus (WCAG 4.1.3): role=status vs alert, aria-live politeness, pre-rendered regions and why updates get missed."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions
  - https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live regions and status messages

**Goal:** screen reader users hear "Saved", "3 results", "Added to basket" or errors that appear without a page load, without focus being yanked around.

## 1. Choose the role
| Message | Markup | Behaviour |
|---|---|---|
| Success/info, results count, progress | `role="status"` (implicit `aria-live="polite"`, `aria-atomic="true"`; Chromium AX tree, run) | Announced when the user is idle |
| Urgent error needing immediate attention | `role="alert"` (implicit `assertive`, atomic) | Interrupts current speech |
| Log/chat/feed | `role="log"` | Polite, not atomic: new entries announced |
| Timer | `role="timer"` | No live setting exposed (off) |
Prefer `status`; overuse of `alert` makes the experience noisy.

## 2. The region must exist before the message
```html
<div id="cart-status" role="status" class="visually-hidden"></div>
```
```js
statusEl.textContent = '';                       // optional reset so a repeated message is re-announced
setTimeout(() => { statusEl.textContent = 'Added "Blue T-shirt" to basket'; }, 50);
```
Most screen readers only announce **changes** to a region that was already in the accessibility tree. Injecting `<div role="alert">Error</div>` in one go is announced by many but not all combinations; rendering the container on load and updating its text is reliable.

## 3. Rules
- Keep messages short and complete in themselves; one region per kind of message, not one per component.
- Don't put interactive content in live regions; don't make huge regions (whole lists) live.
- `aria-atomic="true"` reads the whole region on change (status is atomic by default in spec, but set it explicitly for consistency).
- Visible toasts: the visible element can be the live region; make sure it stays long enough (WCAG 2.2.1) or is dismissible.
- Frameworks: React re-mounting the region on each render breaks announcements - keep it mounted at app root and update text via context/store.

## 4. 4.1.3 scope
Applies to messages that **don't** receive focus. If you move focus to an error summary, the focus move announces it - no live region needed.

## Verify
- [ ] NVDA + Firefox/Chrome and VoiceOver + Safari announce: search results count, save confirmation, add-to-cart.
- [ ] Repeated identical messages are announced each time.
- [ ] No unexpected announcements on page load.
