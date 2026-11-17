---
id: computing-software.digital-privacy-hygiene.password-managers.browser-builtin-password-manager-assessment
name: browser-builtin-password-manager-assessment
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, browser-builtin-password-manager, google-password-manager, icloud-keychain, apple-passwords, firefox-password-manager, on-device-encryption, password-manager-selection]
level: intro
status: draft
description: "Decide when Google Password Manager, Apple Passwords or Firefox's built-in manager is good enough, and how to harden it (on-device encryption, primary password)."
sources:
  - "https://support.google.com/chrome/answer/13402890"
  - "https://support.apple.com/guide/iphone/use-passwords-iphe57d0a0b5/ios"
  - "https://support.mozilla.org/en-US/kb/use-primary-password-protect-stored-logins"
  - "https://www.privacyguides.org/en/passwords/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser built-in password managers

**Goal:** for someone who will never install a separate app, make the built-in
manager safe rather than talk them out of using any manager at all.

## When built-in is good enough
- One ecosystem (all Apple, or all Chrome/Android) and no need to share with someone
  on a different platform.
- Person is low-risk and the alternative is password reuse.

## When it isn't
- Mixed ecosystems (iPhone + Windows + Android partner): sync gaps push people back to
  reuse. Apple Passwords is available on Windows via iCloud for Windows, but it is
  clunkier than a cross-platform manager.
- Need secure notes, attachments, emergency access, or family sharing beyond what
  the platform offers.
- Locally, a Chromium browser profile that isn't protected by an OS-level login
  is readable by malware running as that user (infostealers target browser stores
  first).

## Hardening each one
**Google Password Manager (Chrome/Android)**
- `passwords.google.com` > Settings > **On-device encryption**: enables encryption with
  a key derived from your device screen lock so Google cannot read the passwords.
  Note the warning: lose all devices and the lock and you lose the passwords.
- Turn on **Password Checkup** and act on compromised/reused alerts.
- Protect the Google account itself with passkeys or security keys.

**Apple Passwords (iCloud Keychain)**
- Already end-to-end encrypted; ensure the Apple Account has 2FA and a strong
  device passcode (the passcode is part of the trust chain).
- Use the Passwords app's **Security** list for reused/weak/compromised entries.
- Shared Groups let you share a subset with family.

**Firefox**
- Settings > Privacy & Security > **Use a Primary Password**; without one, the
  `logins.json` and `key4.db` in the profile can be decrypted by anyone with file access.
- Firefox Monitor/alerts for breached sites.

## Gotchas
- A built-in manager tied to an account with SMS-only recovery is only as safe as
  that SIM; fix the account first.
- Exporting from built-ins produces plaintext CSV; handle per the migration skill.

## Verify
- [ ] The account that syncs the passwords has phishing-resistant MFA.
- [ ] On-device encryption (Google) or Primary Password (Firefox) is on.
- [ ] Password health report reviewed and zero reused passwords on email/bank.
