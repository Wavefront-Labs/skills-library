---
id: computing-software.collaboration-platform-administration.nextcloud.two-factor-providers-and-enforcement
name: two-factor-providers-and-enforcement
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [two-factor, 2fa, totp, backup-codes, enforcement]
level: practitioner
status: draft
description: "Enable Nextcloud 2FA providers (TOTP, notification, backup codes) and enforce 2FA system-wide or by group, including how selected and excluded groups combine."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/two_factor-auth.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: require a second factor safely.

Two things must happen: an admin enables at least one provider, and either the user activates 2FA or the admin enforces it.

Providers installed with Nextcloud (2FA is pluggable, more in the App Store):
- Two-Factor TOTP Provider: any RFC 6238 client app (the docs name Aegis and Google Authenticator). Disabled by default; enable under *Apps -> Disabled apps*.
- Two-Factor Authentication via Nextcloud notifications: a logged-in device is the second factor. Also disabled by default.
- Two-Factor Backup Codes: always enabled. Generates ten single-use codes for recovery when a device is stolen or broken.

Enforcement lives under *Administration Settings -> Security*. By default 2FA is optional. You can enforce it system-wide or for selected groups, and exclude groups.

Logic:
- No groups selected: 2FA is enforced for everyone except members of excluded groups.
- Groups selected: enforced for all their members. A user who is in both a selected and an excluded group is enforced, because selected wins.


Check: sign in as a test user in an enforced group and confirm you are walked through 2FA setup before reaching files.
