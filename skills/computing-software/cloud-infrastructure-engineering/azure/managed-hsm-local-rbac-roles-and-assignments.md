---
id: computing-software.cloud-infrastructure-engineering.azure.managed-hsm-local-rbac-roles-and-assignments
name: managed-hsm-local-rbac-roles-and-assignments
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-hsm, local-rbac, key-vault, separation-of-duties, data-plane]
level: practitioner
status: docs-checked
description: "Control Managed HSM data-plane access with local RBAC: built-in roles, key-level scopes, separation of duties, and how it differs from Azure control-plane RBAC."
sources: ["https://learn.microsoft.com/azure/key-vault/managed-hsm/access-control", "https://learn.microsoft.com/azure/key-vault/managed-hsm/built-in-roles", "https://learn.microsoft.com/azure/key-vault/managed-hsm/role-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed HSM local RBAC

**Goal:** least-privilege, separated access to HSM keys - nobody who manages the Azure resource can use keys
unless explicitly granted in the HSM.

## Two planes
- **Control plane** (Azure RBAC, endpoint management.azure.com): create, read, update, delete and move the HSM, set
  tags. Granting control-plane access does **not** grant data-plane access (a subscription Contributor can delete the
  HSM but cannot reach keys or role assignments).
- **Data plane** (Managed HSM local RBAC, enforced by the HSM at `<hsm-name>.managedhsm.azure.net`): keys, role
  management, full backup/restore, security domain. At creation you supply the initial data-plane administrators
  (`--administrators`); only they can use the data plane until others are assigned roles.

## Built-in local roles (all data plane)
| Role | What it grants |
|---|---|
| Managed HSM Administrator | Security domain, full backup and restore, role management. **No** key management |
| Managed HSM Crypto Officer | Role management, purge or recover deleted keys, export keys. No other key management |
| Managed HSM Crypto User | All key management except purge/recover of deleted keys and export; includes cryptographic use |
| Managed HSM Policy Administrator | Create and delete role assignments |
| Managed HSM Crypto Auditor | Read (not use) key attributes |
| Managed HSM Crypto Service Encryption User | Use a key for service encryption (get, wrap, unwrap) |
| Managed HSM Crypto Service Release User | Release a key to a trusted execution environment |
| Managed HSM Backup | Single-key or whole-HSM backup |
| Managed HSM Restore | Single-key or whole-HSM restore |

Crypto Officer and Policy Administrator can manage role assignments, which includes assigning themselves
Administrator, and Entra Global Administrators can also assign it: treat these roles as highly privileged.

## Assign (scope `/` = whole HSM, `/keys` = all keys, `/keys/<name>` = one key)
```bash
az keyvault role definition list --hsm-name hsm-prod -o table
az keyvault role assignment create --hsm-name hsm-prod --role "Managed HSM Crypto Service Encryption User" \
  --assignee-object-id <storage-identity-oid> --assignee-principal-type ServicePrincipal --scope /keys/storage-cmk
az keyvault role assignment list --hsm-name hsm-prod --scope /keys/storage-cmk -o table
```
Listing at `/` or `/keys` shows only top-level assignments, not individual key-level ones. Custom role definitions
are managed with CLI or PowerShell only (not the portal), via `az keyvault role definition create`.

## Separation of duties
- Role administrators, key users, service identities (key use) and auditors should be different principals.
- Because Crypto User holds key lifecycle and cryptographic use while Administrator cannot touch keys, split these
  deliberately rather than giving one group both.

## Gotchas
- Assigning at `/` gives a CMK identity access to every key; scope to the specific key.

## Verify
- [ ] Each service identity has access only to its own key (`az keyvault role assignment list` per key scope).

## Checked
2026-10-27. Confirmed against Learn Managed HSM "Access control", "Local RBAC built-in roles" (updated 2025-11-19) and
"Role management". Fixed: the role table had Administrator managing role assignments with "full admin" (it cannot do key
management), Crypto Officer as key lifecycle (it manages roles and purge/recover/export), Policy Administrator as
security/release policies (it creates and deletes role assignments), Backup as "full backup/restore" (backup only; a
separate Restore role exists). Removed: lock-out on deleting last Administrator, portal blade claims, security-domain
quorum advice and diagnostic-log claims (not in fetched pages).
Method: documentation only; no commands were run.
