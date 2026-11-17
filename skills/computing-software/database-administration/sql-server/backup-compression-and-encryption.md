---
id: computing-software.database-administration.sql-server.backup-compression-and-encryption
name: backup-compression-and-encryption
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, backup-encryption-certificate, backup-compression, backup, certificate, zstd, restore]
level: practitioner
status: docs-checked
description: "Compress and encrypt SQL Server backups with a server certificate, back up that certificate, and restore encrypted backups on another instance."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-encryption
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/create-an-encrypted-backup
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-compression-sql-server
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql
  - https://ola.hallengren.com/sql-server-backup.html
  - https://docs.dbatools.io/Backup-DbaDatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup compression and encryption

## Compression
```sql
EXEC sp_configure 'backup compression default', 1; RECONFIGURE;
BACKUP DATABASE appdb TO DISK = '<BACKUP_DIR>/appdb.bak' WITH COMPRESSION, CHECKSUM;
-- SQL Server 2025 only: ZSTD (optional LEVEL = LOW | MEDIUM | HIGH); the default algorithm is MS_XPRESS
BACKUP DATABASE appdb TO DISK = '<BACKUP_DIR>/appdb.bak' WITH COMPRESSION (ALGORITHM = ZSTD, LEVEL = MEDIUM);
```
Compression trades CPU for less I/O; `QAT_DEFLATE` is a hardware option that needs Intel QuickAssist with integrated acceleration configured. TDE databases compress since 2016 only
when `MAXTRANSFERSIZE` > 65536 (automatic on 2019 CU5+). Check ratio:
```sql
SELECT TOP 20 database_name, backup_finish_date,
  backup_size/1048576 AS raw_mb, compressed_backup_size/1048576 AS comp_mb, encryptor_type
FROM msdb.dbo.backupset ORDER BY backup_finish_date DESC;
```

## Encryption (SQL Server 2014+; not available when backing up on Express or Web)
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<STRONG_SECRET>';     -- once per instance
CREATE CERTIFICATE BackupCert WITH SUBJECT = 'Backup encryption', EXPIRY_DATE = '2036-01-01';

BACKUP DATABASE appdb TO DISK = '<BACKUP_DIR>/appdb.bak'
WITH COMPRESSION, CHECKSUM,
     ENCRYPTION (ALGORITHM = AES_256, SERVER CERTIFICATE = BackupCert);
```
Back up the certificate and its private key immediately:
```sql
BACKUP CERTIFICATE BackupCert TO FILE = '<KEY_BACKUP_DIR>/BackupCert.cer'
WITH PRIVATE KEY (FILE = '<KEY_BACKUP_DIR>/BackupCert.pvk', ENCRYPTION BY PASSWORD = '<SECRET>');
```
Store the files and password in a vault separate from the backups. No certificate = no restore, ever.
Ola Hallengren: `@Encrypt = 'Y', @EncryptionAlgorithm = 'AES_256', @ServerCertificate = 'BackupCert'`.
dbatools: `Backup-DbaDatabase -EncryptionAlgorithm AES256 -EncryptionCertificate BackupCert`.

## Restore elsewhere
```sql
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<OTHER_SECRET>';
CREATE CERTIFICATE BackupCert FROM FILE = '<KEY_BACKUP_DIR>/BackupCert.cer'
WITH PRIVATE KEY (FILE = '<KEY_BACKUP_DIR>/BackupCert.pvk', DECRYPTION BY PASSWORD = '<SECRET>');
RESTORE DATABASE appdb FROM DISK = '<BACKUP_DIR>/appdb.bak' WITH MOVE ..., RECOVERY;
```
The restoring account needs `VIEW DEFINITION` on the certificate, and the certificate must match the one used (same thumbprint). Restoring to Express or Web is supported.

## Gotchas
- Do not renew or alter the certificate in place (a changed thumbprint makes it invalid for existing backups); for rotation create a new certificate for new backups and keep every old one while its backups are retained.
- Appending to an existing backup set is not supported for encrypted backups: use new files (`INIT, FORMAT`). Older SQL Server versions cannot read encrypted backups.
- TDE-encrypted databases are already encrypted in the backup; the TDE certificate is then what you must keep.

## Verify
`encryptor_type` = CERTIFICATE in `msdb.dbo.backupset`, and a test restore on a second instance succeeds using only vault-stored files.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: backup encryption article and BACKUP statement page for SQL Server 2025 (encryption from SQL Server 2014, AES_128/192/256 and TRIPLE_DES_3KEY, certificate or EKM asymmetric key, DMK in master, VIEW DEFINITION permission, certificate backup and restore sequence, Express and Web cannot encrypt during backup but can restore, no append, thumbprint rule; ZSTD available starting with SQL Server 2025 with LEVEL, MS_XPRESS default, QAT_DEFLATE needs QAT; MAXTRANSFERSIZE greater than 64 KB for TDE compression and automatic from 2019 CU5), msdb.backupset columns, Ola Hallengren DatabaseBackup parameters (@Encrypt, @EncryptionAlgorithm, @ServerCertificate), dbatools Backup-DbaDatabase (-EncryptionAlgorithm, -EncryptionCertificate). Wrong in the draft: ZSTD was presented as SQL Server 2022 (it is 2025, and the example would fail on 2022), the Standard/Enterprise-only edition statement was imprecise, and certificate rotation advice contradicted the thumbprint rule. Removed as unconfirmed: the typical 3-5x ratio and the claim that HEADERONLY/FILELISTONLY need the certificate.
Method: documentation only; no commands were run.
