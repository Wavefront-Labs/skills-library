---
id: computing-software.digital-privacy-hygiene.password-managers.leaving-lastpass
name: leaving-lastpass
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, lastpass-migration, migration, vault-breach-lessons]
level: practitioner
status: draft
description: "Move off LastPass completely: export or direct-import, rescue attachments and shared folders, rotate exposed secrets, then delete the account."
sources:
  - "https://support.lastpass.com/s/document-item?language=en_US&bundleId=lastpass&topicId=LastPass/export-vault-items.html"
  - "https://bitwarden.com/help/import-from-lastpass/"
  - "https://support.1password.com/import-lastpass/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Leaving LastPass

**Goal:** a clean exit: everything moved, nothing left behind, and secrets exposed by the 2022 vault-backup theft
rotated.

## Export
- Direct import (preferred): Bitwarden and 1Password can sign in to LastPass and pull the vault.
- Or LastPass > Account options > Advanced > **Export** > LastPass CSV (needs master password, may require email
  verification). Save to an encrypted location.

## What doesn't come over
| Data | Fix |
|---|---|
| Attachments | Open each item with a paperclip and download manually |
| LastPass Authenticator TOTP | Export from the Authenticator app separately or re-enroll 2FA per site |
| Shared folders owned by others | Ask owners to share via the new manager |
| Form fills / credit cards | Check they appear as card/identity items |
| Password history | Not exported |

## Rotate
The 2022 theft took encrypted vaults with unencrypted URLs. Assume weak-master-password vaults may be cracked:
- Change passwords for email, banks, crypto, password manager master password.
- Move crypto seed phrases that were stored in secure notes to new wallets.
- Change 2FA secrets (re-enroll TOTP) stored there.

## Delete
After verifying the new vault on all devices: LastPass Account settings > Delete account. Remove the extension
from all browsers.

## Gotchas
- Very old LastPass accounts used low PBKDF2 iterations; prioritise rotation if you never upgraded.
- Delete the CSV securely afterwards.
