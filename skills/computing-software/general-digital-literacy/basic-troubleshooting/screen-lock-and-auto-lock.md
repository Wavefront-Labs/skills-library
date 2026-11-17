---
id: computing-software.general-digital-literacy.basic-troubleshooting.screen-lock-and-auto-lock
name: screen-lock-and-auto-lock
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, accounts-signin, screen-lock, auto-lock, lock-screen, dynamic-lock]
level: intro
status: docs-checked
description: "Set a password requirement after screen saver or sleep on a Mac, and an Auto-Lock time and passcode on an iPhone, so nobody can use the device while you step away."
sources:
  - https://support.apple.com/en-au/guide/mac-help/mh11784/mac
  - https://support.apple.com/en-au/guide/iphone/iph14a867ae/ios
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock the screen and auto-lock

**Goal:** nobody can use your unlocked computer or phone while you step away.

## Mac
- Apple menu > System Settings > **Lock Screen** (scroll the sidebar if needed).
- *Require password after screen saver begins or display is turned off*: the Mac asks for the login password when it wakes, and you choose how long after the screen saver or sleep begins that is required.
- *Turn display off on battery when inactive* and *on power adapter when inactive* set the idle time before the screen saver starts.
- *Show message when locked* can show contact details for a lost Mac.

## iPhone
- Settings > Display & Brightness > **Auto-Lock**, then set a length of time. If the iPhone sits on the Home Screen with no action, the Auto-Lock time is halved.
- Passcode settings are under Settings > **Face ID & Passcode** on iPhones with Face ID.

## Other devices
Windows and Android steps changed between versions and are not covered here: check the vendor's help for your version.

## Verify
- [ ] Leave the device idle for the set time: it locks and asks for the password or passcode.

## Checked
2026-11-01. Confirmed: Apple "Change Lock Screen settings on Mac" (options and wording above); Apple iPhone User Guide "Set a passcode" (Auto-Lock path, halved time on the Home Screen, Face ID & Passcode). Removed: Windows shortcuts and Dynamic Lock, Android steps, Mac shortcut and Hot Corner, timer and PIN-length advice, notification-preview steps (no page read).
Method: documentation only; no commands were run.
