---
id: computing-software.digital-privacy-hygiene.password-managers.changing-master-password-and-rotating-encryption-key
name: changing-master-password-and-rotating-encryption-key
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, master-password-change, encryption-key-rotation, account-encryption-key, bitwarden, 1password-secret-key, keepassxc, kdf]
level: practitioner
status: draft
description: "Change a vault master password safely, and rotate the underlying encryption key when the old password or a device may be compromised, without breaking sync."
sources:
  - "https://bitwarden.com/help/master-password/"
  - "https://bitwarden.com/help/account-encryption-key/"
  - "https://support.1password.com/secret-key/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Changing the master password and rotating keys

**Goal:** know the difference between changing the password that wraps your vault
key and changing the key itself, and do the right one.

## Why it matters
Most managers encrypt your vault with a random **account encryption key**, which is
itself encrypted ("wrapped") by a key derived from your master password. Changing
only the master password re-wraps the same vault key. Anyone who already captured
the old wrapped key + old password, or the vault key from memory, can still decrypt.

## When to do which
| Trigger | Action |
|---|---|
| Routine strengthening, no suspicion | Change master password |
| Master password typed on a possibly keylogged machine | Change password **and rotate key** |
| Lost an unlocked device or suspect malware | Rotate key, then rotate high-value site passwords |
| Provider breach of encrypted vaults | New password + key rotation; still rotate site passwords (stolen copy uses old key) |

## Bitwarden
1. Export an encrypted backup first.
2. Web vault > Settings > Security > Master password. Tick **Also rotate my account's
   encryption key** when needed.
3. Key rotation re-encrypts every item; all other sessions are logged out. Log in to
   each device again. Old exports encrypted with the account key will no longer
   import (password-protected exports still work with their own password).

## 1Password
Change the account password in the account profile. If the Secret Key may be exposed,
use "Regenerate Secret Key" and print a new Emergency Kit; destroy the old kit.

## KeePassXC
Database > Database Security > change password/key file. The `.kdbx` is re-encrypted
on save; **old copies in backups and sync conflict files still open with the old
password**, so delete or re-encrypt them if the old password is compromised.

## Gotchas
- Never rotate while a device is mid-sync with unsaved local edits; sync first.
- Emergency access grants and organisation memberships may need re-confirmation after
  key rotation; check them.

## Verify
- [ ] All devices re-authenticated with the new password.
- [ ] Old emergency kit / paper copy destroyed.
- [ ] Backup made after the change and test-restored.
