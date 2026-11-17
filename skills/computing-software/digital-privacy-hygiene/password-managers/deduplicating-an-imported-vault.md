---
id: computing-software.digital-privacy-hygiene.password-managers.deduplicating-an-imported-vault
name: deduplicating-an-imported-vault
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-deduplication, migration, duplicate-entries, csv-cleanup, vault-health, password-reuse]
level: practitioner
status: draft
description: "Clean a vault full of duplicates after importing from several browsers and old managers: find exact and near duplicates, keep the newest password, merge the rest."
sources:
  - "https://bitwarden.com/help/import-data/"
  - "https://support.1password.com/watchtower/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deduplicating an imported vault

**Goal:** after importing Chrome + Firefox + an old manager, you typically have 2-3
copies of many logins, some with outdated passwords. Cleaning this is what makes
autofill trustworthy.

## 1. Prefer cleaning before import
If you still have the CSVs (on an encrypted disk), combine them in a spreadsheet:
1. Normalise URL to the registrable domain (strip `https://`, `www.`, paths).
2. Sort by domain, then username.
3. For identical domain+username, keep the row with the newest password (cross-check:
   try it, or keep the one from the browser you used most recently).
4. Import the cleaned CSV only, then securely delete all CSVs.

## 2. Cleaning inside the vault
Most managers have no one-click dedupe (check current features; 1Password Watchtower
and Bitwarden's reports flag **reused passwords**, which surfaces many duplicates).
- Sort by name; duplicates sit together if named consistently.
- For each pair: keep one item, copy over any extra URI, TOTP secret, notes or
  history, then move the other to an `Archive/duplicates` folder (delete after a month).
- **KeePassXC**: identical-entry detection is limited; `keepassxc-cli` export to XML/CSV
  and the spreadsheet method works for big vaults.

## Deciding which password is current
- Last-modified/created date on the item.
- Password history field.
- When in doubt, log in with each; or reset the password and save the new one.

## Gotchas
- Same domain, different usernames are **not** duplicates (personal vs work).
- Mobile app entries (`androidapp://`) may duplicate web entries; merge the URIs into one item.
- Third-party "dedupe" scripts need your plaintext export; avoid unknown tools.

## Verify
- [ ] Searching your 20 most-used sites returns exactly one item each.
- [ ] Reused-password report count dropped to items that are genuinely shared logins.
