---
id: computing-software.digital-privacy-hygiene.password-managers.lastpass-breach-lessons-for-vault-users
name: lastpass-breach-lessons-for-vault-users
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-breach-lessons, lastpass, vault-theft, pbkdf2-iterations, unencrypted-metadata, credential-rotation, crypto-seed-theft, breach-response]
level: practitioner
status: draft
description: "What to do when your password manager's encrypted vaults are stolen: assess exposure (KDF, metadata), and rotate in priority order, using the LastPass 2022 case."
sources:
  - "https://blog.lastpass.com/posts/notice-of-recent-security-incident"
  - "https://www.privacyguides.org/en/passwords/"
  - "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lessons from a vault provider breach

**Goal:** know exactly how exposed you are when a provider loses encrypted vault
copies, and respond proportionately rather than panic or ignore it.

## What happened in the reference case
In the LastPass incidents disclosed in 2022, attackers obtained backups of customer
vaults. Passwords and notes were encrypted, but **site URLs and some metadata were
not**, and many older accounts still had very low **PBKDF2 iteration counts** (some
as low as 1 or 5,000) because the default had been raised over time without
migrating existing accounts. Researchers later linked thefts of cryptocurrency to
cracked vaults whose owners stored seed phrases in secure notes.

## The exposure equation
Offline cracking cost per guess ~ KDF cost. Your exposure depends on:
1. **Master password entropy**: a 6-word diceware phrase (~77 bits) is out of reach
   even at low iteration counts; an 8-character human password is not.
2. **KDF iterations at the time of theft**: changing them now doesn't protect the
   stolen copy.
3. **What was in the vault**: seed phrases and recovery codes are instantly monetisable.
4. **Unencrypted metadata**: the URL list tells an attacker which vaults to crack
   first (crypto exchanges, high-value employers).

## Response playbook
1. **Assume the stolen vault will be cracked if** the master password was under
   ~12 random characters or reused, or iterations were below ~100,000.
2. Rotate in this order: crypto wallets (move funds to a new seed, don't just change a
   password), email accounts, financial accounts, password manager-stored recovery
   codes and TOTP seeds, then everything else.
3. Re-enroll TOTP for accounts whose seeds were in the vault (the seed itself is
   compromised, not just the password).
4. Move to a provider with stronger defaults, or stay and raise KDF settings; either way
   use a new master password.
5. Revoke sessions and review email forwarding rules on the important accounts (see
   `computing-software.digital-privacy-hygiene.password-hygiene.account-security-audit-and-breach-response`).

## Prevent the next one
- Never store crypto seed phrases in an online vault; use paper/metal offline.
- Check your KDF after every provider announcement; old accounts lag defaults.

## Verify
- [ ] Every high-value credential that existed at breach time has been rotated.
- [ ] TOTP seeds stored in the breached vault are re-enrolled.
- [ ] No seed phrase remains in any cloud vault.
