---
id: computing-software.digital-privacy-hygiene.two-factor-auth.aegis-authenticator-encrypted-vault
name: aegis-authenticator-encrypted-vault
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, aegis-authenticator, totp, authenticator-migration]
level: practitioner
status: docs-checked
description: "Set up Aegis Authenticator on Android with an encrypted vault, automatic backups, imports from other authenticator apps and a tested restore."
sources:
  - "https://getaegis.app/"
  - "https://github.com/beemdevelopment/Aegis"
  - "https://www.privacyguides.org/en/multi-factor-authentication/"
  - "https://github.com/beemdevelopment/Aegis/blob/master/docs/vault.md"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Aegis Authenticator with an encrypted vault

**Goal:** an open-source, offline TOTP app on Android whose secrets are encrypted at rest and backed up
automatically.

## What Aegis is
- Free, open-source (GPL-3.0) Android app for HOTP and TOTP codes, available from Google Play and F-Droid.
- Privacy Guides lists it as operating completely offline/locally, with an option to export tokens for backup.
- Android only. On iOS use another app, for example Ente Auth (Privacy Guides lists it), or the TOTP feature of your password
  manager.

## Install and secure
1. Install from F-Droid or Google Play.
2. The vault is stored as a file and can be kept in plain text or encrypted with a password. Choose password
   encryption. Biometric unlock (Android Keystore) can be added as a second credential.
3. Look in the app settings for screen capture prevention and tap to reveal.

## How the encryption works (vault.md)
- Vault contents: AES-256 in GCM mode with a random 256-bit master key.
- Password credential: key derived with scrypt (N 2^15, r 8, p 1).
- Each credential has its own slot holding a copy of the master key, so the master key is only as secure as the
  weakest credential (a weak password or an easily unlocked biometric slot).

## Backups, import and export
- Aegis supports automatic backups of the vault to a location of your choosing, and exports in plaintext or encrypted form.
  Prefer the encrypted export; delete any plaintext file after use.
- It can import from: 2FAS Authenticator, Authenticator Plus, Authy, andOTP, FreeOTP, FreeOTP+, Google Authenticator,
  Microsoft Authenticator, plain text, Steam, TOTP Authenticator and WinAuth. Root access is required for some of these.
- Menu names and backup-version options vary by release; find them in the app settings rather than from a script.

## Test restore (do this)
On a spare device or after reinstalling: import the backup into a fresh Aegis, enter its password, and confirm the codes
match the live app.

## Gotchas
- Forgetting the vault password makes encrypted backups useless. Store it in your password manager and paper kit.
- The vault format and security design are documented in `docs/vault.md` in the Aegis repository.

## Checked
Checked 2026-11-08 against getaegis.app, the Aegis README, Privacy Guides' MFA page and Aegis docs/vault.md. Removed:
settings menu paths, "keep 10 versions", Bitwarden and "plain otpauth URI" import claims, JSON/HTML export formats,
auto-lock option names and the Raivo remark, none of which the pages state.

Method: docs-only read of cited pages, 2026-11-08
