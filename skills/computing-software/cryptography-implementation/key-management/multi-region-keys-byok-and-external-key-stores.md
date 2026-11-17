---
id: computing-software.cryptography-implementation.key-management.multi-region-keys-byok-and-external-key-stores
name: multi-region-keys-byok-and-external-key-stores
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, kms, cloud-kms, byok, hyok, multi-region-keys, external-key-store, xks, cloud-ekm, import-key-material, disaster-recovery]
level: advanced
status: docs-checked
description: "Choose and run cloud KMS key custody options: multi-region keys for DR, BYOK key import, HYOK via AWS XKS / Google Cloud EKM / Azure Managed HSM, and their availability risks."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html", "https://docs.aws.amazon.com/kms/latest/developerguide/keystore-external.html", "https://cloud.google.com/kms/docs/ekm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-region keys, BYOK and external key stores

## Multi-region keys (DR and global apps)

AWS KMS multi-region keys share key material and key ID across regions, so
ciphertext encrypted in `eu-west-1` decrypts in `eu-central-1` without
cross-region calls.

```bash
aws kms create-key --multi-region --description "orders mrk"        # primary, key id mrk-...
aws kms replicate-key --key-id mrk-1234 --replica-region eu-central-1
```

- Each replica has its own key policy, grants and aliases; keep them in sync
  with IaC.
- Use for DR of encrypted data stores (S3 replication, DynamoDB global tables,
  client-side encrypted backups). Single-region keys make cross-region restore
  impossible without re-encryption.
- Do not use them where data residency rules forbid key material in other regions.

GCP: pick the key ring location (regional, multi-region or global) deliberately at creation.

## BYOK: importing key material

You generate key material on your own HSM, wrap it with the KMS-provided
wrapping public key, and import it.

```bash
aws kms create-key --origin EXTERNAL
aws kms get-parameters-for-import --key-id K --wrapping-algorithm RSA_AES_KEY_WRAP_SHA_256 --wrapping-key-spec RSA_4096
# wrap your 256-bit key with the returned public key (on your HSM), then:
aws kms import-key-material --key-id K --encrypted-key-material fileb://wrapped.bin \
  --import-token fileb://token.bin --expiration-model KEY_MATERIAL_DOES_NOT_EXPIRE
```

Trade-offs: you hold an escrow copy (good for exit strategy and recovery,
bad if your copy leaks); you are responsible for its durability (if KMS
material expires or is deleted, only your copy can restore it).

## HYOK: external key stores

The key never enters the cloud provider: KMS calls your external key manager
for each wrap/unwrap.

- AWS XKS (External Key Store) via an XKS proxy to your HSM.
- Google Cloud EKM (partners include Thales and Fortanix), with Key Access Justifications.
- Azure: check the Key Vault / Managed HSM documentation for current external-key options.

Every decrypt depends on your external system's availability and latency:
an outage of your key manager or network link makes cloud data unreadable.
Use only where sovereignty requirements demand it, with HA and caching
designs reviewed.

## Checked

2026-10-31. Confirmed in AWS KMS multi-region keys overview (same key material and key ID; replicas have own key policy, grants, aliases, tags, not synchronised; rotation only on the primary), the AWS KMS API model (WrappingAlgorithm RSA_AES_KEY_WRAP_SHA_256, WrappingKeySpec RSA_4096, ExpirationModel KEY_MATERIAL_DOES_NOT_EXPIRE, flags) and Google Cloud EKM (Key Access Justifications, Thales, Fortanix partners). Removed: GCP location immutability, PKCS#11 mechanism name, Azure FIPS level, import rotation limits (not confirmable on readable pages).

Method: documentation only; no commands were run.

## Verify

- [ ] Cross-region restore test decrypts data with the replica key.
- [ ] BYOK copies are inventoried with custodians and protected like root keys.
- [ ] HYOK availability SLOs and runbooks exist; outage tested.
