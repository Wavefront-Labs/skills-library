---
id: computing-software.digital-privacy-hygiene.device-hardening.lock-screen-privacy-settings
name: lock-screen-privacy-settings
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, lock-screen-privacy, notifications, screen-lock, ios, android]
level: intro
status: docs-checked
description: "Stop the phone lock screen leaking message text and 2FA codes: hide notification previews on iPhone and Android, and review what Siri can show."
sources:
  - "https://ssd.eff.org/module/how-to-get-to-know-iphone-privacy-and-security-settings"
  - "https://ssd.eff.org/module/how-to-get-to-know-android-privacy-and-security-settings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock screen privacy settings

**Goal:** someone holding your locked phone cannot read your messages from the lock screen.

## iPhone
- By default, notifications are visible on the lock screen, so anyone near the phone could read incoming messages.
  Open Settings > Notifications > **Show Previews** and choose **When Unlocked** (previews only after unlock) or
  **Never** (EFF Surveillance Self-Defense).
- Settings > Siri (or Apple Intelligence & Siri): review what Siri can access. EFF notes apps can appear as
  widget suggestions and app text can show in Spotlight search.
- Lockdown Mode is an optional setting for high-risk people, not for everyone; EFF has a separate guide to decide
  whether you need it.

## Android
- Settings > Notifications > **Notifications on lock screen**, then turn off **Sensitive notifications**.
- What counts as sensitive is decided by each sending app, so this may not always hide what you want. If a
  notification must never reveal anything, turn that app's notifications off entirely (EFF).

## Gotchas
- Per-app notification settings can behave differently from the global choice; check messaging and banking apps.

## Verify
- [ ] Lock the phone, send yourself a message, and confirm the lock screen does not show its text.

## Checked
2026-11-01. Confirmed in EFF Surveillance Self-Defense, "How to Get to Know iPhone Privacy and Security Settings"
and "...Android...": Show Previews options, Siri review, Lockdown Mode, Notifications on lock screen and Sensitive
notifications caveats. Removed: Allow Access When Locked list, Medical ID, Pixel display/shortcut/Lockdown power
menu steps, Windows and macOS settings, auto-lock times, smartwatch note (not on the pages read).
Method: documentation only; no commands were run.
