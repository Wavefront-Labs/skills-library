---
id: computing-software.digital-privacy-hygiene.device-hardening.locked-notes-on-phones
name: locked-notes-on-phones
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, locked-notes, apple-notes, samsung-notes, mobile-privacy]
level: practitioner
status: draft
description: "Lock sensitive notes in Apple Notes or Samsung Notes with a passcode or separate password, understand what stays visible, and pick alternatives."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://www.samsung.com/us/support/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Locked notes on phones

**Goal:** keep a few sensitive notes (door codes, medical info, recovery hints) from anyone who picks up the unlocked
phone.

## Apple Notes
1. Settings > Apps > Notes > **Password**: choose **Use device passcode** (simplest) or a separate notes password
   (cannot be recovered if forgotten; existing notes become inaccessible).
2. In a note: share/more menu > **Lock**. Unlock with Face ID/Touch ID or the password.
3. Locked notes are end-to-end encrypted in iCloud. Notes on Google or Exchange accounts cannot be locked.

What stays visible: the note **title** (first line) in the list, and the date. Put nothing sensitive in the first
line.

## Samsung Notes
Note menu > **Lock**; set a password, add biometrics. Locked notes sync to Samsung Cloud; check your account security.

## Google Keep
No lock feature. Use Android Private Space (Android 15) or a password manager secure note instead.

## Better place for secrets
Passwords, recovery codes and card numbers belong in the password manager (secure notes), not a notes app. Use locked
notes for semi-sensitive things you need quickly.

## Gotchas
- Locking a note doesn't remove earlier copies in backups or shared versions; delete the old note and empty
  Recently Deleted.
- Shared notes cannot be locked.
