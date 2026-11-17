---
id: computing-software.software-engineering.mobile-development.mobile-accessibility-talkback-voiceover
name: mobile-accessibility-talkback-voiceover
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ui, mobile-accessibility, talkback, voiceover, dynamic-type, touch-targets]
level: practitioner
status: draft
description: "Make mobile apps accessible: labels, roles, focus order, Dynamic Type and font scaling, 48dp/44pt targets, contrast, and testing with TalkBack/VoiceOver."
sources:
  - https://developer.android.com/guide/topics/ui/accessibility
  - https://developer.android.com/develop/ui/compose/accessibility
  - https://developer.apple.com/documentation/accessibility/supporting-voiceover-in-your-app
  - https://www.w3.org/TR/wcag21/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile accessibility: TalkBack, VoiceOver and Dynamic Type

**Goal:** the app is fully usable with a screen reader, large text, switch control and low vision, which in many markets is also a legal requirement.

## 1. Labels and roles
Android Compose:
```kotlin
Icon(Icons.Default.Delete, contentDescription = "Delete order")    // null for purely decorative images
Row(Modifier.semantics(mergeDescendants = true) {}) { Icon(...); Text("4.5 stars") }   // read as one element
Modifier.toggleable(value = on, role = Role.Switch, onValueChange = ...)
Modifier.semantics { stateDescription = if (expanded) "Expanded" else "Collapsed" }
```
SwiftUI:
```swift
Button(action: delete) { Image(systemName: "trash") }
    .accessibilityLabel("Delete order")
HStack { Image(systemName: "star.fill"); Text("4.5") }
    .accessibilityElement(children: .combine)
Toggle("Notifications", isOn: $on)        // standard controls get traits automatically
Image("hero").accessibilityHidden(true)
```
Labels describe purpose, not appearance ("Delete order", not "trash icon"); do not include the role ("button") since the reader announces it.

## 2. Actions and custom controls
Custom gestures (swipe to delete) need equivalent accessibility actions: Compose `Modifier.semantics { customActions = listOf(CustomAccessibilityAction("Delete") { ...; true }) }`, SwiftUI `.accessibilityAction(named: "Delete") { ... }`. Sliders/steppers: `accessibilityAdjustableAction`.

## 3. Text scaling
- Android: use `sp` for text; test at 200% font scale (Android 14 non-linear scaling). Avoid fixed-height containers for text.
- iOS: use text styles (`.font(.body)`, `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory`), test at accessibility sizes (AX5); switch horizontal layouts to vertical at large sizes (`ViewThatFits` or `dynamicTypeSize` checks).

## 4. Touch targets, contrast, motion
- Minimum target: 48x48 dp (Android), 44x44 pt (iOS), even if the visual icon is smaller (`Modifier.minimumInteractiveComponentSize()`, padding/contentShape).
- Contrast 4.5:1 for body text, 3:1 for large text and UI components (WCAG 2.1 AA).
- Never convey meaning by colour alone; respect Reduce Motion (`AccessibilityManager`, `@Environment(\.accessibilityReduceMotion)`).

## 5. Focus and announcements
Logical reading order follows layout; fix with `traversalIndex`/`isTraversalGroup` (Compose) or `accessibilitySortPriority` (SwiftUI). Announce async results: `AccessibilityNotification.Announcement("Saved").post()` (iOS 17), `view.announceForAccessibility` / live regions (`liveRegion = LiveRegionMode.Polite`) on Android.

## 6. Testing
- Manually: every release, complete core flows with TalkBack and VoiceOver on, and at the largest font size.
- Automated: Android Accessibility Scanner, Compose UI tests with semantics matchers and `enableAccessibilityChecks()` (Espresso ATF); Xcode Accessibility Inspector audit and `XCUIApplication().performAccessibilityAudit()` (Xcode 15+) in UI tests.

## Gotchas
- Images of text and text in custom-drawn canvases are invisible to readers.
- Merged elements that contain multiple buttons become unusable; merge only non-interactive content.
- Truncated labels at large text sizes hide information; allow wrapping.

## Verify
- Core flows complete with eyes closed using TalkBack and VoiceOver, automated audits pass in CI, and screens render without clipping at the largest text size.
