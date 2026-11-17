---
id: computing-software.web-development.web-accessibility.apg-modal-dialog-pattern
name: apg-modal-dialog-pattern
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, accessible-modal, dialog-pattern, focus-management, wai-aria-apg]
level: practitioner
status: verified
description: "Implementing the APG modal dialog pattern: role and labelling, initial focus choice, focus containment, Escape, returning focus, alertdialog, and native dialog first."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
  - https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modal dialog pattern

## 1. Use native `<dialog>` first
`showModal()` gives role, top layer, inert background, Escape and focus return (run in Chromium: first focusable element focused, Escape closed it and returned focus to the opener, background left the AX tree). Tab does not loop only inside a native modal: after the last control it reached browser UI before wrapping, so test it if you need APG's strict cycling. Custom implementations only when you must.

## 2. Requirements (APG)
- `role="dialog"` (or `alertdialog` for urgent confirmations needing a response) and `aria-modal="true"`.
- Name: `aria-labelledby` -> visible title. Optional `aria-describedby` -> short message (for alertdialogs).
- **Initial focus**: the first focusable element by default; but
  - a dialog with long content: focus a static element at the top (title with `tabindex="-1"`) so screen readers start reading at the beginning;
  - destructive confirmations: focus the least destructive action (Cancel);
  - a form: the first field.
- Tab/Shift+Tab cycle within the dialog.
- Escape closes (unless it would lose data - then ask).
- On close, focus returns to the invoking element (or a logical next place if it was removed).
- Background is inert (not just visually dimmed).

## 3. Custom shell
```html
<div class="backdrop" hidden>
  <div role="dialog" aria-modal="true" aria-labelledby="dlg-title" class="dialog">
    <h2 id="dlg-title" tabindex="-1">Edit address</h2>
    …form…
    <button type="button" class="close" aria-label="Close">×</button>
  </div>
</div>
```
Open: save `document.activeElement`, set `inert` on the app root, unhide, focus target. Close: reverse, restore focus. Lock background scroll (`overflow: hidden` on `html` + `scrollbar-gutter: stable`).

## 4. Pitfalls
- Close button as an `<a>` or `<div>` without keyboard support.
- Dialog content taller than viewport with the close button scrolled away - make the body scroll and keep header/actions visible.
- Opening dialogs on page load (unexpected, focus jumps).
- Nested modals - avoid; if unavoidable, each manages focus return to the previous.
- Toasts announcing behind an `aria-modal` dialog may be suppressed in some AT.

## Verify
Keyboard: open, Tab cycles inside, Escape closes, focus returns to trigger. Screen reader: announces "Edit address, dialog" and can't reach background content with the virtual cursor (VoiceOver and NVDA).
