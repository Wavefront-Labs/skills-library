---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-standard-daily-account
name: macos-standard-daily-account
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-standard-account, least-privilege, macos-users, admin-separation]
level: practitioner
status: draft
description: "Run daily work on a Mac as a standard user with a separate admin account, so malware and mistakes can't silently change the system."
sources:
  - "https://support.apple.com/guide/mac-help/set-up-users-guests-and-groups-mtusr001/mac"
  - "https://www.cisecurity.org/benchmark/apple_os"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Daily standard account on a Mac

**Goal:** an admin password prompt (with a different account name and password) stands between malware and the
system.

## Set up
1. System Settings > **Users & Groups** > Add User: create **Admin** type, e.g. `localadmin`, with a long unique
   password stored in your password manager.
2. Log out, log in as the new admin, confirm it works.
3. Back in Users & Groups, select your daily account > turn off **Allow this user to administer this computer**.
   Restart.

## Living with it
- Installing apps to /Applications, system updates and security settings prompt for the admin name and password.
  That prompt is the point: pause and ask why.
- App Store apps and most drag-installs still work; installers that need root will ask.
- `sudo` in Terminal no longer works from the daily account; use `su localadmin` then `sudo`, or log in as admin.
- FileVault: keep the daily user enabled to unlock the disk at boot (Users & Groups or `sudo fdesetup list`).

## Gotchas
- Don't sign the admin account into iCloud; keep it local and boring.
- Keep the Apple Account and Find My on the daily account.
- Touch ID can't approve admin prompts for a different account, so expect to type the password.
