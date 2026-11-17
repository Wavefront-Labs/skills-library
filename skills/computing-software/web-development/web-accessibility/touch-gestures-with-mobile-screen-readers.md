---
id: computing-software.web-development.web-accessibility.touch-gestures-with-mobile-screen-readers
name: touch-gestures-with-mobile-screen-readers
category: computing-software
field: web-development
product: web-accessibility
tags: [touch-screen-reader, voiceover-ios, talkback, mobile-accessibility, gestures]
level: practitioner
status: docs-checked
description: "Making custom touch interactions work with VoiceOver and TalkBack running: how gestures are intercepted, swipe/drag/pinch alternatives, adjustable controls and testing gestures."
sources:
  - https://support.apple.com/guide/iphone/learn-voiceover-gestures-iph3e2e2281/ios
  - https://support.google.com/accessibility/android/answer/6151827
  - https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html
  - https://www.w3.org/TR/mobile-accessibility-mapping/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Touch gestures with mobile screen readers running

When VoiceOver (iOS) or TalkBack (Android) is on, the screen reader intercepts touch gestures, so custom touch gestures may never reach your page.

## 1. What reaches the page
- Make every action reachable through a real control that responds to `click`; screen reader users activate controls by double-tap.

## 2. Provide alternatives for every custom gesture
| Custom gesture | Screen-reader-friendly alternative |
|---|---|
| Swipe to delete/archive a row | Visible or actions-menu button per row |
| Drag to reorder | Move up/down buttons or a "Move to" menu |
| Pinch zoom on a map/image | + / - buttons |
| Carousel swipe | Previous/next buttons, all slides reachable in linear order |
| Pull to refresh | Refresh button |
| Long-press context menu | A "More actions" button |

This also satisfies WCAG 2.5.1 (pointer gestures) and 2.5.7 (dragging movements).

## 3. Don't break native behaviour
- Avoid `user-scalable=no`/`maximum-scale=1` in the viewport meta: blocks zoom (1.4.4).
- Custom elements that react to `touchstart` but not `click` are dead to screen readers.
- Focusable things must have accessible names; the swipe cursor lands on every focusable element and reads it.

## 4. Testing routine
1. Turn on VoiceOver (iOS) or TalkBack (Android) from the device accessibility settings.
2. Swipe through the page linearly: every control announced with name, role and state.
3. Double-tap each control; perform each custom action via its alternative.
4. Check modals trap the swipe order and that hidden content isn't reachable.

## Verify
- [ ] Every gesture-driven action completable with VoiceOver and TalkBack using standard gestures only; no passthrough-only features.

## Checked

2026-10-28. Confirmed in the W3C Understanding SC 2.5.1 and Mobile Accessibility Mapping pages: SC 2.5.1 pointer gestures, SC 2.5.7 dragging movements, SC 1.4.4 resize text and that restrictive user-scalable / maximum-scale viewport values block zoom. Removed: the synthetic-click, passthrough-gesture and role=slider adjustment claims, the touch-action bullet, platform-specific settings paths and the TalkBack volume-key claim.

Method: documentation only; no commands were run.
