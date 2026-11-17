---
id: computing-software.ux-hci-design.platform-guidelines.platform-differences-ios-android-web
name: platform-differences-ios-android-web
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [cross-platform-design, platform-adaptation]
level: advanced
status: draft
description: "Decide what stays consistent across platforms (brand, flows) and what follows platform conventions (navigation, controls)."
sources:
  - https://developer.apple.com/design/human-interface-guidelines/
  - https://m3.material.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-platform
- Keep consistent: information architecture, terminology, brand, core flows.
- Adapt to platform: back behaviour (iOS swipe-back vs Android system back/predictive back), navigation placement, dialogs and pickers, typography (SF vs Roboto/Google Sans), haptics, share sheets.
- Cross-platform frameworks (Flutter, React Native) need explicit platform adaptation.
- Jakob's law: users of each platform expect that platform's conventions.

## Verify
- [ ] Platform-native users complete core tasks without unfamiliar gestures.
