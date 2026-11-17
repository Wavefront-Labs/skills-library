---
id: computing-software.digital-privacy-hygiene.password-hygiene.discovering-forgotten-accounts
name: discovering-forgotten-accounts
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, account-discovery, account-inventory, email-search, sign-in-with-google, have-i-been-pwned, forgotten-accounts, attack-surface]
level: practitioner
status: draft
description: "Build a complete list of accounts you've ever made by mining mailboxes, password stores, SSO connections and breach records, so forgotten accounts can be secured or deleted."
sources:
  - "https://www.privacyguides.org/en/basics/account-deletion/"
  - "https://haveibeenpwned.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discovering forgotten accounts

**Goal:** every forgotten account with an old reused password is a breach waiting to
be used against you. Find them.

## Sources to mine
1. **Password managers and browsers**: export lists of sites from every browser profile
   (old Chrome profiles, Firefox, Safari) and old managers.
2. **Mailbox search** (each email address you've used), queries such as:
   `"welcome to"`, `"verify your email"`, `"confirm your account"`, `"your account"`,
   `"password reset"`, `"thanks for signing up"`, `"unsubscribe"`. Gmail operators:
   `subject:(welcome OR verify OR confirm) older_than:1y`.
3. **SSO connections**: Google `myaccount.google.com/connections` ("Sign in with Google"),
   Apple Settings > [name] > Sign in with Apple, Facebook Apps and websites, Microsoft
   app permissions, GitHub authorised apps.
4. **Have I Been Pwned**: search each address; every listed breach is an account you had.
5. **Payment history**: card and PayPal statements show subscriptions and shops.
6. Phone: apps installed historically (App Store/Play purchase history).

## Record
One row per account: service, email used, login method (password/SSO), 2FA, keep/delete.
Put "keep" items into the vault; queue "delete" items for
`computing-software.digital-privacy-hygiene.password-hygiene.deleting-old-accounts-properly`.

## Gotchas
- Old email addresses (university, ISP addresses) may have lapsed; accounts tied to them
  can't be recovered by you but can by whoever gets that address. Change their email now.
- Don't log in to suspicious "your account" emails during the search; navigate directly.

## Verify
- [ ] Inventory covers all email addresses you've used.
- [ ] Each entry has a keep/delete decision.
