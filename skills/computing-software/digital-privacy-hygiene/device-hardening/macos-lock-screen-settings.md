---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-lock-screen-settings
name: macos-lock-screen-settings
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-lock-screen, auto-lock, screen-lock]
level: practitioner
status: draft
description: "Lock a Mac quickly and automatically: require password immediately, display-off timers, hot corner or Ctrl-Cmd-Q, and login window options."
sources:
  - "https://support.apple.com/guide/mac-help/change-lock-screen-settings-mchl8f6deb3d/mac"
  - "https://support.apple.com/guide/mac-help/use-hot-corners-mchlp3000/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# macOS lock screen settings

**Goal:** a Mac left unattended locks fast and needs your password.

## System Settings > Lock Screen
| Setting | Set |
|---|---|
| Start Screen Saver when inactive | 5 minutes or less |
| Turn display off on battery when inactive | 2-5 minutes |
| Turn display off on power adapter when inactive | 10 minutes or less |
| Require password after screen saver begins or display is turned off | **Immediately** |
| Show large clock / message when locked | Optional: "If found call..." contact message |
| Login window shows | Name and password (doesn't reveal account list) |
| Show password hints | Off |

## Lock instantly
- **Ctrl+Cmd+Q**.
- Apple menu > Lock Screen.
- Hot corner: System Settings > Desktop & Dock > Hot Corners > choose a corner > **Lock Screen**.
- Touch ID key press on some keyboards (if configured).

## Automatic login
System Settings > Users & Groups > Automatically log in as: **Off** (it's disabled when FileVault is on).

## Apple Watch unlock
Convenient, but anyone who takes the Mac while you're near can wake it unlocked. Turn off in Touch ID & Password
for high-risk settings.

## Gotchas
- "Prevent automatic sleeping when the display is off" doesn't stop locking; the password requirement is tied to
  display off / screen saver.
- Caffeinate/Amphetamine-style apps can stop idle lock; check them.
