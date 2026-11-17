---
id: computing-software.cybersecurity-defensive.authelia.storage-encryption-key-rotation
name: storage-encryption-key-rotation
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, storage-encryption, change-key, encryption-check, key-rotation, cli]
level: advanced
status: docs-checked
description: "Verify and rotate the Authelia storage encryption key with authelia storage encryption check and change-key, including the command-line connection flags."
sources:
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_encryption_check/
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_encryption_change-key/
  - https://www.authelia.com/configuration/storage/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The encryption key protects sensitive database values such as stored second factor secrets. Two CLI commands help you manage it.

Check that the configured key matches the data:

```bash
authelia storage encryption check --config /path/to/configuration.yml
authelia storage encryption check --verbose --config /path/to/configuration.yml
```

Without `--verbose` it validates the key; with it, every row of encrypted data is checked, which is the way to prove all data is intact.

Change the key:

```bash
authelia storage encryption change-key --config /path/to/configuration.yml \
  --new-encryption-key '<NEW_KEY>'
```

The current key comes from the configuration (or `--encryption-key`), and `--new-encryption-key` supplies the replacement. All encrypted data is re-encrypted with it.

These commands inherit database connection flags (`--encryption-key`, `--postgres.address`, `--postgres.password`, `--mysql.address` and friends), so they can run from a maintenance container with no configuration file. Prefer files and environment secrets so nothing sensitive lands in shell history.

Suggested sequence for a rotation (this ordering is practice, not from the pages): stop writers or take a database backup, run `check --verbose` with the old key, run `change-key`, update the configured key in every deployment, restart, then `check --verbose` again with the new key.

Check: the final verbose check passes and a user can still authenticate with TOTP.

## Checked

2026-11-08. Read in full: CLI pages for encryption check and change-key, storage introduction. Flags verified; rotation sequence labelled as practice.

Method: documentation only; no commands were run.
