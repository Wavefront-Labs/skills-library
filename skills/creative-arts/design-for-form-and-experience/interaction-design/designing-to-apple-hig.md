---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-to-apple-hig
name: designing-to-apple-hig
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [apple-hig, human-interface-guidelines, ios-design, platform-guidelines, swiftui, sf-symbols, dynamic-type]
level: practitioner
status: draft
description: "Design for Apple platforms with the Human Interface Guidelines: layout and safe areas, Dynamic Type, SF Symbols, system colours, standard navigation and platform conventions."
sources:
  - "Apple Human Interface Guidelines (developer.apple.com/design/human-interface-guidelines)"
  - "Apple - SF Symbols (developer.apple.com/sf-symbols)"
  - "Apple Developer - Design resources and UI kits (developer.apple.com/design/resources)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing to Apple's HIG

**Goal:** an app that feels native on iOS, iPadOS, macOS, watchOS, tvOS and visionOS by using the platform's conventions.

## Core principles
Clarity, deference to content, depth; use **system components** and behaviours first, customising sparingly.

## Key specs and practices
- **Touch targets:** at least **44x44 pt**. Margins respect **safe areas** (Dynamic Island, home indicator) and the layout margins.
- **Typography:** San Francisco; use **text styles** (Large Title 34, Title 1 28, Headline 17 semibold, Body 17, Footnote 13, Caption 12) with **Dynamic Type** so text scales; test at the largest accessibility sizes and let layouts reflow.
- **Colour:** semantic system colours (label, secondaryLabel, systemBackground, systemBlue) that adapt to light, dark and increased contrast; support Dark Mode; accent colour for tint.
- **Icons:** **SF Symbols** with weights and scales matching text; use hierarchical or palette rendering; provide labels (accessibility).
- **Navigation:** tab bar (3-5 tabs) for top-level, navigation stack with large title and Back, sheets for focused tasks, split view on iPad, sidebar on iPad and Mac; support the swipe-back gesture and do not override system gestures.
- **Controls:** standard buttons, segmented controls, pickers, menus; destructive actions in red; confirmation via action sheet / confirmation dialog.
- **Feedback:** haptics (UIFeedbackGenerator) used sparingly; system animations and spring behaviours.
- **Accessibility:** VoiceOver labels and traits, Reduce Motion, Bold Text, Increase Contrast.
- **Privacy:** just-in-time permission requests with a clear purpose string.

## Process
Design with the Apple UI kits in Figma or Sketch, prototype in SwiftUI previews, test on device with Dynamic Type and Dark Mode, and review against the HIG sections for each component used.

## Verify
- [ ] System components, text styles and semantic colours used.
- [ ] 44 pt targets, safe areas, Dark Mode and Dynamic Type verified.
- [ ] Permissions requested in context.
