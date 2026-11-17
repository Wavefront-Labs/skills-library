---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-dynamic-lock-and-lock-on-idle
name: windows-dynamic-lock-and-lock-on-idle
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, dynamic-lock, auto-lock, screen-lock]
level: practitioner
status: draft
description: "Make Windows lock itself when you walk away: Win+L habit, dynamic lock with a paired phone, idle sign-in requirement, and presence sensing."
sources:
  - "https://support.microsoft.com/windows/lock-your-windows-pc-automatically-when-you-step-away-from-it-0b8f6a2f-12e2-4e2f-8f91-d7d5de1ea8de"
  - "https://support.microsoft.com/windows/manage-presence-sensing-settings-in-windows-11"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Windows dynamic lock and lock-on-idle

**Goal:** an unattended Windows PC locks within minutes, even if you forget Win+L.

## Habit first
**Win+L** every time you stand up.

## Dynamic lock
1. Pair your phone over Bluetooth (Settings > Bluetooth & devices).
2. Settings > Accounts > Sign-in options > **Dynamic lock** > "Allow Windows to automatically lock your device when
   you're away".
Windows locks about 30 seconds after the phone drops out of Bluetooth range and the PC is idle.

## Idle lock
- Settings > Accounts > Sign-in options > "If you've been away, when should Windows require you to sign in again?"
  > **Every time**.
- Settings > System > Power & battery > Screen and sleep: turn off screen after 5 minutes (on battery and plugged in).
- Screen saver (search "screen saver"): wait 5 min, tick **On resume, display logon screen**. This is the
  idle-lock that works even if sleep is disabled.

## Presence sensing (supported hardware)
Settings > Privacy & security > Presence sensing / System > Power > "Turn off my screen when I leave" and "Wake my
device when I approach".

## Gotchas
- Dynamic lock depends on Bluetooth range (can be 10 m+ through walls); idle timeout is the backstop.
- Media playback or apps holding the screen awake can block idle locks; check `powercfg /requests`.
