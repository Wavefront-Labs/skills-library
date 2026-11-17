---
id: computing-software.cybersecurity-defensive.system-hardening.sql-server-hardening
name: sql-server-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-hardening, sql-server-hardening, mssql, windows-authentication, sa-account, xp-cmdshell, surface-area-reduction]
level: advanced
status: draft
description: "Harden Microsoft SQL Server: Windows auth, disable or rename sa, surface area reduction (xp_cmdshell, CLR, OLE), least privilege, encrypted connections and patch level."
sources: ["CIS Microsoft SQL Server 2022 Benchmark", "Microsoft Learn - SQL Server security best practices", "Microsoft Learn - Surface Area Configuration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL Server hardening

**Goal:** a SQL Server instance with minimal features enabled, no shared sa use, least-privilege logins and encrypted connections.

## Authentication
- Prefer Windows authentication mode; if mixed mode is required, enforce password policy on SQL logins (`CHECK_POLICY = ON`).
- Disable and rename `sa`: `ALTER LOGIN sa DISABLE; ALTER LOGIN sa WITH NAME = [sa_disabled];`.
- Remove `BUILTIN\Administrators` style broad sysadmin grants; review `SELECT name FROM sys.server_principals p JOIN sys.server_role_members m ON p.principal_id=m.member_principal_id WHERE m.role_principal_id = SUSER_ID('sysadmin');`.

## Surface area
```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 0;
EXEC sp_configure 'clr enabled', 0;              -- unless needed; then 'clr strict security' = 1
EXEC sp_configure 'Ole Automation Procedures', 0;
EXEC sp_configure 'Ad Hoc Distributed Queries', 0;
EXEC sp_configure 'remote access', 0;
EXEC sp_configure 'cross db ownership chaining', 0;
EXEC sp_configure 'Database Mail XPs', 0;        -- if unused
RECONFIGURE;
```
Disable unused protocols (Named Pipes) in Configuration Manager; disable SQL Browser if using fixed ports; set `TRUSTWORTHY OFF` on user databases.

## Service accounts
Run engine and agent as virtual accounts or gMSAs, not LocalSystem or domain admins. The service account's rights are what `xp_cmdshell` would get.

## Privileges
- Apps get database roles (`db_datareader`/`db_datawriter` or custom roles with `EXECUTE` on schemas), never `db_owner`/sysadmin.
- Revoke `CONNECT` from `guest` in user databases.

## Encryption
Install a certificate and set "Force Encryption" (or `Force Strict Encryption` with TDS 8.0 in SQL 2022); clients use `Encrypt=True;TrustServerCertificate=False`.

## Patching
Track CU level (`SELECT @@VERSION`); apply latest CU and GDR security updates.

## Verify
- [ ] `SELECT name, value_in_use FROM sys.configurations WHERE name IN ('xp_cmdshell','clr enabled')` = 0.
- [ ] `sys.dm_exec_connections` shows `encrypt_option = TRUE` for app connections.
