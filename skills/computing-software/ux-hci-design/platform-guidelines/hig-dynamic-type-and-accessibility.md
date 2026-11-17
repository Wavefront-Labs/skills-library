---
id: computing-software.ux-hci-design.platform-guidelines.hig-dynamic-type-and-accessibility
name: hig-dynamic-type-and-accessibility
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [dynamic-type, voiceover-labels]
level: practitioner
status: draft
description: "Use text styles for Dynamic Type, label controls for VoiceOver and honour Reduce Motion and contrast settings."
sources:
  - https://developer.apple.com/design/human-interface-guidelines/accessibility
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Apple accessibility
- Use system text styles (`.body`, `.headline`) so text scales; test at the largest accessibility sizes and avoid truncation.
- SwiftUI: `.accessibilityLabel`, `.accessibilityHint`, `.accessibilityValue`; UIKit: `accessibilityLabel`, traits.
- Respect `UIAccessibility.isReduceMotionEnabled`, Increase Contrast, Bold Text, Differentiate Without Color.
- Use Accessibility Inspector in Xcode to audit.

## Verify
- [ ] Complete core flows with VoiceOver and at the largest Dynamic Type size.
