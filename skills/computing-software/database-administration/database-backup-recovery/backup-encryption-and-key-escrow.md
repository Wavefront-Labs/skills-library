---
id: computing-software.database-administration.database-backup-recovery.backup-encryption-and-key-escrow
name: backup-encryption-and-key-escrow
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, backup-key-management, backup-encryption, key-escrow, kms, backup-strategy]
level: practitioner
status: gated
description: "Encrypt database backups at rest and in transit, manage keys with a KMS or vault, escrow keys for disaster recovery, rotate them, and prove encrypted backups restore."
sources:
  - https://pgbackrest.org/user-guide.html#quickstart/configure-encryption
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-encryption
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup encryption and key escrow

**Goal:** stolen backup media is useless to an attacker, while you can always decrypt your own backups during a disaster, even when the primary site (and its key server) is gone.

## Encrypt
| Tool | How |
|---|---|
| pgBackRest | `repo1-cipher-type=aes-256-cbc` (the only non-`none` type; client-side), `repo1-cipher-pass` (from vault) |
| Barman / WAL-G | WAL-G libsodium or PGP keys; cloud bucket SSE-KMS (gated: unconfirmed, source is paywalled or blocked) |
| XtraBackup | `--encrypt` with `--encrypt-key-file` (confirm flags and algorithm names in the Percona docs for your version) (gated: unconfirmed, source is paywalled or blocked) |
| SQL Server | `BACKUP DATABASE ... WITH ENCRYPTION (ALGORITHM = AES_256, SERVER CERTIFICATE = BackupCert)` (2014+; algorithms AES 128/192/256 and Triple DES; not on Express or Web editions, which can still restore; needs a master key in `master` and a certificate) |
| Oracle RMAN | `CONFIGURE ENCRYPTION FOR DATABASE ON` with TDE keystore, or `SET ENCRYPTION ON IDENTIFIED BY ...` (gated: unconfirmed, source is paywalled or blocked) |
| mongodump / logical dumps | Pipe through `age`/`gpg` or write to SSE-KMS buckets |
| Object storage | SSE-KMS / CMEK plus bucket policy requiring encryption |

TDE-encrypted databases: physical backups contain encrypted pages, but logical dumps are plaintext; encrypt them separately.

## Key management
- Keys live in a KMS/HSM/vault (AWS KMS, Azure Key Vault, GCP KMS, HashiCorp Vault), never next to the backups.
- Separate duties: backup operators can write backups but not read keys; key custodians cannot delete backups.
- Rotation: new backups use the new key; keep old keys (disabled for encryption, enabled for decryption) for as long as backups encrypted with them are retained (cryptoperiod guidance: NIST SP 800-57; confirm specifics there).

## Escrow for disaster recovery
- Export keys or certificates (SQL Server: `BACKUP CERTIFICATE BackupCert TO FILE ... WITH PRIVATE KEY (ENCRYPTION BY PASSWORD = ...)`; Oracle wallet backups) to an offline escrow: split knowledge (two custodians), sealed storage or a second-region KMS with cross-region key replication.
- Document the recovery procedure for keys as part of the DR runbook.
- Without the certificate/key, a SQL Server encrypted backup cannot be restored (Microsoft says so explicitly). Restore needs the original certificate with the matching thumbprint, so do not renew or alter it; store its backup away from the backup files. Test on a clean server.

## Pitfalls
- Encrypting with a passphrase stored in the same repository or CI variable that has delete rights to backups.
- Deleting a KMS key (scheduled deletion) renders all dependent backups unrecoverable: protect keys with deletion locks and alerts.

## Verify
Quarterly: on an isolated host with only escrowed material, decrypt and restore the latest backup; record time and any missing steps.
