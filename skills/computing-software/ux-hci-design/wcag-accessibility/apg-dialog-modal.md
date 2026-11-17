---
id: computing-software.ux-hci-design.wcag-accessibility.apg-dialog-modal
name: apg-dialog-modal
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [apg-dialog-modal, modal-focus-management, aria-apg-patterns]
level: practitioner
status: docs-checked
description: "Implement a modal with role=dialog, labelled, focus moved in and returned, Esc to close and background inert."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modal dialog (APG pattern)
- `role="dialog"` with `aria-modal="true"`, named by `aria-labelledby` (a visible title) or `aria-label`.
- On open: focus first focusable element (or the dialog / heading for long content).
- Tab and Shift+Tab cycle within the dialog; Esc closes.
- On close: return focus to the opener.
- Content outside a modal dialog is inert: users cannot interact with it. Include a visible close or cancel button in the tab sequence.

## Verify
- [ ] Keyboard only: open, tab-cycle, Esc, focus returns to trigger.

## Checked

- Date: 2026-11-02.
- Confirmed against the W3C ARIA Authoring Practices Guide Dialog (Modal) pattern: Tab/Shift+Tab containment, Escape closes, initial focus placement, focus returns to the invoking element on close, `aria-modal`, `aria-labelledby`/`aria-label`, inert outside content, close button recommendation.
- Removed: the native `<dialog>`/`showModal()` and `inert` attribute claims (not on the page).

Method: documentation only; no commands were run.
