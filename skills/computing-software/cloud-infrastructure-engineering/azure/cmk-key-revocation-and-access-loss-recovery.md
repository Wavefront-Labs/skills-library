---
id: computing-software.cloud-infrastructure-engineering.azure.cmk-key-revocation-and-access-loss-recovery
name: cmk-key-revocation-and-access-loss-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, customer-managed-keys, key-revocation, cmk-access-loss, crypto-shredding, tde-cmk, storage-cmk]
level: advanced
status: docs-checked
description: "Understand and recover from CMK key loss: what Storage, SQL TDE, disks and Cosmos DB do when a key is disabled or access revoked, and how to restore or crypto-shred."
sources: ["https://learn.microsoft.com/azure/storage/common/customer-managed-keys-overview", "https://learn.microsoft.com/azure/azure-sql/database/transparent-data-encryption-byok-overview", "https://learn.microsoft.com/azure/cosmos-db/how-to-setup-customer-managed-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMK key revocation and recovery

**Goal:** know the blast radius of a disabled key, deleted vault or removed identity permission - and get data back
(or deliberately make it unrecoverable).

## What happens per service (key disabled, deleted, or identity loses wrap/unwrap)
| Service | Effect | Recovery |
|---|---|---|
| Azure SQL DB / MI (TDE) | Encrypted database becomes inaccessible when key access is revoked | Restore access to the key; key revalidation depends on the key remaining available in Key Vault |

Storage, managed disks and Cosmos DB behave differently; read each service's customer-managed key page (see sources) before a revocation drill.

## Restore checklist
1. Is the key **disabled**? `az keyvault key set-attributes --vault-name kv --name k --enabled true`
2. Is it **soft-deleted**? `az keyvault key recover --vault-name kv --name k` (vault itself: `az keyvault recover --name kv`).
3. Did the service identity lose rights? Re-grant **Key Vault Crypto Service Encryption User** (RBAC) or
   the equivalent access-policy permissions to the storage account / SQL server / DES / Cosmos identity.
4. Check service-specific status until healthy.

## Prevent accidental loss
- Soft delete and purge protection on every CMK vault (required for Azure SQL TDE and Cosmos DB customer-managed keys).
- CanNotDelete lock on CMK vaults; restrict Key Vault Crypto Officer / Administrator via PIM.
- Activity log alerts on key disable, delete and role assignment removal on the vault.

## Deliberate revocation (crypto-shredding)
Disable the key (or remove access) to render data unreadable - an exit/offboarding control. To make it permanent,
delete and **purge** after the retention period (purge protection blocks early purge by design).

## Gotchas
- SQL TDE point-in-time recovery, geo-recovery and key revalidation depend on the key staying available in Key Vault.
- Keep the previous key version enabled after rotation until the service has switched (Cosmos DB docs: no activity on the previous version after 24 hours of rotation); do not delete old versions early.

## Verify
- [ ] Runbook tested in non-prod: disable key, observe failure, re-enable, confirm recovery time and alerts fired.

## Checked
2026-10-28. Confirmed on the SQL TDE BYOK and Cosmos DB customer-managed key pages: Key Vault Crypto Service Encryption User role for the service identity, soft delete and purge protection required, SQL database inaccessible when key access is revoked, revalidation and recovery depend on the key staying available, Cosmos previous-key 24-hour note. The `az keyvault` commands passed the CLI reference check.
Removed (not confirmed): Storage, disk and Cosmos revocation behaviour in the table, the Key Vault firewall step, the `az sql db show --query status` hint, Event Grid, and the geo-replica key-chain claim.

Method: documentation only; no commands were run.
