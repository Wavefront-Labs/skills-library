---
id: computing-software.cloud-infrastructure-engineering.azure.customer-managed-keys-and-managed-hsm
name: customer-managed-keys-and-managed-hsm
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, customer-managed-keys, cmk, managed-hsm, byok, encryption-scopes, key-vault, disk-encryption-sets, storage-encryption, infrastructure-encryption, double-encryption, key-rotation, hsm, fips-140-3-level-3, security-domain, local-rbac, key-release, confidential-computing, sql-tde-cmk, cosmos-cmk]
level: advanced
status: docs-checked
description: "Put Storage/Disk/SQL/Cosmos under customer-managed keys with versionless keys and UAMI, encryption scopes, BYOK, and when Managed HSM (L3, security domain) is required."
sources: ["https://learn.microsoft.com/azure/storage/common/customer-managed-keys-overview", "https://learn.microsoft.com/azure/virtual-machines/disk-encryption", "https://learn.microsoft.com/azure/key-vault/managed-hsm/overview", "https://learn.microsoft.com/azure/key-vault/keys/hsm-protected-keys-byok", "https://learn.microsoft.com/azure/key-vault/general/soft-delete-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customer-managed keys and Managed HSM — own the key without owning an outage

**Goal:** regulated data encrypted under a key you control and can revoke, rotated
automatically, and a key store sized to the real requirement (Key Vault Premium vs Managed HSM).

## 1. Decide the key store
| Requirement | Store |
|---|---|
| "Customer-managed" checkbox | Key Vault **Standard** (software) or **Premium** (`RSA-HSM`) |
| FIPS 140-3 Level 3, single-tenant HSM, key never leaves | **Managed HSM** (priced per pool; see the pricing page) |
| Full HSM control, PKCS#11, Thales appliances | Dedicated HSM / Cloud HSM (check which Azure services integrate) |
Managed HSM extras: **local RBAC** (vault-level roles like *Managed HSM Crypto User*
assigned by `az keyvault role assignment --hsm-name`), a **security domain** you must
download at activation (guard it and its quorum keys — losing it loses the HSM), and
`az keyvault backup` to a storage account for region recovery.

## 2. The CMK pattern (same for every service)
1. Key: `az keyvault key create -n cmk-storage --vault-name kv-sec-prod --kty RSA-HSM --size 3072`
   with a rotation policy (2-year expiry, rotate 30 days before).
2. Identity: **user-assigned** managed identity (survives resource recreation and is
   available at create time) with *Key Vault Crypto Service Encryption User* on the key.
3. Point the service at the **versionless** key URI so auto-rotation is picked up.
```bash
az storage account update -n stprod -g rg --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault https://kv-sec-prod.vault.azure.net \
  --encryption-key-name cmk-storage --key-vault-user-identity-id <uami-resource-id> \
  --identity-type UserAssigned --user-identity-id <uami-resource-id>
```
Disks: `az disk-encryption-set create --key-url <versionless> --enable-auto-key-rotation true --mi-user-assigned <uami>`
then `az disk create --disk-encryption-set <des>`; VMs reference the DES on each disk.
SQL: `az sql server tde-key set --server-key-type AzureKeyVault --kid <key-url>` (TDE protector);
Cosmos DB: check its CMK doc for when the key can be set.
4. Vault firewall: keep *Allow trusted Microsoft services* on, or allow the service's outbound access; check each service's CMK doc.

## 3. Blob encryption scopes
Per-container or per-blob keys inside one account:
`az storage account encryption-scope create -n tenant-a --account-name stprod -g rg --key-source Microsoft.KeyVault --key-uri <key>`
then `az storage container create --default-encryption-scope tenant-a --prevent-encryption-scope-override true`.
Lets you "crypto-shred" one tenant by disabling its key, without one storage account per tenant.
`--require-infrastructure-encryption` adds the second layer (AES-256 twice) regulators sometimes ask for.

## 4. BYOK
Generate on your HSM (nCipher, Thales, Utimaco, Fortanix), wrap with the vault's Key
Exchange Key: `az keyvault key create --kty RSA-HSM -n kek --ops import` →
`az keyvault key download --file kek.pem` → vendor BYOK tool produces `.byok` →
`az keyvault key import --byok-file key.byok --kty RSA-HSM`. Imported keys can't be
auto-rotated in Azure; re-import a new version from your HSM.

## 5. Revocation and recovery
- Revoke = remove the identity's role or disable the key: data becomes inaccessible until the key is re-enabled; nothing is deleted. For disks, I/O generally starts to fail one hour after the key is disabled, deleted or expired.
- Key deleted with soft delete/purge protection → recoverable for the retention period (7 to 90 days, default 90). A purged key =
  data gone. This is the whole reason purge protection is mandatory for CMK vaults.
- Disaster: plan Managed HSM recovery with `az keyvault backup` + the security domain.

## Gotchas
- Keep every prior key version available while services rotate: Storage checks the vault only once daily, so wait 24 hours before disabling an older version.
- SQL TDE with CMK: old backups still need the key version that protected them, so keep old versions.
- Managed HSM: download the security domain at activation and store it safely.

## Verify
- [ ] `az storage account show --query encryption.keySource` → `Microsoft.Keyvault`; the key version in use changes after a manual key rotation.
- [ ] Disabling the key makes blob reads fail; re-enabling restores.
- [ ] Managed HSM: security domain file and quorum key holders documented; `az keyvault backup` scheduled.
- [ ] Policy *Storage accounts should use customer-managed key* is compliant for the scope.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: Managed HSM overview (single-tenant, FIPS 140-3 Level 3), Storage CMK (daily version check, wait 24 hours, Crypto Service Encryption User role), disk encryption (I/O fails about one hour after a key is disabled), soft-delete retention 7 to 90 days, TDE old-version guidance.

Removed because not confirmed: the 3-node and 3-of-N quorum figures, 7-day activation deadline, minutes/one-hour revocation timings, Cosmos creation-time rule, region-pair replication claims, cross-tenant and deallocation gotchas, SQL MI Inaccessible state, and an error name.

Method: documentation only; no commands were run.
