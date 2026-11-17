---
id: computing-software.database-administration.sql-server.backup-to-url
name: backup-to-url
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-backup, backup-to-url, azure-blob-storage, s3-backup, shared-access-signature, credential, block-blob, striping, maxtransfersize]
level: practitioner
status: docs-checked
description: "Back up SQL Server directly to Azure Blob (SAS block blobs) or S3-compatible storage with credentials, striping and transfer-size settings that work."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/sql-server-backup-to-url
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/sql-server-backup-to-url-s3-compatible-object-storage
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql
  - https://ola.hallengren.com/sql-server-backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup to URL (Azure Blob and S3)

**Goal:** off-host backups written straight to object storage, restorable from any server.

## Azure Blob with SAS (2016+, preferred)
Block blobs, credential named exactly after the container URL:
```sql
CREATE CREDENTIAL [https://<account>.blob.core.windows.net/sqlbackups]
  WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
  SECRET = '<sas-token-without-leading-?>';   -- perms: read, write, delete, list (the docs' stored access policy uses rwld)

BACKUP DATABASE appdb
  TO URL = 'https://<account>.blob.core.windows.net/sqlbackups/appdb_full_1.bak',
     URL = 'https://<account>.blob.core.windows.net/sqlbackups/appdb_full_2.bak',
     URL = 'https://<account>.blob.core.windows.net/sqlbackups/appdb_full_3.bak'
  WITH COMPRESSION, CHECKSUM, MAXTRANSFERSIZE = 4194304, BLOCKSIZE = 65536, STATS = 10;
```
A single block blob holds max 50,000 blocks x 4 MB = ~195 GB, so stripe large backups
across several URLs (up to 64, about 12.8 TB in total) and set `MAXTRANSFERSIZE = 4194304` with
`BLOCKSIZE = 65536`, as Microsoft recommends, to make best use of the 50,000 blocks per blob. SQL Server can write smaller blocks
and reach the block limit early, so stripe even backups under 200 GB, especially differential or uncompressed ones.
Transaction log backups to several files use 64 KB blocks regardless of `MAXTRANSFERSIZE`. The legacy page-blob form
(storage account key credential, `WITH CREDENTIAL`) caps at 1 TB; block blob is preferred from SQL Server 2016.
Other limits: no appending (overwrite with `WITH FORMAT`), no premium storage, and backup to URL does not work if Shared Key
authorization is disabled on the storage account.
Managed identity (SQL Server 2022 and later; see the CREATE CREDENTIAL page for platform requirements) avoids SAS rotation:
`CREATE CREDENTIAL [https://...] WITH IDENTITY = 'Managed Identity';`.

## S3-compatible (2022+)
```sql
CREATE CREDENTIAL [s3://s3.us-east-1.amazonaws.com/my-bucket/sql]
  WITH IDENTITY = 'S3 Access Key', SECRET = '<AccessKeyID>:<SecretKey>';
BACKUP DATABASE appdb TO URL = 's3://s3.us-east-1.amazonaws.com/my-bucket/sql/appdb_1.bak',
                         URL = 's3://s3.us-east-1.amazonaws.com/my-bucket/sql/appdb_2.bak'
  WITH COMPRESSION, CHECKSUM, MAXTRANSFERSIZE = 20971520;   -- up to 20 MB parts
```
S3: up to 10,000 parts per file, so the file limit is 10,000 x MAXTRANSFERSIZE (stripe to up to 64 URLs for larger databases).
`MAXTRANSFERSIZE` is 5 to 20 MB, default 10 MB, and changing it requires `COMPRESSION`. Any S3-compatible provider works over HTTPS with a
certificate trusted by the SQL Server host; Express editions are not supported.
Region can be passed with `BACKUP_OPTIONS = '{"s3": {"region":"us-west-2"}}'`.

## Restore
```sql
RESTORE DATABASE appdb FROM URL = '...appdb_full_1.bak', URL = '...appdb_full_2.bak', URL = '...appdb_full_3.bak'
  WITH NORECOVERY, STATS = 10;
```
The restoring server needs the same credential.

## Gotchas
- SAS expiry silently breaks every backup job: alert on job failure and rotate before expiry.
- Ola Hallengren `DatabaseBackup @URL = ..., @NumberOfFiles = 8, @MaxTransferSize = 4194304, @BlockSize = 65536`
  handles striping; its docs say cleanup is not supported when backing up to URL, so use storage lifecycle policies.
- Azure immutable storage (container-level policy) is supported for backup to URL from SQL Server 2025; before that the immutable-storage policy must be off. With it, `WITH FORMAT` on an existing blob fails.
- Network throughput is often the bottleneck; compression reduces the bytes sent.

## Verify
- [ ] A striped full backup larger than 200 GB completes.
- [ ] `RESTORE VERIFYONLY FROM URL = ...` succeeds from a different server.
- [ ] Credential/SAS expiry date tracked.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: backup to URL (Azure Blob) article and S3-compatible article for SQL Server 2025 (block blob preferred from 2016 and needs SAS, page blob 1 TB, block blob about 195.3 GB from 50,000 blocks x 4 MB, up to 64 URLs and 12.8 TB, recommended MAXTRANSFERSIZE 4194304 and BLOCKSIZE 65536, log backups 64 KB blocks, no append, no premium storage, Shared Key note, immutable storage from 2025; S3 from SQL Server 2022, 10,000 parts, MAXTRANSFERSIZE 5-20 MB default 10 MB and COMPRESSION requirement, HTTPS and trusted certificate, Express unsupported, region via BACKUP_OPTIONS, credential naming and IDENTITY = 'S3 Access Key'), CREATE CREDENTIAL (SAS identity, no leading ?, managed identity), Ola Hallengren page (@URL, @BlockSize, cleanup unsupported for URL). Removed as unconfirmed: the error 1117 symptom, the 'add create permission for 2022' SAS note, MinIO by name, S3 Object Lock and the stripes-beyond-8 remark.
Method: documentation only; no commands were run.
