---
id: computing-software.systems-network-administration.backup-and-recovery.rotating-backup-encryption-keys
name: rotating-backup-encryption-keys
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-key-rotation, key-rotation, backup-encryption, restic-key, kms, password-rotation]
level: advanced
status: docs-checked
description: "Rotate backup encryption passwords and keys without losing access to older restore points: restic key add and remove, AWS KMS key rotation, and record keeping."
sources:
  - https://restic.readthedocs.io/en/stable/070_encryption.html
  - https://restic.readthedocs.io/en/stable/100_references.html
  - https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Rotating backup keys and passwords

**Goal:** limit exposure from leaked or departing-staff-known secrets while keeping every retained restore point restorable.

## Principle
Rotation affects new data; old restore points can stay encrypted with the old key until they expire. Keep old keys and passwords escrowed for at least the longest retention (including GFS, tape and archive copies). For any other backup product, read its documentation on whether changing a job password re-encrypts existing files.

## restic
restic allows multiple access keys (passwords) per repository, managed with the `key` command (`list`, `add`, `remove`, `passwd`). The key in use is marked with an asterisk in `key list`.
```bash
restic -r <repo> key list
restic -r <repo> key add               # new password
restic -r <repo> key remove <old-id>   # after confirming the new one works
```
This rotates **access passwords**, not the master key. restic's reference notes that a password change does not help if an attacker already has the local encryption key, because that gives access to the master key. Changing the master key currently means the `copy` command, which moves data into a new repository with a new master key, or starting a completely new repository and backup.

## AWS KMS
- Automatic rotation is optional for customer managed keys. If you do not specify `RotationPeriodInDays` when enabling it, the default is 365 days. On-demand rotation is also available.
- When you decrypt, KMS automatically uses the same key material version that encrypted the ciphertext, so old data stays readable after rotation.
- Asymmetric keys, HMAC keys and keys in custom key stores can only be rotated manually (create a new KMS key and repoint aliases or applications).
- Rotation history: the `GetKeyRotationStatus` and `ListKeyRotations` operations, and the KMS console.
- Never delete or disable a key while data encrypted with it is retained.

## Procedure
1. Generate the new secret in the vault; escrow copies (two people, offline).
2. Apply to jobs or repos.
3. Run a backup and a test restore with the new secret.
4. Test restore of an old restore point with the old secret.
5. Schedule retirement of the old secret after the last dependent restore point expires.

## Verify
Restore tests succeed for both the newest and oldest retained restore points, and the key register lists every secret still needed.

## Checked

2026-11-09. Confirmed against restic "Encryption" (key list/add/remove/passwd, asterisk marker), restic "References" (master key, password change, copy) and AWS KMS "Rotate KMS keys" (365-day default, optional automatic and on-demand rotation, decrypt uses original key material version, manual rotation for asymmetric/HMAC/custom key store keys, GetKeyRotationStatus, ListKeyRotations). Removed: Veeam Password Manager behaviour and Azure Key Vault claims (no cited source), the "yearly" wording for customer managed keys, and the "never disable a key" claim kept only as advice.

Method: documentation only; no commands were run.
