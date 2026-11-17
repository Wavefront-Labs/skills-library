---
id: computing-software.database-administration.sql-server.entra-authentication-for-azure-sql
name: entra-authentication-for-azure-sql
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, azure-sql, azure-sql-database, azure-sql-managed-instance, entra-authentication-sql, microsoft-entra-id, azure-ad-authentication, managed-identity, entra-only-authentication, contained-database-users, from-external-provider]
level: practitioner
status: docs-checked
description: "Set up Microsoft Entra authentication for Azure SQL: Entra admin, contained users from external provider, managed identities, Entra-only mode."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-configure
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-azure-ad-only-authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Entra authentication for Azure SQL

**Goal:** people and apps sign in with Entra ID identities (MFA, conditional access,
managed identities without secrets) instead of SQL logins with passwords.

## 1. Set the Entra admin (server level)
One user or **group** per logical server / MI (use a group so admins can change
without touching SQL):
```bash
az sql server ad-admin create -g rg -s prod-srv --display-name "SQL Admins" --object-id <group-object-id>
```
MI: `az sql mi ad-admin create`; the MI's identity needs Entra "Directory Readers"
(or the User/Group/Application read permissions) to resolve principals.

## 2. Create database users for Entra principals
Connect as the Entra admin, in the target database:
```sql
CREATE USER [alice@contoso.com] FROM EXTERNAL PROVIDER;
CREATE USER [DataAnalysts] FROM EXTERNAL PROVIDER;            -- Entra group
CREATE USER [orders-api] FROM EXTERNAL PROVIDER;              -- managed identity / app name
ALTER ROLE db_datareader ADD MEMBER [DataAnalysts];
```
These are contained users (no login in master).
Duplicate display names: `CREATE USER [name] FROM EXTERNAL PROVIDER WITH OBJECT_ID = '<guid>'`.

## 3. Apps with managed identity (no secrets)
- Enable a system- or user-assigned managed identity on the App Service / VM / AKS workload.
- Create the user as above with the identity's name.
- Connection string: use the managed identity authentication mode of your SQL driver (see the Microsoft Entra authentication overview).

## 4. Entra-only authentication
Disable SQL authentication entirely:
```bash
az sql server ad-only-auth enable -g rg -n prod-srv
```
Enforce with Azure Policy (see Azure Policy for Microsoft Entra-only authentication in the Learn docs).

## Troubleshooting
- Error 33134 / "Principal could not be resolved": server/MI identity lacks directory read
  permission, or a guest/B2B user needs `WITH OBJECT_ID`.
  lists Entra users (E) and groups (X).

## Verify
- [ ] Entra admin is a group; break-glass process documented.
- [ ] Apps use managed identity; no SQL passwords in config.
- [ ] Entra-only auth enabled where nothing still needs SQL logins.

## Checked

2026-10-28. Confirmed in the Learn Entra overview, configure and Entra-only pages: az sql server ad-admin and ad-only-auth commands (also checked against the az reference), Directory Readers requirement, error 33134, CREATE USER ... WITH OBJECT_ID, Azure Policy for Entra-only. Removed: SQL Server 2022 / Azure Arc claim, driver authentication keyword list and version, token lifetime, sys.database_principals query, old-driver note, geo-secondary and server-login sentences, SSMS option name.

Method: documentation only; no commands were run.
