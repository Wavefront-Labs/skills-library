---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-notification-privacy
name: signal-notification-privacy
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-notification-privacy, signal, lock-screen-privacy, notifications]
level: practitioner
status: draft
description: "Stop Signal message text and sender names appearing on the lock screen and in OS notification history, on Android, iOS and desktop."
sources:
  - "https://support.signal.org/"
  - "https://support.apple.com/guide/iphone/change-notification-settings-iph7c3d96bab/ios"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Signal notification content privacy

**Goal:** end-to-end encryption is pointless if the message is readable on a locked screen or stored in a
notification log.

## Signal setting
Signal > Settings > **Notifications** > Show (Android) / Show (iOS):
- **Name, content and actions** (default)
- **Name only**
- **No name or content** (just "New message"): use this for high-risk situations.

Signal Desktop: Settings > Notifications > Notification content: same three choices.

## OS layer
- **iOS:** Settings > Notifications > Show Previews > When Unlocked (applies to all apps).
- **Android:** Settings > Notifications > Notifications on lock screen > "Show conversations, default and silent"
  vs "Hide silent" vs "Don't show"; set sensitive content hidden. Notification history (Android 11+) stores
  past notifications; turn it off if content shows.
- **Smartwatches** mirror notifications; check the watch app's privacy setting.

## Also consider
- iOS notification extension can decrypt messages in the background; that is normal and stays on device.
- Push notifications go via Apple/Google but contain no content; Signal fetches the message itself.
- Screen Lock (Settings > Privacy > Screen lock) needs device unlock to open Signal.
- Incognito keyboard on Android (Settings > Privacy) asks the keyboard not to learn what you type.

## Verify
Lock the phone and send yourself a message from a linked device: the lock screen should show only what you chose.
