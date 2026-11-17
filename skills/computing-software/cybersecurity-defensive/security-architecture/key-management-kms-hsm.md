---
id: computing-software.cybersecurity-defensive.security-architecture.key-management-kms-hsm
name: key-management-kms-hsm
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, key-management, kms, hsm, key-rotation, key-policy, separation-of-duties, envelope-encryption, cloudhsm, key-vault, fips-140-3]
level: advanced
status: draft
description: "Manage cryptographic keys with KMS and HSMs: key hierarchy, key policies and separation of duties, rotation, backup, destruction and audit of key use."
sources: ["NIST SP 800-57 Part 1 Rev. 5 Recommendation for Key Management", "CompTIA Security+ SY0-701 objective 1.4 (HSM, KMS, key escrow)", "AWS KMS Developer Guide", "FIPS 140-3"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key management with KMS and HSMs

**Goal:** keys are generated, stored, used, rotated and destroyed under control, so that
encryption actually restricts access to data.

## Choose the store
| Option | When |
|---|---|
| Cloud KMS (AWS KMS, Azure Key Vault, GCP Cloud KMS) | Default for cloud workloads; FIPS 140-3 validated HSMs behind an API |
| Dedicated HSM (CloudHSM, Azure Managed HSM, on-prem Luna/nShield) | Single-tenant requirement, custom crypto, CA keys, payment (PCI PIN) |
| External key store (XKS, HYOK) | Sovereignty: keys outside the provider; you own availability risk |
| Secrets manager | Secrets (passwords, API keys), not encryption keys |

## Practices
1. **Hierarchy**: KEKs in KMS/HSM wrap data keys; applications never see KEK material.
2. **Key policy and separation of duties**: key administrators (create, rotate, schedule
   deletion) are different principals from key users (encrypt/decrypt). AWS example:
```json
{"Sid":"AllowUseByAppRole","Effect":"Allow",
 "Principal":{"AWS":"arn:aws:iam::111122223333:role/app"},
 "Action":["kms:Decrypt","kms:GenerateDataKey"],"Resource":"*",
 "Condition":{"StringEquals":{"kms:ViaService":"s3.eu-west-1.amazonaws.com"}}}
```
3. **Rotation**: automatic annual rotation for symmetric KMS keys (old versions kept for
   decrypt); asymmetric and imported keys rotate manually by new key + re-encryption or alias switch.
4. **Cryptoperiods** per NIST 800-57 guide rotation for signing and TLS keys.
5. **Backup / escrow**: HSM key backups with M-of-N custody; cloud KMS keys are not exportable (plan accordingly).
6. **Destruction**: scheduled deletion with a waiting period (7-30 days) and alert on scheduling; deletion is crypto-shredding of everything encrypted under it.
7. **Audit**: log every key operation (CloudTrail KMS, Key Vault diagnostic logs) and alert on decrypt from unusual principals or volumes.

## Gotchas
- `kms:*` to an application role or wildcard principals in key policies defeats the purpose.
- Grants (AWS KMS grants) bypass key policy reviews: list them in audits.
- Keys in environment variables or config files are not managed keys.
- A deleted key with no backups makes data unrecoverable: protect `ScheduleKeyDeletion` tightly.

## Verify
- [ ] Inventory of keys with owner, purpose, rotation and who can decrypt.
- [ ] Alert test: scheduling deletion of a test key triggers a notification.
