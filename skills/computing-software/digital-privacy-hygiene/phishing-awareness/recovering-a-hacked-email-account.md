---
id: computing-software.digital-privacy-hygiene.phishing-awareness.recovering-a-hacked-email-account
name: recovering-a-hacked-email-account
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, hacked-email-recovery, account-takeover-recovery, email-forwarding-rules]
level: practitioner
status: draft
description: "Recover a hacked Gmail, Outlook, iCloud or Yahoo account with official recovery flows, then evict the attacker: rules, delegates, apps, recovery info."
sources:
  - "https://support.google.com/accounts/answer/6294825"
  - "https://support.microsoft.com/account-billing/how-to-recover-a-hacked-or-compromised-microsoft-account-24ca907d-bcd3-3d0d-d8ac-08a0f64fbf2c"
  - "https://support.apple.com/en-us/102656"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Recovering a hacked email account

**Goal:** get back in through official channels and remove every way the attacker kept access.

## Recover
| Provider | Route |
|---|---|
| Gmail | g.co/recover; answer from a device and location you've used before |
| Outlook/Microsoft | account.live.com/acsr recovery form (if the password was changed); recovery code if you have it |
| iCloud | iforgot.apple.com; account recovery wait period if needed |
| Yahoo | Sign-in helper |
Avoid "account recovery services" found via search or social media; they're scams.

## Evict the attacker (once back in)
1. New strong password; sign out of all sessions/devices.
2. **Recovery phone/email**: remove anything you don't own.
3. **2FA**: remove attacker-added methods; add a passkey or security key.
4. **Forwarding** and POP/IMAP settings: remove unknown forwarding addresses.
5. **Filters/rules**: delete rules that forward, archive or delete mail (attackers hide security alerts).
6. **Delegates** and **app passwords**; **third-party app access** (OAuth): remove unknowns.
7. **Signature/auto-reply**: check for planted links.

## Then
- Check sent mail and deleted items for what they did; warn contacts if they sent scams.
- Reset passwords for accounts that use this email for recovery, starting with financial ones.
- Look at the password manager: if the email password was reused, rotate everywhere.

## Gotchas
- If you can't recover, set up a new address and move accounts to it; notify contacts of the old address being
  compromised.
