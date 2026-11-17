---
id: computing-software.messaging-and-integration.ntfy.known-issues-ios-safari
name: known-issues-ios-safari
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, known-issues, ios, safari, workarounds]
level: practitioner
status: docs-checked
description: "Documented ntfy known issues on iOS and Safari with their workarounds: refresh, missing notifications, New message, sounds, PWA crash."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/known-issues.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Known issues

The upstream list is incomplete; these are the documented ones.

1. **iOS app not refreshing the view** (#267): new notifications do not appear until you swipe down. The page blames the Notification Service Extension, SwiftUI and Core Data but says the cause is unclear. Workaround: manually swipe down to refresh.
2. **iOS not receiving notifications**:
   - Firebase/APNS flakiness: remove and re-add the subscription to force a re-subscribe.
   - Self-hosted: set `upstream-base-url: "https://ntfy.sh"` (not your own host) and make `base-url` exactly match the Default Server in the iOS app.
3. **iOS shows "New message" instead of content**: the iPhone cannot reach the self-hosted server. Make sure the phone and server are on the same network or the phone can reach the server, and turn on `log-level: debug` or `trace`.
4. **Safari plays no sound for web push**: Safari does not support sounds for web push and treats it all as silent; the page says this was to be fixed with iOS 17 / Safari 17 (2023).
5. **PWA on iOS crashes with an IndexedDB error** (#787) on resuming from the background. Cause is a WebKit bug. Workaround: reload the app.

The FAQ adds that the iOS app is bare bones and somewhat buggy.

## Checked

2026-11-04. Confirmed every item against the ntfy known issues page and the FAQ (iOS app bare bones and a little buggy). Corrected: the Safari sound issue was expected to be fixed in iOS 17 / Safari 17. Removed: the Verify step.
Method: documentation only; no commands were run.
