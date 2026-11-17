---
id: computing-software.systems-network-administration.backup-and-recovery.sql-server-tde-certificate-backup
name: sql-server-tde-certificate-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [tde-certificate-backup, sql-server, transparent-data-encryption, database-master-key, database-backup, key-management]
level: advanced
status: docs-checked
description: "Back up and restore SQL Server TDE certificates with private keys and the master key, so encrypted databases restore on another server."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-certificate-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/move-a-tde-protected-database-to-another-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TDE certificate backup

**Goal:** a TDE-protected database can be restored on any server, years later.

## What protects what
The database encryption key (DEK) is a symmetric key secured by a certificate in the server's `master` database (or by an asymmetric key protected by an EKM module). The certificate should itself be protected by the database master key. If the certificate is unavailable, or you restore or attach the database on another server, you need backups of the certificate and its private key, or the database cannot be opened.

## Back up (immediately after enabling TDE)
```sql
USE master;
BACKUP CERTIFICATE TDE_Cert_2026 TO FILE = N'<vault-dir>\TDE_Cert_2026.cer'
  WITH PRIVATE KEY (FILE = N'<vault-dir>\TDE_Cert_2026.pvk',
                    ENCRYPTION BY PASSWORD = N'<long passphrase>');
```
- Private keys are saved in PVK format; encryption of the private key file is required. Its password need not match the database master key password.
- If the certificate's private key is encrypted by a password in the database, add `DECRYPTION BY PASSWORD`.
- Keep copies of both the certificate file and the private key file; you need both to recover the certificate.
- Also back up the database master key and any certificate in a contained system database. This is required when the database is in log shipping or database mirroring.
- SQL Server 2022 can back up certificates with private keys to PKCS #12 / PFX format.

## Restore on a new server
Copy the certificate and key files to the destination, then:
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = N'<new strong password>';
CREATE CERTIFICATE TDE_Cert_2026 FROM FILE = N'<keys-dir>\TDE_Cert_2026.cer'
  WITH PRIVATE KEY (FILE = N'<keys-dir>\TDE_Cert_2026.pvk', DECRYPTION BY PASSWORD = N'<passphrase>');
```
Then restore or attach the database. `CREATE CERTIFICATE` restores a backed-up certificate; `ALTER CERTIFICATE` restores a private key to an existing certificate.

## Gotchas
- A certificate past its expiry date can still encrypt and decrypt data with TDE.
- Availability groups: create the master key and certificates (or EKM asymmetric key) on all secondary replicas before creating the DEK on the primary.
- After removing the DEK, take a log backup then a fresh full backup of the decrypted database; keep the master key and certificate for restoring backups taken while encrypted.

## Verify
Restore last night's backup on an isolated test instance using only the stored certificate files and passphrase.

## Checked
2026-11-09. Confirmed against the three Microsoft Learn pages in sources: DEK/certificate/EKM relationship, immediate certificate and private key backup, PVK format and required encryption, separate password, DECRYPTION BY PASSWORD, CREATE/ALTER CERTIFICATE restore, PFX in SQL Server 2022, log shipping/mirroring backup requirement, expired certificate, availability group ordering, post-DEK-removal backups. Removed (not stated on the pages): the Service Master Key hierarchy, BACKUP MASTER KEY and BACKUP SERVICE MASTER KEY statements, error 33111, rotation advice, and Azure Key Vault guidance.
Method: documentation only; no commands were run.
