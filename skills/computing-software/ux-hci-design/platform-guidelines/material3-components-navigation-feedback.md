---
id: computing-software.ux-hci-design.platform-guidelines.material3-components-navigation-feedback
name: material3-components-navigation-feedback
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [material3-components, snackbar-vs-dialog]
level: practitioner
status: draft
description: "Choose between navigation bar, rail, drawer; button emphasis levels; and snackbar vs dialog for feedback."
sources:
  - https://m3.material.io/components/navigation-bar/overview
  - https://m3.material.io/components/snackbar/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# M3 component choice
- Navigation bar (3-5 destinations, compact), rail (medium+), drawer (many destinations, expanded).
- Button emphasis: filled > filled tonal > outlined > text; one filled button per screen section.
- Snackbar: brief non-critical feedback, optional single action (Undo), auto-dismiss; dialog: interrupts for decisions or critical info.
- FAB for the primary action of a screen.
- Check m3.material.io for current component names/status; guidelines evolve (e.g. expressive updates).

## Verify
- [ ] Screens show at most one primary emphasis action; undo offered via snackbar for deletions.
