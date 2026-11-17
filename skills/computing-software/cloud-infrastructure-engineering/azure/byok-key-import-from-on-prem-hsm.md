---
id: computing-software.cloud-infrastructure-engineering.azure.byok-key-import-from-on-prem-hsm
name: byok-key-import-from-on-prem-hsm
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, byok, byok-import, key-import, hsm-key-transfer, kek, managed-hsm, key-vault-premium]
level: advanced
status: docs-checked
description: "Transfer an HSM-protected key from an on-prem HSM into Key Vault Premium or Managed HSM with the BYOK flow: KEK creation, vendor wrapping, .byok upload and verification."
sources: ["https://learn.microsoft.com/azure/key-vault/keys/hsm-protected-keys-byok", "https://learn.microsoft.com/azure/key-vault/managed-hsm/hsm-protected-keys-byok", "https://learn.microsoft.com/azure/key-vault/keys/byok-specification"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BYOK key import from an on-prem HSM

**Goal:** a key generated in your own HSM (for compliance or key escrow) lands in an Azure HSM
without its plaintext ever existing outside an HSM boundary.

## When to use
- Regulation requires key generation in a customer-controlled HSM, or the same key must exist on-prem and in Azure.
- Otherwise prefer keys generated in Azure (simpler, rotation policies work).

## Supported sources
Vendor HSMs with BYOK tooling: Thales Luna, Entrust nShield, Utimaco, Fortanix, Marvell LiquidSecurity, IBM, Cryptomathic, etc. (check the current list). Target: Key Vault **Premium** (`RSA-HSM`, `EC-HSM`) or **Managed HSM**.

## Flow
1. **Create a Key Exchange Key (KEK)** in the target — an RSA-HSM key with only the `import` operation:
```bash
az keyvault key create --kty RSA-HSM --size 4096 --name kek-byok --ops import --vault-name kv-prem
az keyvault key download --name kek-byok --vault-name kv-prem --file kek.pem
```
   (Managed HSM: `--hsm-name` instead of `--vault-name`.)
2. **Transfer kek.pem** to the on-prem HSM environment (public key only — no secrecy needed, but verify integrity).
3. **Wrap the target key** with the vendor tool: generates the target key (or uses an existing one) and wraps it with the KEK, producing a `.byok` key transfer package.
4. **Upload**:
```bash
az keyvault key import --vault-name kv-prem --name cmk-orders --byok-file cmk-orders.byok --kty RSA-HSM --ops wrapKey unwrapKey
```
5. Delete the KEK once the import is done (it is single-purpose).

## Constraints
- KEK must be in the **same vault** as the import target.
- KEK can only have the `import` operation; key types and sizes must match the wrapping spec.
- Rotation: auto-rotation policies generate new versions *in Azure*; if keys must come from on-prem, rotation = repeat BYOK for a new version.

## Gotchas
- `az keyvault key import --pem-file` is a different path from `--byok-file`; use `--byok-file` for BYOK.
- The `.byok` file is wrapped for one KEK; if you recreate the KEK, re-wrap.
- Premium vault (not Standard) is required for HSM keys; Standard vault rejects `RSA-HSM`.

## Verify
- [ ] `az keyvault key show --vault-name kv-prem -n cmk-orders --query "key.kty"` returns `RSA-HSM`.
- [ ] A test wrap/unwrap succeeds (`az keyvault key encrypt/decrypt` with RSA-OAEP-256).
- [ ] Audit logs show the import by the expected operator; KEK deleted.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: KEK rules (RSA-HSM, import only, same vault), Premium and Managed HSM support, vendor list, az keyvault key create/download/import flags.

Removed because not confirmed: oct-HSM, KEK size list, CKM_RSA_AES_KEY_WRAP, KEK expiry claim, exportability claim, pem-file compliance claim, and the KeyImport audit name.

Method: documentation only; no commands were run.
