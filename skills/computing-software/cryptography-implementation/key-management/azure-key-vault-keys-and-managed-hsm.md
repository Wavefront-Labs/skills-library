---
id: computing-software.cryptography-implementation.key-management.azure-key-vault-keys-and-managed-hsm
name: azure-key-vault-keys-and-managed-hsm
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, azure-key-vault-keys, azure-key-vault, azure-managed-hsm, azure, rbac, purge-protection, key-rotation-policy, security-domain]
level: practitioner
status: docs-checked
description: "Create and use Azure Key Vault keys and Managed HSM: RBAC roles, purge protection, key operations, rotation policy and security-domain handling."
sources: ["https://learn.microsoft.com/en-us/azure/key-vault/keys/about-keys", "https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide", "https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/security-domain"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Key Vault keys and Managed HSM

## Vault creation with safe defaults
```
az keyvault create --name kv-orders --resource-group rg-sec --location westeurope \
  --sku premium --enable-rbac-authorization true --enable-purge-protection true --retention-days 90
```
- Premium-SKU vaults can hold HSM-protected keys (`RSA-HSM`, `EC-HSM`).

## Keys
```
az keyvault key create --vault-name kv-orders --name orders-kek --kty RSA-HSM --size 3072 --ops wrapKey unwrapKey
az keyvault key encrypt --vault-name kv-orders --name orders-kek --algorithm RSA-OAEP-256 --value <base64>
az keyvault key rotation-policy update --vault-name kv-orders --name orders-kek --value policy.json
```
Restrict `--ops` to what the key needs.

## RBAC roles
| Role | Use |
|---|---|
| Key Vault Crypto Service Encryption User | For services doing CMK (read key, wrap/unwrap) |
| Key Vault Administrator | All data plane operations on the vault and its objects (avoid for apps) |
The data plane supports Azure RBAC or the legacy access policy model; prefer RBAC.

## Managed HSM
- Single-tenant FIPS 140-3 Level 3 validated HSM (`az keyvault create --hsm-name ...`).
- **Security domain:** activation requires downloading an encrypted security domain protected by a quorum of RSA
  keys you supply (`az keyvault security-domain download --sd-wrapping-keys k1.cer k2.cer k3.cer --sd-quorum 2`).
  Lose the quorum and the HSM's keys are unrecoverable; store the wrapping keys like root CA keys.
- The quorum is at least 3 RSA key pairs sent at download, with a maximum quorum size of 10; Microsoft recommends m >= 3.

## Verify
- [ ] Purge protection on; RBAC mode enabled.
- [ ] App identity has Crypto User on the single key, nothing broader.
- [ ] Managed HSM security domain quorum keys are held by separate custodians.

## Checked
2026-10-31. Confirmed against the Key Vault about-keys, RBAC guide and Managed HSM security-domain pages: key types
(`RSA-HSM`, `EC-HSM`), role descriptions kept, FIPS 140-3 Level 3 Managed HSM, security domain quorum rules, RBAC or
access-policy data plane. CLI flags via check_commands. Removed (not on fetched pages): soft-delete and purge-protection
irreversibility claim, rotation policy fields, Crypto User and Officer role rows, Managed HSM local RBAC note, logging.
Method: documentation only; no commands were run.
