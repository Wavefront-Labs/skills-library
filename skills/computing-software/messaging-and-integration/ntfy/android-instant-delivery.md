---
id: computing-software.messaging-and-integration.ntfy.android-instant-delivery
name: android-instant-delivery
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, android, instant-delivery, foreground-service, fcm]
level: practitioner
status: docs-checked
description: "How the ntfy Android app delivers notifications: instant delivery foreground service, Firebase on Google Play, F-Droid behaviour, and battery."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android delivery modes

## Variants

Available on Google Play, F-Droid and as APKs from GitHub Releases. Play and F-Droid builds are largely identical, except F-Droid does not use Firebase. iOS is App Store only.

## Instant delivery

A foreground service with a permanent notification keeps a connection to the server so messages arrive even in doze mode. To turn it off, long-press the foreground notification, open its settings, and switch off "Subscription Service". Without instant delivery, messages can be delayed by minutes or hours.

## Firebase (FCM)

- Only the Google Play build uses FCM, and only for `ntfy.sh`.
- Self-hosted servers never use it; the F-Droid build never does.
- F-Droid: instant delivery is always on, with no option to disable it, and the UI hides mentions of it.

## Battery

Per the FAQ, on ntfy.sh without instant delivery the app adds no battery use. A constant connection (self-hosted, instant delivery, F-Droid) used about 0-1% over 17 hours on the author's phone.

## Checked

2026-11-04. Confirmed against the ntfy phone page (variants, instant delivery, Firebase scope, F-Droid note) and the FAQ (battery figure). Removed: a gotcha about self-hosted Play users and the Verify step, neither stated on the pages.
Method: documentation only; no commands were run.
