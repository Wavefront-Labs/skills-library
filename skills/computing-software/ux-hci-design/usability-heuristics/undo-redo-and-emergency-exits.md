---
id: computing-software.ux-hci-design.usability-heuristics.undo-redo-and-emergency-exits
name: undo-redo-and-emergency-exits
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [undo-redo-design, emergency-exit, uh-user-control]
level: practitioner
status: draft
description: "Design undo/redo, cancel buttons and escape routes so users can back out of mistaken actions."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Emergency exits
- Prefer **undo** over confirmation dialogs for reversible actions ("Message deleted - Undo" snackbar for several seconds).
- Every modal, wizard and flow needs a visible cancel/close and honours Esc.
- Multi-level undo for editors; define what a step is (typing coalesced into words).
- Back button must work in single-page apps: use the History API (`pushState`) for meaningful views.

## Gotchas
- Undo toasts must be reachable by keyboard and persist long enough (WCAG 2.2.1 timing).
- Soft-delete (trash with retention) beats permanent delete plus confirm.

## Verify
- [ ] From any state, one obvious action leaves without data loss.
