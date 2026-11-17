---
id: computing-software.digital-privacy-hygiene.two-factor-auth.registering-a-backup-security-key
name: registering-a-backup-security-key
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, backup-security-key, security-keys, yubikey, key-inventory, off-site-key, fido2, account-recovery]
level: practitioner
status: draft
description: "Register a second security key on every account, keep an inventory of where each key is enrolled, and handle sites that only accept one key."
sources:
  - "https://www.privacyguides.org/en/security-keys/"
  - "https://support.yubico.com/hc/en-us/articles/360013656800-Using-Your-U2F-YubiKey-with-Google-Accounts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Registering a backup security key

**Goal:** FIDO credentials can't be copied between keys (by design). The only backup is
a second key registered separately on every account.

## Procedure
1. Have both keys in hand. Label them physically (`A - keyring`, `B - home safe`).
2. For each account, in its security settings: Add security key > register **A**,
   name it `YubiKey A`; Add another > register **B**, name it `YubiKey B`.
3. Record the enrollment in an inventory (a secure note):
   `Google: A, B | GitHub: A, B, passkey-1Password | Bank X: A only (single-key site)`.
4. Move **B** to its storage place.

## Adding accounts later (B is off-site)
Options:
- Register with A and immediately add a non-key backup (recovery codes, passkey in
  password manager), and add a reminder to register B on next visit.
- Or keep B at home (not off-site) and a third key C off-site, enrolled quarterly.

## Sites that allow only one key
Some banks and older services accept a single key. Then: key + recovery codes stored
offline, or TOTP kept as backup method. Note it in the inventory.

## Lost key
Revoke it on every account using the inventory, register a replacement (see
`computing-software.digital-privacy-hygiene.two-factor-auth.hardware-security-key-deployment-at-scale`
for the lost-key response).

## Verify
- [ ] Each high-value account lists two keys.
- [ ] Logging in with B alone works for a sample of accounts.
