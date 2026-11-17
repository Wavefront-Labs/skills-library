---
id: computing-software.ux-hci-design.usability-heuristics.status-you-are-here-indicators
name: status-you-are-here-indicators
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [you-are-here, system-state-indicator]
level: practitioner
status: draft
description: "Make current location, selection and mode visible: active nav item, breadcrumbs, step indicators and mode labels."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Showing where the user is and what state things are in
- **Current location**: highlight the active navigation item; use `aria-current="page"` on it for assistive tech.
- **Multi-step flows**: show "Step 2 of 4" with named steps, and mark completed steps.
- **Selection**: show how many items are selected ("3 selected") and what actions apply.
- **Modes**: if the UI has modes (edit vs view), label the mode visibly, not only by cursor or colour.
- **Background processes**: sync status ("Saved", "Saving...", "Offline - changes will sync").

## Gotchas
- Do not rely on colour alone to mark the active item (WCAG 1.4.1); add weight, underline or an icon.
- Status text that changes dynamically needs a live region so screen readers hear it (WCAG 4.1.3).

## Verify
- [ ] On every page, a first-time user can tell where they are without using the back button.
