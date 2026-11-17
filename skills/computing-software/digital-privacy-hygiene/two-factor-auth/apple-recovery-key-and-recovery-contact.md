---
id: computing-software.digital-privacy-hygiene.two-factor-auth.apple-recovery-key-and-recovery-contact
name: apple-recovery-key-and-recovery-contact
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, apple-recovery-key, apple-recovery-contact, recovery-codes, apple-account, account-recovery, advanced-data-protection, icloud]
level: practitioner
status: docs-checked
description: "Set up an Apple Account recovery contact and/or 28-character recovery key, understand that the key turns off Apple's standard recovery, and store it safely."
sources:
  - "https://support.apple.com/en-us/109345"
  - "https://support.apple.com/en-us/102641"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apple recovery key and recovery contact

**Goal:** get back into your Apple Account (and end-to-end encrypted iCloud data) after
forgetting the password or losing devices.

## Recovery contact
- Someone you know and trust, such as family or a close friend. You can add up to five.
  They can give you a six-digit recovery code (in person or by phone) during recovery;
  they get no access to your account. Apple does not know who your contacts are, so
  remember them yourself.
- Requirements: all your Apple devices on iOS 15, iPadOS 15 or macOS Monterey 12 or later,
  the contact has such a device too, both have iMessage on, and both are over 13 (age
  varies by country or region).
- iPhone: Settings > your name > Sign-In & Security > Recovery Contacts > Add Recovery
  Contact. A Family Sharing member is added automatically; anyone else must accept the
  invite in Messages. Mac: System Settings > your name > Sign-In & Security.
- With no contact you can still do full account recovery, which can take longer.

## Recovery key
- An optional 28-character code. It is used with a trusted phone number and an Apple
  device to reset your password, and can help access end-to-end encrypted iCloud data
  under Advanced Data Protection.
- **Setting one turns off Apple's standard account recovery.** Lose the key and you can be
  locked out of the account permanently, and Apple cannot give you the key back.
- Needs iOS 14, iPadOS 14 or macOS Big Sur or later. Set up: Settings > your name >
  Sign-in & Security > Recovery Key > Continue; write it down and confirm it. To make a new
  key, use Replace Recovery Key; to go back to standard recovery, Remove Recovery Key.
- You may be asked for the key when changing account details, for example adding a new
  trusted phone number.

## Advanced Data Protection
If you use ADP you are prompted to choose a recovery contact or a recovery key to access
your encrypted iCloud data on a new device ("Some iCloud data isn't syncing").

## Storage
Print or write the key and keep it in a safe place, ideally in more than one place; you
can give a copy to a trusted family member. Do **not** store it in Apple's Passwords app,
iCloud Photos, Notes or iCloud Drive, because you cannot open those if you lose the
account.

## Verify
- [ ] Recovery Contacts or Recovery Key shows set up in Sign-In & Security.
- [ ] The printed key is readable and stored in two places, none of them in iCloud.

## Checked
Checked 2026-11-08 against Apple Support 109345 (recovery key) and 102641 (recovery
contact). Removed: the choice table, the "Account Recovery" menu name, and the
high-risk advice, which the pages do not state.

Method: docs-only read of cited pages, 2026-11-08
