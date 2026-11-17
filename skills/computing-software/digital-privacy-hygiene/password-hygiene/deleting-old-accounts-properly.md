---
id: computing-software.digital-privacy-hygiene.password-hygiene.deleting-old-accounts-properly
name: deleting-old-accounts-properly
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, delete-old-accounts, account-deletion, justdeleteme, data-download, right-to-erasure, gdpr, ccpa, account-minimization]
level: intro
status: draft
description: "Delete unused online accounts properly: export what you need, scrub data first where deletion is fake, use the real deletion path or a GDPR/CCPA request, and confirm."
sources:
  - "https://www.privacyguides.org/en/basics/account-deletion/"
  - "https://justdeleteme.xyz/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deleting old accounts properly

**Goal:** fewer accounts = fewer breaches with your data and fewer takeover targets.

## Procedure per account
1. **Export** anything you want (photos, purchase history, invoices).
2. **Find the deletion path**: account settings ("Close account", "Delete account"), or
   JustDeleteMe's direct links and difficulty ratings.
3. If only "deactivate" exists, **scrub first**: replace name, address, phone, birthday,
   profile photo with blanks or placeholders; delete stored payment cards; then deactivate.
4. If no path: email the privacy/DPO contact with a **deletion request** citing GDPR
   Article 17 (EU/UK) or CCPA/CPRA (California) or your local law; keep the reply.
5. **Unlink SSO**: remove the app from Google/Apple/Facebook connections afterwards.
6. Move the vault item to Archive with the deletion date (don't delete the item for a while;
   you may need to prove ownership if the account reappears).

## Special cases
- Old email accounts: don't delete if accounts still reset to them, and some providers
  recycle deleted addresses (someone else gets your address). Prefer securing and keeping
  with forwarding off.
- Accounts with money (gift balances, crypto, airline miles): withdraw first.
- Sites with "can't delete" policies: scrub data, set a random password, remove 2FA phone.

## Verify
- [ ] Login attempt after the stated grace period fails (account gone).
- [ ] SSO connection removed; vault item archived with date.
