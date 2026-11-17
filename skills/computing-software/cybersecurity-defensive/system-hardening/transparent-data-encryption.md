---
id: computing-software.cybersecurity-defensive.system-hardening.transparent-data-encryption
name: transparent-data-encryption
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-hardening, transparent-data-encryption, tde, encryption-at-rest, key-management, sql-server-tde, backup-encryption]
level: practitioner
status: docs-checked
description: "Enable SQL Server transparent data encryption, back up the certificate and private key, check encryption state, and understand what TDE does not protect."
sources: ["https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transparent data encryption

**Goal:** SQL Server data files, logs and backups are encrypted at rest with keys you can recover, without app changes.

## SQL Server
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<strong>';
CREATE CERTIFICATE TDECert WITH SUBJECT = 'TDE certificate';
-- immediately back up the certificate and its private key (BACKUP CERTIFICATE) to a secure off-server location
USE AppDb;
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256 ENCRYPTION BY SERVER CERTIFICATE TDECert;
ALTER DATABASE AppDb SET ENCRYPTION ON;
SELECT * FROM sys.dm_database_encryption_keys WHERE encryption_state = 3;  -- 3 = encrypted
```
- The database encryption key (DEK) is a symmetric key protected by a certificate in `master` or by an asymmetric key held by an EKM module.
- Backup files of TDE databases are encrypted with the DEK, so restoring needs the certificate. Without the certificate and private key you cannot open the database on another server: data loss.
- `tempdb` is encrypted automatically once any user database uses TDE; `master`, `model` and `msdb` cannot be TDE-encrypted.
- Keep the certificate even after disabling TDE (parts of the log may stay protected). Never drop it from `master` while a database uses it.
- Encryption runs as a background scan; use the DMV for state. Maintenance and some operations are blocked while it runs.
- FILESTREAM data is not encrypted by TDE.

## What TDE does not do
- It protects data and log files at rest (stolen drives or backup tapes), not data in transit: use encrypted connections for that.
- Replication does not carry data encrypted; enable TDE separately on distribution and subscriber databases.

## Gotchas
- Restoring a TDE backup on another server fails without the certificate: test DR.
- An expired certificate can still be used by TDE, but rotate per your key policy.
- Availability groups: create the master key and certificate on all secondary replicas before creating the DEK on the primary.

## Verify
- [ ] `encryption_state = 3` for all in-scope databases.
- [ ] A restore test on a separate server using the backed-up certificate succeeds.
- [ ] `pvt_key_last_backup_date` is not NULL for each TDE certificate (join `sys.certificates` to `sys.dm_database_encryption_keys`).

## Checked
2026-11-01. Confirmed in Microsoft Learn "Transparent Data Encryption (TDE)": the key steps, AES_256 and `ALTER DATABASE ... SET ENCRYPTION ON`, certificate and private key backup, restore needing the certificate, `encryption_state` value 3, tempdb behaviour, system databases excluded, EKM protector, expired certificates still usable, FILESTREAM, replication, availability group order, `pvt_key_last_backup_date`, no encryption across communication channels.
Removed: Oracle, RDS, Cloud SQL and Azure managed-database sections, PCI DSS reference, backup compression and MAXTRANSFERSIZE claim, key-rotation statement, Azure Key Vault and Always Encrypted advice, and the claim about DBAs and SQL injection.
Method: documentation only; no commands were run.
