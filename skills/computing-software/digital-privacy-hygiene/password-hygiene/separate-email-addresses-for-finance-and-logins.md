---
id: computing-software.digital-privacy-hygiene.password-hygiene.separate-email-addresses-for-finance-and-logins
name: separate-email-addresses-for-finance-and-logins
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, email-compartmentalization, primary-email-security, email-aliases, phishing-reduction, unpublished-email, finance-email]
level: practitioner
status: draft
description: "Split email identities: a private address only for banks and critical logins, a public one for people, and aliases for shopping, so phishing to the public address is easy to spot."
sources:
  - "https://www.privacyguides.org/en/basics/email-security/"
  - "https://www.privacyguides.org/en/email-aliasing/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Separate email addresses for finance and logins

**Goal:** if your bank only ever emails an address nobody else knows, any "bank" email to
your public address is a phish by definition. Compartmentalising also limits what one
breach reveals.

## A simple three-tier layout
| Address | Used for | Who knows it |
|---|---|---|
| **Vault address** (unpublished) | Bank, brokerage, password manager, Apple/Google account recovery, registrar, carrier | Only those services |
| **Personal address** | Friends, family, work contacts | People |
| **Aliases** (one per site) | Shopping, newsletters, forums, apps | Each site its own |

The vault address can be a second account at the same provider or a custom-domain address
that's never published. Protect it with security keys.

## Migration
1. Create the vault address; enable strongest MFA.
2. Move tier-1 services to it one by one (bank profile settings > email).
3. Set the personal address to forward nothing from these services.
4. Check the personal address is no longer the recovery address for tier-1 accounts.

## Habit
Email from your "bank" arriving at your personal or alias address = phishing; delete or
report without opening links.

## Gotchas
- Don't forward the vault address into the personal inbox; that undoes the separation
  (read it on its own, or use a separate mail client profile).
- Some banks send to an address you can't change easily online; call them.

## Verify
- [ ] Tier-1 services all use the vault address.
- [ ] Vault address doesn't appear in a search of your name or in data broker results.
