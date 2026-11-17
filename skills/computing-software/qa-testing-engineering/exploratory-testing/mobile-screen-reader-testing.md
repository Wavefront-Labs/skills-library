---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-screen-reader-testing
name: mobile-screen-reader-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [talkback, voiceover, mobile-accessibility, screen-reader, a11y, wcag]
level: practitioner
status: draft
description: "Test mobile apps with TalkBack and VoiceOver: gestures, labels, roles and traits, focus order, touch target size, dynamic type and the platform scanners."
sources:
  - https://www.w3.org/WAI/WCAG22/quickref/
  - https://support.google.com/accessibility/android/answer/6283677
  - https://support.apple.com/guide/iphone/turn-on-and-practice-voiceover-iph3e2e415f/ios
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile screen reader testing (TalkBack, VoiceOver)

**Goal:** a blind user can complete the key journeys using only the platform screen reader.

## Setup
- Android: Settings > Accessibility > TalkBack. Enable the accessibility shortcut (hold both volume keys) to toggle fast.
- iOS: Settings > Accessibility > VoiceOver; set the Accessibility Shortcut (triple-click side button).
- Learn the gestures first: swipe right/left = next/previous element, double-tap = activate, two-finger swipe (TalkBack) or three-finger swipe (VoiceOver) = scroll, iOS rotor (two-finger rotate) for headings and links.

## Checks
- **Every control has a meaningful label:** never "button", "unlabeled", or file names like `ic_close_24`. Icons need `contentDescription` (Android) or `accessibilityLabel` (iOS/React Native).
- **Role/trait announced:** button, link, heading, selected, toggled on/off.
- **Focus order** follows visual order; focus is not lost when dialogs open or close; modals contain focus.
- **State changes announced:** errors, loading finished, toasts (live regions / `UIAccessibility.post`).
- **Decorative images** are hidden from the reader.
- **Custom gestures** (swipe-to-delete) have an accessible alternative (actions menu).
- **Touch targets** at least 48x48 dp (Android) / 44x44 pt (Apple HIG).
- **Font scaling** at the largest setting: no clipped or overlapping text.

## Scanners (find the easy half)
Android Accessibility Scanner app; Xcode Accessibility Inspector audit; Espresso `AccessibilityChecks.enable()`.

## Verify
Each critical journey is completed eyes-closed with the reader on both platforms, and scanner reports are clean or each item is triaged.
