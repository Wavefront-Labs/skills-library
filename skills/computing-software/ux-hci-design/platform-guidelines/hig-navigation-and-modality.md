---
id: computing-software.ux-hci-design.platform-guidelines.hig-navigation-and-modality
name: hig-navigation-and-modality
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [hig-navigation, hig-modality]
level: practitioner
status: draft
description: "Use tab bars, navigation stacks, sidebars and sheets as HIG recommends and avoid unnecessary modals."
sources:
  - https://developer.apple.com/design/human-interface-guidelines/tab-bars
  - https://developer.apple.com/design/human-interface-guidelines/modality
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Apple navigation
- Tab bar: top-level peer sections (typically up to 5 on iPhone), persistent, not for actions.
- Navigation stack / back button for hierarchical drill-down, support swipe-back gesture.
- Sidebar on iPad and Mac for larger hierarchies.
- Modal sheets for focused tasks that must be completed or dismissed; provide a clear dismissal (Done/Cancel); avoid stacking modals.

## Verify
- [ ] Interactive swipe-back and dismissal gestures work and do not conflict with custom gestures.
