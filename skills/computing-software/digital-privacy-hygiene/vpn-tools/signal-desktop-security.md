---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-desktop-security
name: signal-desktop-security
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-desktop-security, signal-linked-devices, disk-encryption]
level: practitioner
status: draft
description: "Secure Signal Desktop: link and unlink safely, protect the local message database with OS encryption and keychain, and control notification exposure."
sources:
  - "https://support.signal.org/hc/en-us/articles/360007320551-Linked-Devices"
  - "https://support.signal.org/hc/en-us/articles/360008216551"
  - "https://ssd.eff.org/module/how-to-use-signal"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Signal Desktop security

**Goal:** the desktop copy of your Signal history isn't the weak point.

## Linking
Signal Desktop > scan the QR from the phone: Settings > Linked devices > Link new device. Optionally transfer
message history on link. Only link computers you control.

## What lives on the computer
Messages and attachments in a local encrypted database. Its key is protected with the OS credential store
(Keychain, Windows DPAPI, Linux secret service) in current versions, so anyone with your logged-in OS session can
still read it. Protect the computer:
- Full-disk encryption (BitLocker/FileVault/LUKS).
- Screen lock with short timeout; separate OS accounts for other people.
- Signal Desktop has no separate app PIN; the OS lock is the lock.

## Settings
- Settings > Notifications: show **name only** or **no name or content** to avoid message previews on screen.
- Disappearing messages apply to desktop too.
- Settings > Privacy > Clear history on this device if needed.

## Unlink when
Travelling with the laptop through borders, selling/repairing it, or if it's stolen: phone > Settings > Linked
devices > remove. Unlinked desktops delete local data on next launch; stolen ones may not launch, so assume data
on disk is exposed if the disk wasn't encrypted.

## Gotchas
- Linked devices go inactive after about 30 days without use and are unlinked.
- Backups of your home folder (Time Machine, cloud sync) include the Signal database.
