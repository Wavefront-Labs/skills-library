---
id: computing-software.ux-hci-design.platform-guidelines.hig-layout-touch-targets-safe-areas
name: hig-layout-touch-targets-safe-areas
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [hig-layout, safe-area-insets, pg-apple-hig]
level: practitioner
status: draft
description: "Respect safe areas, margins and the 44 x 44 point minimum control size on Apple platforms."
sources:
  - https://developer.apple.com/design/human-interface-guidelines/layout
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Apple layout
- Minimum tappable area 44 x 44 points on iOS (HIG); larger on other input.
- Respect safe areas (notch, Dynamic Island, home indicator); content extends under bars with insets via `safeAreaInset` / Auto Layout safe area guides.
- Use adaptive layouts: size classes (compact/regular) rather than device models.
- Support Dynamic Type and rotation where relevant.
(Verify current numbers against the live HIG; they are revised with OS releases.)

## Verify
- [ ] Test on smallest and largest devices and with split view on iPad.
