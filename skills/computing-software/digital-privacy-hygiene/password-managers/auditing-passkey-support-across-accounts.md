---
id: computing-software.digital-privacy-hygiene.password-managers.auditing-passkey-support-across-accounts
name: auditing-passkey-support-across-accounts
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, passkey-inventory, passkeys, account-inventory]
level: practitioner
status: draft
description: "Inventory which of your accounts support passkeys, which already have one and where it's stored, then plan enrolment for the high-value ones first."
sources:
  - "https://passkeys.directory/"
  - "https://bitwarden.com/help/storing-passkeys/"
  - "https://support.1password.com/watchtower/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Auditing passkey support across accounts

**Goal:** a list of accounts with passkey status, so you enrol deliberately rather than one prompt at a time.

## Sources of truth
- **passkeys.directory** (community list of sites supporting passkeys, with sign-in vs MFA use).
- **1Password Watchtower:** "Passkeys available" flags items whose site supports passkeys.
- **Bitwarden:** login items that hold a passkey show a passkey field and created date; search the vault for
  items with a passkey via the item view.
- Platform lists: iCloud Passwords app, Google Password Manager (passwords.google.com), Windows Settings >
  Accounts > Passkeys.

## Build the table
| Account | Supports passkey? | Passkey exists? | Stored in | Password still active? | Hardware key too? |
Start with the top 15 accounts (email, password manager, Apple/Google/Microsoft, bank, registrar, social,
work SSO).

## Enrolment order
1. Accounts that allow passkey **instead of** SMS MFA (biggest security gain).
2. Email and identity providers.
3. Shopping/social for convenience.

## Clean-up
- Duplicate passkeys across providers: decide which to keep and delete the other at the site's security
  settings and in the provider.
- Note sites where the passkey only replaces the password but SMS remains a fallback; remove SMS if allowed.

## Gotchas
- passkeys.directory isn't exhaustive; check the site's security settings page.
- Some sites accept passkeys only on certain platforms (e.g. mobile app only).
