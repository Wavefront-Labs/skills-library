---
id: computing-software.database-administration.sql-server.transparent-data-encryption
name: transparent-data-encryption
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, sql-server-security, transparent-data-encryption, tde, encryption-at-rest, database-encryption-key, service-master-key, certificate-backup, byok, akv]
level: advanced
status: docs-checked
description: "Enable SQL Server TDE with a backed-up certificate, monitor the encryption scan, and restore or move TDE databases without losing the key."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/move-a-tde-protected-database-to-another-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-objects/sys-dm-database-encryption-keys-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transparent data encryption (TDE)

**Goal:** data files, log files, tempdb and backups encrypted at rest, with the
certificate safely backed up so a restore elsewhere is possible.

## Key hierarchy
Service master key (per instance, DPAPI) -> database master key in `master` ->
certificate (or asymmetric key / EKM key) in `master` -> database encryption key (DEK)
in the user database. Losing the certificate = losing every backup of that database.

## Enable
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<strong-password>';
CREATE CERTIFICATE TDE_Cert WITH SUBJECT = 'TDE certificate';
-- BACK UP IMMEDIATELY, store off-server with the password in a vault
BACKUP CERTIFICATE TDE_Cert TO FILE = '<SECURE_SHARE>\TDE_Cert.cer'
  WITH PRIVATE KEY (FILE = '<SECURE_SHARE>\TDE_Cert.pvk', ENCRYPTION BY PASSWORD = '<pvk-password>');
USE appdb;
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256 ENCRYPTION BY SERVER CERTIFICATE TDE_Cert;
ALTER DATABASE appdb SET ENCRYPTION ON;
```
TDE is not available for `master`, `model` or `msdb`, and `tempdb` is encrypted automatically but cannot be encrypted directly. Edition
availability: see Microsoft's editions and supported features pages. The algorithm can be AES_128, AES_192, AES_256 or TRIPLE_DES_3KEY (see
CREATE DATABASE ENCRYPTION KEY). The DEK can also be protected by an asymmetric key, but only one held by an EKM module. If any filegroup is READ ONLY the
encryption operation fails. FILESTREAM data is not encrypted. While the first encryption scan runs, ALTER DATABASE and other maintenance is
blocked (single-user mode allows maintenance).

## Monitor the scan
```sql
SELECT DB_NAME(database_id) db, encryption_state, encryption_state_desc, percent_complete, encryption_scan_state_desc
FROM sys.dm_database_encryption_keys;   -- encryption_state 3 = encrypted; the _desc columns need SQL Server 2019+; tempdb shows up too
```
The background scan reads each page into the buffer pool and writes it back encrypted. From SQL Server 2019 you can pause and resume it:
`ALTER DATABASE appdb SET ENCRYPTION SUSPEND;` / `RESUME` (not in Azure SQL). Remove TDE with `ALTER DATABASE appdb SET ENCRYPTION OFF;`, wait for
decryption, then `DROP DATABASE ENCRYPTION KEY`; after that take a log backup and a fresh full backup, and keep the certificate until you have.

## Restore on another server
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<pw>';   -- if none exists
CREATE CERTIFICATE TDE_Cert FROM FILE = '<path>\TDE_Cert.cer'
  WITH PRIVATE KEY (FILE = '<path>\TDE_Cert.pvk', DECRYPTION BY PASSWORD = '<pvk-password>');
RESTORE DATABASE appdb FROM DISK = '...';
```
Without the certificate (and private key) the database cannot be opened, restored or attached on another server. The private-key
password need not match the database master key password. For availability groups, create the master key and certificate on all
secondary replicas **before** creating the DEK on the primary; for log shipping or mirroring, back up the master key and certificate too.

## Rotation
Change the protector with
`ALTER DATABASE ENCRYPTION KEY ENCRYPTION BY SERVER CERTIFICATE TDE_Cert_2027;`
(state 6 = protection change in progress). If you change a DEK twice you must take a log backup before changing it again. Keep the old
certificate as long as any backups or log segments encrypted under it are retained. Never drop the certificate from `master`; error 33091
warns when the certificate used by `CREATE DATABASE ENCRYPTION KEY` has not been backed up.

## Gotchas
- tempdb becomes encrypted when any database uses TDE (small CPU cost for everyone).
- Instant file initialization is not used for TDE databases.
- Backups of a TDE database are encrypted with the DEK, so restores need the certificate.
- Expired certificates still work for TDE. Do not password-protect a certificate that TDE already uses: the database becomes inaccessible after restart.
- Buffer pool extension files are not encrypted by TDE. TDE does not encrypt connections; replication does not carry encryption to subscribers.

## Verify
- [ ] Certificate and private key backup exists off-server and a test restore succeeded elsewhere.
- [ ] `encryption_state = 3` (ENCRYPTED) for each intended database; `pvt_key_last_backup_date` in `sys.certificates` is not NULL for the TDE certificate.
- [ ] Certificate present on every AG/log-shipping replica.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Transparent Data Encryption, Move a TDE-protected database and sys.dm_database_encryption_keys (2017-2025).
Confirmed: key hierarchy, enable/backup/restore T-SQL, DEK algorithms and EKM-only asymmetric keys, scan suspend/resume (2019), DMV columns and their 2019 gates, tempdb and IFI effects, AG certificate ordering, DEK change and removal rules, error 33091. Removed unconfirmed claims: Standard-edition-since-2019, Azure default-on, the EXPIRY_DATE clause, restore error text, MAXTRANSFERSIZE rule and the "quick" rotation claim.
Method: documentation only; no commands were run.
