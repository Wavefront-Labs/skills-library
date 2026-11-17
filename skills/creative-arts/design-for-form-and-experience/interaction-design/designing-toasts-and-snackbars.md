---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-toasts-and-snackbars
name: designing-toasts-and-snackbars
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [toast, snackbar, transient-notification, notifications, feedback, live-regions, ui-feedback]
level: practitioner
status: docs-checked
description: "Design toasts and snackbars: short non-critical confirmations, one action, queueing, user control of timing, and polite live-region announcements."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toasts and snackbars

**Goal:** brief, non-blocking feedback about a result, that does not hide critical information.

## When to use
Low-stakes confirmations of a user action ("Message sent", "Item archived"). Not for errors that need a decision or fix, not for critical alerts, and not for content the user must read (use inline messages, banners or dialogs).

## Design
- **Short text,** one line where possible, no title; optional **one action** (Undo, View). No icon-only meaning.
- **Position:** consistent; do not cover primary controls or navigation.
- **Duration:** pick one team-wide value and allow longer for text with an action. A toast that disappears on a timer is a time limit: under WCAG 2.2 SC 2.2.1 Timing Adjustable (Level A) the user must be able to turn it off, adjust it or extend it (exceptions: real-time events, essential limits, limits longer than 20 hours), so offer pause on hover and focus, or a persistent variant.
- **One at a time:** queue or replace; never stack more than one or two.
- **Persistent variant** for actions that need a response (with dismiss) rather than auto-dismiss.
- Dismissable by swipe or close button; do not rely on timeout alone for important content.

## Accessibility
- Announce with a polite live region (`role="status"` or `aria-live="polite"`) so the message is conveyed without moving focus (SC 4.1.3 Status Messages).
- Action buttons must be keyboard reachable before the toast disappears; when focus is inside, pause the timer.
- Text contrast at least 4.5:1 (SC 1.4.3).

## Pair with undo
For destructive-but-reversible actions use a toast with Undo instead of a confirmation dialog (`creative-arts.design-for-form-and-experience.interaction-design.choosing-undo-over-confirmation`).

## Verify
- [ ] Used only for low-stakes feedback; one at a time.
- [ ] Timer can be paused or extended; announced politely.

## Checked
2026-11-01. Confirmed: SC 2.2.1 turn-off, adjust and extend options and exceptions (Understanding Timing Adjustable), SC 4.1.3 status messages by role (Understanding Status Messages), and the 4.5:1 text ratio (Understanding Contrast Minimum). Removed: the 4-10 second duration range, screen positions and live-region-timing claim, plus the Material 3 and NN/g sources (not readable).
Method: documentation only; no commands were run.
