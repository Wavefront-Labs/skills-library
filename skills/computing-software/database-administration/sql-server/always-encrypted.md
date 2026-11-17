---
id: computing-software.database-administration.sql-server.always-encrypted
name: always-encrypted
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, sql-server-security, always-encrypted, column-master-key, column-encryption-key, deterministic-encryption, randomized-encryption, secure-enclaves, client-side-encryption]
level: advanced
status: docs-checked
description: "Protect sensitive SQL Server columns with Always Encrypted so the server never sees plaintext: keys, encryption types, driver settings and enclave limits."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-enclaves
  - https://learn.microsoft.com/en-us/sql/connect/jdbc/using-always-encrypted-with-the-jdbc-driver
  - https://learn.microsoft.com/en-us/sql/connect/odbc/using-always-encrypted-with-the-odbc-driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Always Encrypted

**Goal:** columns (SSN, card numbers) that are encrypted in the client driver, so
DBAs, backups and a compromised server only ever see ciphertext.

## Keys
- **Column master key (CMK)**: lives outside SQL Server (Windows cert store, Azure Key
  Vault, HSM). SQL Server stores only metadata pointing to it.
- **Column encryption key (CEK)**: encrypted by the CMK, stored in the database,
  used to encrypt column data.
DBAs who manage the database should not have access to the CMK: that separation is
the whole security model. Provision keys from a machine that holds the CMK, not the DB server.

## Encryption types
- **Deterministic**: same plaintext -> same ciphertext. Allows equality lookups,
  joins, GROUP BY, DISTINCT, IN and indexes. Leaks frequency patterns.
- **Randomized**: no computation, search, grouping, indexing or joins without enclaves; strongest.
String columns of either type must use a `_BIN2` collation (the BIN2 variant of the database's default collation family).

## Set up (SSMS wizard or PowerShell)
SSMS: right-click table -> Encrypt Columns, choose type and keys; it moves data out
and back through the client. PowerShell `SqlServer` module: `New-SqlColumnMasterKeySettings`,
`New-SqlColumnMasterKey`, `New-SqlColumnEncryptionKey`, `Set-SqlColumnEncryption`.
Resulting DDL looks like:
```sql
CREATE TABLE dbo.patients (
  id int IDENTITY PRIMARY KEY,
  ssn char(11) COLLATE Latin1_General_BIN2
      ENCRYPTED WITH (COLUMN_ENCRYPTION_KEY = CEK1, ENCRYPTION_TYPE = DETERMINISTIC,
                      ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256') NOT NULL);
```

## Application side
- Connection string: `Column Encryption Setting=Enabled` (ADO.NET / Microsoft.Data.SqlClient,
  JDBC `columnEncryptionSetting=Enabled`, ODBC `ColumnEncryption=Enabled`).
- App identity needs access to the CMK in its key store (for Azure Key Vault, see the key management article for the exact permissions) and the `VIEW ANY COLUMN MASTER KEY DEFINITION` / `VIEW ANY COLUMN ENCRYPTION KEY DEFINITION` database permissions (granted to `public` by default in SQL Server).
- Queries must be **parameterized**; literals in `WHERE ssn = '123-45-6789'` fail with
  an operand type clash. In SSMS enable "Parameterization for Always Encrypted".

## Secure enclaves (SQL Server 2019 and later, Azure SQL Database)
With enclave-enabled keys, randomized columns support pattern matching, comparison operators,
sorting and in-place encryption (no round-trip to the client). Enclave type and attestation
setup are covered in the Always Encrypted enclaves article; check it before planning.

## Gotchas
- Not supported on encrypted columns: default or check constraints, IDENTITY, full-text indexes, partitioning columns, most computed columns, FOR XML / FOR JSON, SQL Server replication, linked-server and OPENROWSET queries, and the xml, text, image, geography, geometry, hierarchyid and user-defined types. Availability groups work. Literals and T-SQL variables cannot target encrypted columns; copying plaintext columns into encrypted ones with `INSERT..SELECT` or `BULK INSERT` fails with operand type clash.
- After changing an encrypted column's definition run `sp_refresh_parameter_encryption` on dependent objects.
- Key rotation: `ALTER COLUMN ENCRYPTION KEY` adds or drops an encrypted value of a CEK; see the key management article for the full CMK rotation procedure.
- TDE vs Always Encrypted: TDE protects files at rest from someone with disk access;
  Always Encrypted protects data from privileged users of the server.

## Verify
- [ ] `sys.column_encryption_keys` / `sys.column_master_keys` list the keys and the CMK is
      not accessible from the DB server.
- [ ] Selecting the column from SSMS without the setting returns varbinary ciphertext.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: main Always Encrypted page for SQL Server 2025 (deterministic vs randomized operations, BIN2 collation rule for all string columns, long unsupported list including default and check constraints, replication and linked servers, parameterization and operand clash, four key permissions and the public default, enclaves available from SQL Server 2019, T-SQL cannot provision keys), Learn driver pages for the connection keywords (Column Encryption Setting=Enabled for SqlClient, columnEncryptionSetting=Enabled for JDBC, ColumnEncryption=Enabled for ODBC). Wrong in the draft: BIN2 was limited to deterministic character columns. Removed as unconfirmed: the Key Vault permission list, HGS/attestation specifics, the SqlBulkCopy statement and the detailed rotation steps.
Method: documentation only; no commands were run.
