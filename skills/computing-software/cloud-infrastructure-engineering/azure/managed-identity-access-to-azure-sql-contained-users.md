---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-access-to-azure-sql-contained-users
name: managed-identity-access-to-azure-sql-contained-users
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identities, azure-sql, contained-user, create-user-from-external-provider, entra-authentication]
level: practitioner
status: docs-checked
description: "Give an app's managed identity access to Azure SQL: Entra admin, CREATE USER FROM EXTERNAL PROVIDER (or WITH OBJECT_ID), roles, connection strings and login errors."
sources: ["https://learn.microsoft.com/azure/azure-sql/database/authentication-aad-configure", "https://learn.microsoft.com/azure/app-service/tutorial-connect-msi-sql-database", "https://learn.microsoft.com/sql/t-sql/statements/create-user-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed identity access to Azure SQL

**Goal:** password-less app connections to Azure SQL Database / Managed Instance.

## 1. Entra admin on the server
```bash
az sql server ad-admin create -g rg-data -s sql-orders --display-name sg-sql-admins --object-id <groupObjectId>
```
Use a group (with PIM) rather than a person.

## 2. Create the contained user (in each database)
Connect to the **user database** as the Entra admin (SSMS/Azure Data Studio, Entra auth):
```sql
CREATE USER [app-orders-prod] FROM EXTERNAL PROVIDER;      -- name of MI (= resource name or UAMI name)
ALTER ROLE db_datareader ADD MEMBER [app-orders-prod];
ALTER ROLE db_datawriter ADD MEMBER [app-orders-prod];
-- or least privilege: GRANT EXECUTE ON SCHEMA::api TO [app-orders-prod];
```
`FROM EXTERNAL PROVIDER` makes SQL look the name up in Entra, so the **server's identity** needs Graph read rights
(Directory Readers role, or User.Read.All + GroupMember.Read.All + Application.Read.All). Without that, use:
```sql
CREATE USER [app-orders-prod] FROM EXTERNAL PROVIDER WITH OBJECT_ID = '<mi-principal-object-id>';
```
(`WITH OBJECT_ID` is documented for Azure SQL as a preview enhancement; use it where the server identity cannot resolve the name.)

## 3. Connection string
```
Server=tcp:sql-orders.database.windows.net;Authentication=Active Directory Default; Database=orders;
```
The App Service tutorial uses `Authentication=Active Directory Default`, which works both locally and in App Service.

## Errors
- Login fails for the identity: confirm the contained user exists in *that* database (users are per database).
- `CREATE USER ... FROM EXTERNAL PROVIDER` cannot resolve the name: check the server identity's Graph permissions or use `WITH OBJECT_ID`.

## Gotchas
- Turn on Entra-only authentication once SQL logins are gone.

## Verify
- [ ] `SELECT name, type_desc FROM sys.database_principals` lists the identity; app connects with no password in config.

## Checked
2026-10-28. Confirmed on the Entra authentication configure page, the App Service managed identity tutorial and the CREATE USER reference: `CREATE USER ... FROM EXTERNAL PROVIDER [WITH OBJECT_ID]` (preview for Azure SQL), Directory Readers role or fine-grained Graph permissions (User.Read.All, GroupMember.Read.All, Application.Read.All) for the server identity, `Authentication=Active Directory Default`. `az sql server ad-admin create` passed the CLI reference check.
Fixed: `WITH OBJECT_ID` is a preview enhancement. Removed (not confirmed): the `Active Directory Managed Identity` and JDBC `ActiveDirectoryMSI` strings, SqlClient version, group token lag and failover-group notes, the exact error text.

Method: documentation only; no commands were run.
