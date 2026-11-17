---
id: computing-software.digital-privacy-hygiene.device-hardening.inactivity-auto-reboot-on-phones
name: inactivity-auto-reboot-on-phones
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, inactivity-reboot, before-first-unlock, grapheneos, ios, android, auto-restart]
level: practitioner
status: docs-checked
description: "Configure GrapheneOS auto-reboot after being locked, and use manual reboots elsewhere, so a lost or seized phone returns to its locked before-first-unlock state."
sources:
  - "https://grapheneos.org/features"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://source.android.com/docs/security/features/encryption/file-based"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inactivity auto-reboot on phones

**Goal:** a phone that has not been unlocked for a while reboots itself, putting data at rest
again (keys out of memory) so an attacker cannot just keep it powered and wait for an exploit.

## GrapheneOS
- It has an auto-reboot feature: a countdown starts each time the device is locked, and the
  device reboots if no successful unlock happens before it reaches zero. Unlocking any
  profile cancels the timer, not just the Owner profile.
- The timer is 18 hours by default; it can be set between 10 minutes and 72 hours, or turned
  off. Find it in the Settings security section and set it deliberately.
- Choosing a value: the default suits a low-risk daily user; shorten it if the phone may be
  left unattended (hotel, locker) or you face higher risk. Very short timers mean the phone
  may reboot during a long meeting, and apps cannot receive until the next unlock.
- Logging out of user profiles also purges that profile's encryption keys from memory.

## Other platforms
- Stock iOS and Android: check the vendor's current documentation for any built-in
  inactivity restart behaviour, since it arrives with OS or services updates and is not
  documented in the sources here.
- Where no timer exists, reboot manually before travel, protests or handing the device over.

## Gotchas
- The timer counts from the last lock without a successful unlock, so leaving the screen on
  does not help.
- Rebooting does nothing useful if the passcode is weak.

## Verify
- [ ] OS fully updated.
- [ ] GrapheneOS auto-reboot set to a value you chose.

## Checked
2026-11-01. Confirmed on the GrapheneOS features page: countdown on lock, cancelled by any
unlock, 18 hour default, 10 minute to 72 hour range, profile logout purging keys. Removed
(not confirmed in the sources): iOS 72-hour and Android 3-day behaviour, Samsung auto
restart, exact settings path, and a numeric recommendation range.
Method: documentation only; no commands were run.
