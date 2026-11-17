---
id: computing-software.software-engineering.mobile-development.screenshot-and-screen-recording-protection
name: screenshot-and-screen-recording-protection
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-security, flag-secure, screen-capture, task-switcher, uiscreen-captured, sensitive-screens, masvs-platform]
level: practitioner
status: draft
description: "Protect sensitive screens from capture and app-switcher previews: Android FLAG_SECURE, iOS capture detection and snapshot hiding, and the limits of both."
sources: ["https://developer.android.com/reference/android/view/WindowManager.LayoutParams#FLAG_SECURE", "https://developer.apple.com/documentation/uikit/uiscreen/1617812-iscaptured", "https://mas.owasp.org/MASVS/09-MASVS-PLATFORM/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screenshot and screen-recording protection

Relevant to MASVS-PLATFORM and MASVS-STORAGE: sensitive data can leak through screenshots, screen recording, and the task-switcher thumbnail.

## Android: FLAG_SECURE
```kotlin
window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)
// Compose: apply in the host Activity; clear the flag when leaving the sensitive screen
window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
```
Effect: blocks screenshots and screen recording of that window, blanks it in the recent-apps overview, and hides it from non-secure displays (casting). Android 14 added `setRecentsScreenshotEnabled(false)` for just the recents preview.

## iOS
iOS has no API to block user screenshots. Options:
- Detect recording/mirroring: `UIScreen.main.isCaptured` plus `UIScreen.capturedDidChangeNotification` (newer scene-based code reads `UIScene`/`UITraitCollection`-era properties; check current docs) and cover content when true.
- Observe `UIApplication.userDidTakeScreenshotNotification` to warn or log (after the fact).
- Hide content in the app switcher: in `sceneWillResignActive` / `applicationWillResignActive` overlay a blur or logo view and remove it on become active.
- A secure text-field layer trick is widely used to blank captures, but it is an undocumented workaround that may break across iOS versions.

## Gotchas
- FLAG_SECURE also disables legitimate accessibility screenshot tools and some assistive overlays; use it only for truly sensitive views.
- Cameras pointed at the screen defeat all of this; treat it as friction.
- Keyboards and autofill suggestions can cache sensitive text; use secure text entry fields.

Verify: on Android try a screenshot and a screen recording on the protected screen (expect a blocked message/black frame) and check the recents thumbnail; on iOS start a screen recording and confirm the overlay hides content.
