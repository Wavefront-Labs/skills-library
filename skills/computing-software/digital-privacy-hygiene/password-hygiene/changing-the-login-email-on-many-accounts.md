---
id: computing-software.digital-privacy-hygiene.password-hygiene.changing-the-login-email-on-many-accounts
name: changing-the-login-email-on-many-accounts
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, account-email-change, email-migration, account-lifecycle]
level: practitioner
status: draft
description: "Move dozens of accounts off an old or ISP email address in priority order, using the password manager as the inventory and keeping the old inbox alive."
sources:
  - "https://www.privacyguides.org/en/basics/account-creation/"
  - "https://ssd.eff.org/module/creating-strong-passwords"
  - "https://www.cisa.gov/secure-our-world"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Changing the login email on many accounts

**Goal:** retire an old address (ISP email, a breached account, a work address) without losing any account whose
recovery depends on it.

## Build the list
1. Password manager: filter/search all items whose username is the old address; export a list of item names.
2. Search the old inbox for "welcome", "verify your email", "password reset", "receipt", "statement".
3. Check SSO: sites where you used "Sign in with Google/Apple/Microsoft" for that account.

## Order
1. **Recovery roots first:** other email accounts, Apple/Google/Microsoft accounts, password manager, phone carrier.
2. **Money:** banks, cards, PayPal, tax, investments, crypto.
3. **Identity and government** portals.
4. Shopping, social, subscriptions. Delete accounts you no longer need instead of migrating them.

## Per account
- Settings > Account > Email; most sites send a code to the new address and a notice to the old one.
- Some sites (or banks) need a phone call or ID check; note them and batch them.
- Update the username in the password manager item and tag it `migrated`.
- If the account used the old email as username and won't change it, close it and recreate it.

## Keep the old inbox for a while
- Turn on forwarding from old to new (or keep checking) for at least a year; stragglers show up as renewals and
  annual notices.
- For ISP email, check the ISP's policy for keeping the mailbox after you leave; many delete it, which lets the
  address eventually be reassigned to someone who could reset your accounts.
- A custom domain prevents this problem next time.

## Verify
Search the vault for the old address: zero results except the old mailbox itself. Try a password reset on two
migrated accounts to confirm mail goes to the new address.
