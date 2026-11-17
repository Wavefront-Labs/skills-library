---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.key-rotation-crypto-shredding
name: key-rotation-crypto-shredding
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, crypto-shredding, key-rotation, envelope-encryption, right-to-erasure]
level: practitioner
status: draft
description: "Rotate encryption keys correctly and use crypto-shredding for erasure: envelope encryption, per-tenant or per-subject keys, backups, and proving deletion."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html", "https://learn.microsoft.com/azure/key-vault/keys/how-to-configure-key-rotation", "https://cloud.google.com/kms/docs/key-rotation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key rotation and crypto-shredding

## Steps
1. **Envelope encryption**: data encrypted with data keys (DEKs), DEKs wrapped by a KMS key
   (KEK). Rotation of the KEK in AWS KMS, Azure Key Vault and Cloud KMS creates new key
   versions; old versions stay to decrypt existing data. That is rotation without re-encryption.
2. **Set rotation periods** from NIST SP 800-57 cryptoperiod guidance and policy (commonly 1
   year for KEKs; automatic rotation in KMS). Re-encrypt data only when a key is suspected
   compromised.
3. **Crypto-shredding**: give each tenant (or data subject for high-value cases) its own key;
   destroying the key renders all their data, including backups and replicas, unreadable.
   AWS KMS key deletion has a 7-30 day waiting period; Cloud KMS version destruction has a
   scheduled-destruction delay; Key Vault soft-delete and purge protection retention apply.
4. **Backups**: shredding works only if backups are encrypted with the same per-tenant keys.
5. **Evidence**: log key destruction events (CloudTrail, Activity Log, Cloud Audit Logs) as
   proof of erasure; document residual plaintext (logs, search indexes) and handle separately.

## Gotchas
- Purge protection on Key Vault blocks immediate destruction by design; plan the delay.
- Per-subject keys at millions of subjects strain KMS quotas; use a key hierarchy.

## Verify
- [ ] Automatic rotation enabled on KEKs.
- [ ] Crypto-shredding test: data and backups unreadable after key destruction.
