---
id: computing-software.systems-network-administration.backup-and-recovery.backup-encryption-key-escrow
name: backup-encryption-key-escrow
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-encryption, key-escrow, encryption-password, key-management, restic, disaster-recovery]
level: practitioner
status: docs-checked
description: "Encrypt backups without locking yourself out: restic repository keys, a second recovery key, a key inventory and an escrow test."
sources:
  - https://restic.readthedocs.io/en/stable/070_encryption.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Backup encryption keys and escrow

**Goal:** stolen backup media is useless to an attacker, while you can always decrypt your own backups, even after losing the backup server and the person who set it up.

## restic repository keys
The restic `key` command sets multiple access keys or passwords per repository. Its sub-commands are `list`, `add`, `remove` and `passwd` (changes a password).

```bash
restic -r /srv/restic-repo key list
restic -r /srv/restic-repo key add
```

`key list` shows ID, user, host and creation time for each key; the key currently in use is marked with an asterisk (*). `key add` asks for the repository password and then for the new key's password twice.

## Escrow procedure
1. Generate strong, long, random passwords per repository.
2. Store them in the enterprise password vault with access limited to the backup admin group, plus an offline escrow (sealed envelope or hardware token in a safe).
3. For restic, add a second key for recovery with `restic key add` and keep it offline, so one lost password does not lock you out of the repository.
4. Keep a key inventory recording which key protects which repository; never write the keys themselves in tickets or docs.
5. Test periodically: restore from an encrypted backup on a clean machine using only the escrowed secrets, which simulates losing the backup server.

## DR considerations
The password vault itself must be reachable in a disaster (offline copy or separate tenancy).

## Verify
Key inventory complete; the latest clean-machine decryption test succeeded using escrowed secrets only.

## Checked

2026-11-09. Confirmed against the restic "Encryption" page: multiple keys per repository, the `key` sub-commands list/add/remove/passwd, output columns and the asterisk marking the current key. Removed (not on the cited page): Veeam password loss protection, Bacula PKI, AWS Backup and Azure Backup key models, KMS account-compromise advice, rotation and deduplication claims, the "lose all passwords, lose the repo" statement and the yearly test interval. The escrow steps are procedure advice, not product facts.

Method: documentation only; no commands were run.
