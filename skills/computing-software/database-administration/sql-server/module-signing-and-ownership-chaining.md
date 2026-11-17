---
id: computing-software.database-administration.sql-server.module-signing-and-ownership-chaining
name: module-signing-and-ownership-chaining
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-security, module-signing, ownership-chaining, execute-as, certificate-signing, least-privilege]
level: advanced
status: docs-checked
description: "Give a stored procedure elevated rights safely in SQL Server: ownership chains, EXECUTE AS pitfalls, and signing modules with certificates instead."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/ownership-chains
  - https://learn.microsoft.com/en-us/sql/relational-databases/tutorial-signing-stored-procedures-with-a-certificate
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/execute-as-clause-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module signing and ownership chaining

Goal: users execute `dbo.usp_TruncateStaging` without being granted `ALTER` on the table or
server-level rights.

## Ownership chaining (free, limited)
If a procedure and the objects it references have the **same owner**, permissions on the
referenced objects are not checked; only EXECUTE on the procedure (see the ownership chains page for what chaining covers; DDL such as `TRUNCATE` needs another approach, below).

## EXECUTE AS (works, but broad)
```sql
CREATE PROCEDURE dbo.usp_TruncateStaging WITH EXECUTE AS OWNER AS TRUNCATE TABLE dbo.Staging;
```
A module that runs `TRUNCATE TABLE` and executes as a user who may alter the table extends the right to truncate to whoever has EXECUTE on the module. The impersonation applies to everything inside the module, so keep such modules small.

## Module signing (preferred)
Grant rights to a certificate-mapped user and sign the procedure with the certificate (see the signing tutorial). Callers keep their own identity.
```sql
USE Sales;
CREATE CERTIFICATE cert_staging ENCRYPTION BY PASSWORD = '<PASSWORD>'
  WITH SUBJECT = 'Sign usp_TruncateStaging';
CREATE USER cert_staging_user FROM CERTIFICATE cert_staging;   -- no login, cannot connect
GRANT ALTER ON dbo.Staging TO cert_staging_user;               -- TRUNCATE needs ALTER
ADD SIGNATURE TO dbo.usp_TruncateStaging BY CERTIFICATE cert_staging WITH PASSWORD = '<PASSWORD>';
GRANT EXECUTE ON dbo.usp_TruncateStaging TO app_role;
```

## Maintenance
- Re-check the signature after every change to the procedure and re-sign in the deployment pipeline if needed.
- Back up the certificate with its private key if you need to re-sign elsewhere.

## Verify
As a user with only EXECUTE: `EXEC dbo.usp_TruncateStaging;` succeeds, while
`TRUNCATE TABLE dbo.Staging;` directly fails with permission denied.

## Checked

2026-10-28. Confirmed against Microsoft Learn: the signing stored procedures tutorial (CREATE CERTIFICATE, ADD SIGNATURE) and the EXECUTE AS clause page (a module with TRUNCATE TABLE that executes as a user who can alter the table extends truncate rights to users with EXECUTE). Removed unconfirmed: dynamic SQL / cross-database chaining limits, TRUSTWORTHY escalation note, ORIGINAL_LOGIN behaviour, server-level certificate-in-master procedure, signature-drop-on-ALTER claim, sys.crypt_properties query, sys.user_token check.

Method: documentation only; no commands were run.
