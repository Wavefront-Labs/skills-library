---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-modal-dialogs
name: designing-modal-dialogs
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [modal-dialog, dialogs, notifications, overlays, dialog-design, focus-management, alert-dialog]
level: practitioner
status: draft
description: "Design modal dialogs: use them rarely, one task and clear title, specific buttons, focus trap and return, Esc and scrim behaviour, and proper dialog ARIA."
sources:
  - "Nielsen Norman Group - Modal and Nonmodal Dialogs: When (and When Not) to Use Them (nngroup.com/articles/modal-nonmodal-dialog)"
  - "W3C WAI-ARIA Authoring Practices - Dialog (Modal) Pattern (w3.org/WAI/ARIA/apg/patterns/dialog-modal)"
  - "MDN Web Docs - dialog element (developer.mozilla.org/docs/Web/HTML/Element/dialog)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modal dialogs

**Goal:** interrupt only when the interruption is worth it, and make it accessible.

## When a modal is justified
Critical info or decision that blocks progress (destructive confirmation, unsaved changes, a required choice, a short focused task). Not for promos, long forms, error spam or content that benefits from the page behind. Prefer inline, popover, side panel (non-modal) or a separate page.

## Anatomy and content
- **Title** states the task or question; short body only; **specific buttons** ("Delete project", "Keep editing"); the primary action is the safe or expected one, destructive actions styled as such.
- Close (X) at the top plus Cancel; **Esc** closes; scrim click closes only if no data loss.
- Size: narrow (about 400-560 px), scroll the body not the page; full-screen sheets on small screens.
- Do not stack modals; do not auto-open on load (consent banners excepted by law, designed minimally).

## Behaviour (accessibility)
- Use native `<dialog>` with `showModal()`, which provides focus trapping, `::backdrop`, Esc and inert background, or implement the ARIA pattern: `role="dialog"` (or `alertdialog` for urgent confirmations), `aria-modal="true"`, `aria-labelledby` the title, `aria-describedby` the message.
- Move focus into the dialog (first focusable, or the heading/least destructive button for alerts); trap Tab; **return focus** to the invoking element on close.
- Lock background scroll; hide the page from assistive technology (`inert`).

## Verify
- [ ] Modal is truly necessary; one task, specific button labels.
- [ ] Esc, focus trap and focus return work; screen reader announces title.
- [ ] Mobile layout and scrolling tested.
