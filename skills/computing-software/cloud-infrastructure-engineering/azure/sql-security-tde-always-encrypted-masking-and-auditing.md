---
id: computing-software.cloud-infrastructure-engineering.azure.sql-security-tde-always-encrypted-masking-and-auditing
name: sql-security-tde-always-encrypted-masking-and-auditing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-security, tde, transparent-data-encryption, tde-cmk, always-encrypted, secure-enclaves, dynamic-data-masking, row-level-security, sql-auditing, defender-for-sql, vulnerability-assessment, advanced-threat-protection, entra-authentication, entra-only-auth, managed-identity-sql, sql-firewall, private-endpoint, ledger, data-discovery-classification, least-privilege-sql, contained-users, sql-auditing-setup]
level: advanced
status: docs-checked
description: "Secure Azure SQL: Entra-only auth, private endpoint, TDE with customer-managed keys, Always Encrypted, masking and row-level security, auditing, Defender for SQL."
sources: ["https://learn.microsoft.com/en-us/azure/azure-sql/database/security-best-practice", "https://learn.microsoft.com/en-us/azure/azure-sql/database/transparent-data-encryption-byok-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/dynamic-data-masking-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/auditing-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-azure-ad-only-authentication", "https://learn.microsoft.com/en-us/cli/azure/sql/server"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure SQL security — identity, network, encryption, visibility, in that order

**Goal:** no SQL logins, no public endpoint, keys you control, sensitive columns
protected from the DBA where the business asks, and an audit trail plus Defender
findings that someone reads.

## 1. Identity (the biggest win)
```bash
az sql server ad-admin create -g rg -s sql-prod-uks --display-name sg-sql-admins --object-id <group-oid>
az sql server ad-only-auth enable -g rg -n sql-prod-uks          # disables SQL authentication; use ad-only-auth disable to revert
```
Or create the server with `--enable-ad-only-auth` plus `--external-admin-principal-type/-name/-sid`. For a managed instance the equivalent is `az sql mi ad-only-auth enable`.

In the database, map identities to **contained users** (no server logins):
```sql
CREATE USER [app-orders-identity] FROM EXTERNAL PROVIDER;      -- managed identity / SP / group name
ALTER ROLE db_datareader ADD MEMBER [app-orders-identity];
ALTER ROLE db_datawriter ADD MEMBER [app-orders-identity];
```
- The server or instance identity needs the *Directory Readers* role (or the lower-level Microsoft Graph permissions) to resolve Entra principals; assigning it needs Privileged Role Administrator or higher, and a role-assignable group holding Directory Readers is the documented workaround.
- Least privilege: custom roles per app (`CREATE ROLE orders_rw; GRANT SELECT, INSERT, UPDATE ON SCHEMA::orders TO orders_rw`), never `db_owner` for apps; separate identities per app and environment.

## 2. Network
Disable public network access on the server (`az sql server update --enable-public-network false`) and use a private endpoint. If public access must stay, set `--minimal-tls-version 1.2` (the recommended minimum, after testing your apps) and use narrow firewall rules. On Managed Instance, use NSGs to restrict the public endpoint (port 3342) to required sources, or keep it disabled. Outbound firewall rules (`az sql server outbound-firewall-rule`, with `--restrict-outbound-network-access` on the server) limit where the server can connect.

## 3. Encryption
- **TDE** is on by default. With a **customer-managed key** the server identity needs Key Vault `get`, `wrapKey` and `unwrapKey` permissions (or, with Azure RBAC, the *Key Vault Crypto Service Encryption User* role). `az sql server tde-key set --server-key-type AzureKeyVault --kid <key-url> --auto-rotation-enabled true` sets the protector; a versionless key identifier makes SQL always use the latest enabled key version. If the server loses access to the protector, within up to 10 minutes databases refuse connections and change to the Inaccessible state (the only allowed action is deleting). In a failover-group pair, both servers need get, wrapKey and unwrapKey on the primary server's key vault.
- **Always Encrypted** is client-side column encryption: the server never sees plaintext keys or data, so the database engine cannot compute on encrypted columns unless secure enclaves are used. Check the Always Encrypted documentation for supported enclave types and driver settings for your tier.
- Connections: use `Encrypt=True;TrustServerCertificate=False`.

## 4. Data-level controls
- **Dynamic data masking**: `ALTER TABLE customers ALTER COLUMN email ADD MASKED WITH (FUNCTION = 'email()')`; other functions are `default()`, `partial(prefix, "padding", suffix)` and `random(low, high)`. Grant `UNMASK` to chosen users (column-level UNMASK is documented). Server admin, Entra admin and `db_owner` see unmasked data. Masking obfuscates results; it is not encryption.
- **Row-level security**: predicate function plus `CREATE SECURITY POLICY ... ADD FILTER PREDICATE ...` keyed on `SESSION_CONTEXT` or the user.
- **Data discovery and classification** labels columns; audit records carry `data_sensitivity_information` (truncated beyond 4,000 characters, as are statements).
- **Ledger** tables provide tamper-evident history; see the ledger overview for digest storage and overhead before using it.

## 5. Auditing and Defender
```bash
az sql server audit-policy update -g rg -n sql-prod-uks --state Enabled --lats Enabled --lawri <log-analytics-workspace-resource-id>
az sql server ms-support audit-policy update -g rg -n sql-prod-uks --state Enabled --lats Enabled --lawri <log-analytics-workspace-resource-id>
```
- Auditing writes to a storage account, a Log Analytics workspace or Event Hubs. On servers with many busy databases, default server-level auditing can produce very large volumes in one place, so scope the audit actions.
- `az sql server audit-policy update` takes `--lats`/`--log-analytics-target-state` and `--lawri`/`--log-analytics-workspace-resource-id` for Log Analytics.
- **Microsoft Defender for SQL** adds vulnerability assessment and threat detection; it can be enabled per server or managed instance, or for a whole subscription through Defender for Cloud. Look up the current plan names in Defender for Cloud before scripting it with `az security pricing create`.

## Gotchas
- Entra-only auth with an app still using a SQL login fails at connection time: find SQL-authenticated clients in the audit log before switching.
- Group-based contained users need the server identity to read the directory (Directory Readers or Graph permissions), otherwise `CREATE USER ... FROM EXTERNAL PROVIDER` cannot resolve the group.
- TDE CMK plus a Key Vault firewall or private network: test key access before go-live, because loss of access takes databases to Inaccessible.
- Always Encrypted breaks server-side computation on the column (filtering, sorting) unless enclaves are configured; plan column by column with the app team.
- Masking applies to query results; admins and `db_owner` always see plaintext.

## Verify
- [ ] `az sql server ad-only-auth get -g rg -n sql-prod-uks` shows Entra-only enabled; `az sql server show` shows public network access disabled and minimal TLS 1.2; `az sql server tde-key show` shows AzureKeyVault.
- [ ] An app connects with its managed identity and a SQL-login attempt fails.
- [ ] A masked column returns masked values for a user without UNMASK; an RLS predicate limits tenant rows (test with `EXECUTE AS USER`).
- [ ] Audit events arrive in the chosen destination.

## Checked
2026-10-27. Confirmed against Learn: security best practices, TDE with customer-managed keys (permissions, Inaccessible state timing, versionless keys), dynamic data masking, auditing overview, Entra-only authentication (including `az sql server ad-only-auth` and `az sql mi ad-only-auth`), Directory Readers role, and the az sql server/audit-policy/tde-key/ad-admin CLI references.
Corrected: `az sql server update --enable-ad-only-auth` does not exist (use `az sql server ad-only-auth enable`); `--lawid` is `--lawri`; Inaccessible happens within up to 10 minutes, not hours; `--public-network-access` is `--enable-public-network` on `az sql server`.
Removed (unconfirmed): key size list, soft-delete and purge-protection claim, default audit action groups, KQL examples, Defender plan name, express-configuration claim, policy built-in names, bacpac and cross-tenant claims.
Method: documentation only; no commands were run.
