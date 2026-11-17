---
id: computing-software.general-digital-literacy.email-clients.email-account-hacked
name: email-account-hacked
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, phishing, hacked-email-account, compromised-account, account-takeover, active-sessions]
level: practitioner
status: draft
description: "Recover a hacked Gmail, Outlook or iCloud email account: regain access, remove attacker rules and forwarding, secure linked accounts and warn contacts."
sources:
  - https://support.google.com/accounts
  - https://support.microsoft.com/en-us/account-billing
  - https://support.apple.com/en-us/102560
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Email account hacked

**Signs:** contacts get spam from you, password suddenly wrong, unknown sign-in alerts, sent items
you didn't write, missing emails.

## 1. Get back in
- Can sign in: change the password immediately (long, unique).
- Can't: use the official recovery page only: **g.co/recover** (Google), **account.live.com/acsr**
  (Microsoft recovery form), **iforgot.apple.com** (Apple). Use a device and network you've used
  before.

## 2. Kick the attacker out
- **Sign out everywhere**: Google Security › *Your devices* › sign out unknown; Microsoft account ›
  Security › *Sign out everywhere*; Apple Account › Devices › remove.
- Turn on 2-step verification with an authenticator app or passkey; regenerate backup codes.

## 3. Remove what they left behind (attackers do this on purpose)
- **Forwarding** addresses (Gmail Settings › Forwarding and POP/IMAP; Outlook › Mail › Forwarding).
- **Filters/rules** that delete or archive mail (bank, "security", your name).
- **Recovery phone/email** changed to theirs; **app passwords**; connected third-party apps
  (Google › Third-party connections; Microsoft › Apps and services).
- Signature, auto-reply, and *Send mail as* addresses.

## 4. Contain
- Change passwords on any account that reuses that password, starting with banks and other email.
- Email is the reset key for everything: check recent "password reset" emails in Trash.
- Tell contacts not to open recent messages from you.
- Scan the computer for malware if the cause is unclear.

## Verify
- [ ] Security page shows only your devices, 2SV on, no forwarding or unknown rules, recovery info
  yours.
