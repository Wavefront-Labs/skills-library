---
id: computing-software.digital-privacy-hygiene.two-factor-auth.enrolling-in-google-advanced-protection
name: enrolling-in-google-advanced-protection
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, google-advanced-protection, advanced-protection-program, account-hardening-programs, security-keys, passkeys, high-risk-users, journalists, account-recovery]
level: practitioner
status: docs-checked
description: "Enroll a high-risk Google account in Advanced Protection: passkey or security key sign-in, recovery trade-offs and which apps stop working."
sources:
  - "https://landing.google.com/advancedprotection/"
  - "https://support.google.com/accounts/answer/7539956"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Advanced Protection Program

**Goal:** give a likely-targeted person's Google account the strongest settings Google
offers, accepting less convenience.

## What it changes
- Sign-in requires a **passkey or security key**. If you choose a password instead of a
  passkey, you must use a security key as the second step.
- **Tighter account recovery**: with no account access, Google's recovery request
  "takes a few days" to verify it is you.
- Only Google apps and **verified third-party apps** can access sensitive data such as
  Gmail and Drive.
- **Stronger checks on downloads** in Chrome; you can send a suspicious file to be scanned.
- **App passwords are blocked**, and any existing app passwords are revoked at enrolment.
- It is free; you may need to buy security keys.

## Before enrolling
1. Add a recovery email and phone number to the account.
2. Turn on 2-Step Verification.
3. Have a passkey or FIDO-compliant security key ready. If using keys, Google recommends
   a primary key and at least one backup key.
4. Review what will break (below), then use "Get started" on the Advanced Protection page.

## Check first
- Mail clients that rely on app passwords stop working.
- Third-party apps that are not verified lose access to sensitive data.
- Google Workspace accounts: enrolment works only if the admin has enabled Advanced
  Protection; an admin cannot make enrolment mandatory.
- iPhone users: iCloud backups include signed-in Google sessions, passwords and passkeys,
  so Google recommends security keys on the iCloud account too.
- Android TV: remove the account and add it again, choosing set-up using a phone on the
  same Wi-Fi network.

## Gotchas
- If you lose a key and still have access: add the replacement under Security & sign-in >
  Passkeys and security keys, then remove the lost one. Without access, submit a
  recovery request and wait; when told, sign in and turn Advanced Protection on again.
- Carry your key whenever you might sign in on a new device, including when travelling.
- To leave: Security section > Advanced Protection Program > Unenroll. Do not do it under
  pressure from someone claiming to be from Google.

## Verify
- [ ] The Security section shows Advanced Protection on.
- [ ] A new browser sign-in needs the passkey or security key.

## Checked
Checked 2026-11-08 against the Google Advanced Protection landing page and the Advanced
Protection help page (answer 7539956). Removed: Android Advanced Protection link, being
signed out of other devices, the connections page URL, and "SMS and codes" wording not
stated on the pages.

Method: docs-only read of cited pages, 2026-11-08
