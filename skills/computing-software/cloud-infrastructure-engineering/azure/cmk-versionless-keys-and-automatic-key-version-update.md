---
id: computing-software.cloud-infrastructure-engineering.azure.cmk-versionless-keys-and-automatic-key-version-update
name: cmk-versionless-keys-and-automatic-key-version-update
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, customer-managed-keys, versionless-key, auto-key-version, key-rotation-policy, disk-encryption-sets]
level: practitioner
status: docs-checked
description: "Make CMK rotation hands-off: versionless key URIs on Storage, disk encryption sets, SQL TDE auto-rotation and Cosmos DB, paired with a Key Vault rotation policy."
sources: ["https://learn.microsoft.com/azure/storage/common/customer-managed-keys-configure-existing-account", "https://learn.microsoft.com/azure/virtual-machines/disk-encryption#automatic-key-rotation-of-customer-managed-keys", "https://learn.microsoft.com/azure/azure-sql/database/transparent-data-encryption-byok-key-rotation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versionless CMK keys and automatic version update

**Goal:** rotate keys in Key Vault on a schedule and have every consuming service follow automatically.

## 1. Rotation policy on the key
```bash
az keyvault key rotation-policy update --vault-name kv-cmk --name storage-cmk --value '{
  "lifetimeActions":[{"trigger":{"timeAfterCreate":"P365D"},"action":{"type":"Rotate"}},
                     {"trigger":{"timeBeforeExpiry":"P30D"},"action":{"type":"Notify"}}],
  "attributes":{"expiryTime":"P2Y"}}'
```

## 2. Point services at the key without a version
- **Storage**: omit the version.
```bash
az storage account update -g rg -n stdata --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault https://kv-cmk.vault.azure.net --encryption-key-name storage-cmk \
  --key-vault-user-identity-id <uami-id> --identity-type UserAssigned
```
  Storage checks the vault for a new version once daily; wait 24 hours before disabling the old version.
- **Disk encryption set**: enable auto rotation.
```bash
az disk-encryption-set update -g rg -n des-prod --key-url https://kv-cmk.vault.azure.net/keys/disk-cmk \
  --enable-auto-key-rotation true
```
  Disks, snapshots and images referencing the set update to the new version within one hour; VMs are not rebooted.
- **SQL TDE**: server-level auto-rotation (new key version applied within 24 hours).
```bash
az sql server tde-key set -g rg -s sql-orders --server-key-type AzureKeyVault \
  --kid https://kv-cmk.vault.azure.net/keys/tde-cmk --auto-rotation-enabled true
```
- **Cosmos DB**: use a versionless key URI per its CMK doc.

## Gotchas
- Don't disable or delete previous key versions straight after rotation - services may still be re-wrapping.
- Versioned URIs (the old default in some templates) silently stop rotation - audit with Resource Graph for key
  URIs ending in a version GUID.
- Managed HSM keys support the same patterns; check each service supports HSM-backed keys in your region.

## Verify
- [ ] Rotate manually (`az keyvault key rotate`) in non-prod and confirm each service reports the new key version within its window.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: Storage daily version check and 24 hour wait, disk encryption sets updating within one hour without reboot, SQL TDE auto-rotation within 24 hours, TDE old-version guidance.

Removed because not confirmed: the Cosmos DB field name and the re-wrap/no-I/O claim.

Method: documentation only; no commands were run.
