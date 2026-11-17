---
id: computing-software.database-administration.sql-server.ledger-tables
name: ledger-tables
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, ledger-tables, updatable-ledger, append-only-ledger, database-digest, tamper-evidence, sp-verify-database-ledger]
level: advanced
status: docs-checked
description: "Create SQL Server 2022 / Azure SQL ledger tables (updatable and append-only), store database digests, and verify tamper evidence with sp_verify_database_ledger."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-how-to-updatable-ledger-tables
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sys-sp-verify-database-ledger-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-digest-management
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-how-to-append-only-ledger-tables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ledger tables

Ledger makes tampering **detectable**, not impossible: each transaction is hashed into a chain
(blocks of transactions), and digests stored outside the database let you prove later that
rows and history were not altered, even by a sysadmin.

## Create
```sql
-- updatable: keeps history of every row version
CREATE TABLE dbo.AccountBalance (
  AccountId int NOT NULL PRIMARY KEY,
  Balance decimal(19,4) NOT NULL)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.AccountBalance_History), LEDGER = ON);

-- append-only: inserts only (audit/event logs)
CREATE TABLE dbo.AuditEvent (EventId bigint IDENTITY, Payload nvarchar(4000), At datetime2 DEFAULT sysutcdatetime())
WITH (LEDGER = ON (APPEND_ONLY = ON));
```
Ledger is available from SQL Server 2022 and creating ledger tables needs the `ENABLE LEDGER` permission. Hidden columns `ledger_start_transaction_id`,
`ledger_end_transaction_id`, `ledger_start_sequence_number`, `ledger_end_sequence_number` are added. A ledger view (`dbo.AccountBalance_Ledger`) shows
each change with its `ledger_operation_type_desc` (an update appears as a DELETE plus an INSERT); join `sys.database_ledger_transactions` for commit time
and principal. Microsoft recommends querying history through the ledger view, not the history table. Append-only tables block updates and deletes
and have no history table. A ledger database (configured at creation, cannot be converted back) allows only ledger tables, each updatable by default.
Hashes are SHA-256 over Merkle trees; blocks chain through the previous block's root hash.

## Digests
```sql
EXECUTE sp_generate_database_ledger_digest;   -- one row, a JSON document: database_name, block_id, hash, last_transaction_commit_time, digest_time
```
Needs the `GENERATE LEDGER DIGEST` permission. Store digests where privileged users cannot rewrite them: Azure Blob Storage with a locked immutability
policy, Azure Confidential Ledger, or an on-premises WORM device. Automatic digest upload on SQL Server supports only Azure Storage accounts (the
`sqldbledgerdigests` container is created manually, with a SAS policy and a matching SQL Server credential); in Azure SQL Database/Managed Instance it
is configured through the portal, PowerShell or CLI. The database scoped configuration is `LEDGER_DIGEST_STORAGE_ENDPOINT = <URL> | OFF` (default OFF;
SQL Server 2022+). Automatic digests are generated every 30 seconds when transactions occurred. Digests are tied to the database's create time,
so restored databases get a new incarnation.

## Verify
```sql
EXECUTE sp_verify_database_ledger N'<digest JSON>';                       -- @digests: JSON list from sys.database_ledger_latest_digest
EXECUTE sp_verify_database_ledger N'<digest JSON>', @table_name = N'dbo.AccountBalance';
```
The procedure recomputes block hashes, compares them with the supplied digests, verifies table hashes (all, or the named table) and checks nonclustered indexes. It
returns code 0 (success) or 1 (failure) and one row with `last_verified_block_id`; it requires the `VIEW LEDGER CONTENT` permission. Run on a schedule
and alert on failure.

## Gotchas
- Updatable ledger tables keep every previous row version in the history table; plan storage.
- Ledger makes tampering detectable, not impossible: someone with control of the machine can edit database files, but verification will then fail. Combine with permissions, auditing and backups.
- Check Microsoft's ledger limitations page for unsupported features before adopting.

## Checklist
- [ ] Digest storage configured and immutable.
- [ ] Scheduled verification job with alerting.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Ledger overview, Create and use updatable ledger tables, Digest management, sys.sp_verify_database_ledger and ALTER DATABASE SCOPED CONFIGURATION (SQL Server 2022 and later).
Confirmed: CREATE TABLE ... LEDGER = ON syntax, hidden columns, ledger view and transactions view, digest JSON fields and permissions, storage options and SQL Server automatic-storage restrictions, scoped configuration, verification procedure syntax, results and permission. Added the append-only syntax source. Removed unconfirmed claims: in-place conversion with `sp_copy_data_in_batches`, `CREATE DATABASE ... WITH LEDGER`, renamed dropped tables, `sp_verify_database_ledger_from_digest_storage`, the success message text, TRUNCATE/ALTER COLUMN and feature-compatibility specifics.
Method: documentation only; no commands were run.
