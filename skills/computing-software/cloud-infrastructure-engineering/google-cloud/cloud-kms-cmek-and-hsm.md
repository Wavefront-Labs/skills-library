---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-kms-cmek-and-hsm
name: cloud-kms-cmek-and-hsm
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-kms, kms, cmek, customer-managed-encryption-keys, cloud-hsm, cloud-external-key-manager, ekm, key-rings, crypto-keys, key-rotation, key-versions, envelope-encryption, autokey, cmek-org-policy, key-access-justifications, separation-of-duties, kms-iam, encrypt-decrypt-api, asymmetric-keys, mac-keys]
level: advanced
status: docs-checked
description: "Run Cloud KMS as the org key service: key rings, CMEK with service agents, Autokey, rotation and version lifecycle, HSM and EKM, destroy-key safety net."
sources: ["https://cloud.google.com/kms/docs/key-management-service", "https://cloud.google.com/kms/docs/cmek", "https://cloud.google.com/kms/docs/autokey-overview", "https://cloud.google.com/kms/docs/key-rotation", "https://cloud.google.com/kms/docs/hsm", "https://cloud.google.com/kms/docs/ekm", "https://cloud.google.com/kms/docs/separation-of-duties", "https://cloud.google.com/kms/docs/destroy-restore"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud KMS, CMEK and HSM

**Goal:** every regulated dataset is encrypted with a key your org controls, in a key project
nobody else can touch, rotated on schedule, with the ability to cryptographically shred data by destroying a key — and no way to do that by accident.

## 1. Layout
- One **key project per environment** (`prj-p-kms`), owned by the security team; data projects reference keys cross-project.
- **Key ring** per region per domain (`europe-west1/payments`); check each service's CMEK page for which key locations it accepts.
- **Purposes**: `ENCRYPT_DECRYPT` (symmetric, CMEK), `ASYMMETRIC_SIGN`, `ASYMMETRIC_DECRYPT`, `MAC`. **Protection level**: `SOFTWARE`, `HSM` (FIPS 140-2 Level 3 certified HSMs), `EXTERNAL`/`EXTERNAL_VPC` (Cloud EKM: keys managed in your external key manager, over the internet or over a VPC).
```bash
gcloud kms keyrings create payments --location=europe-west1 --project=prj-p-kms
gcloud kms keys create gcs --keyring=payments --location=europe-west1 --purpose=encryption \
  --protection-level=hsm --rotation-period=90d --next-rotation-time=2026-11-01T00:00:00Z \
  --destroy-scheduled-duration=30d   # minimum 24 hours; default 30 days
```

## 2. CMEK on services (service agents must be granted)
Each service that supports CMEK has its own CMEK page naming the flag to pass the key and the service agent that needs `roles/cloudkms.cryptoKeyEncrypterDecrypter`; grant that role on the key (not the project) with `gcloud kms keys add-iam-policy-binding`, using the **data** project's service agent.
- **Autokey**: services request `KeyHandle`s (`CreateKeyHandle`) and Autokey creates the keys for you, which scales CMEK across a folder; see the Autokey overview.

## 3. Rotation and versions
- Rotation creates a new primary version; older versions remain available for existing data.
- Disable old versions after confirming no reads (`kms keys versions disable`), then destroy: the version stays in the scheduled-for-destruction state for the configured duration (default 30 days) and can be restored during it. Before destroying, re-encrypt anything the version protects with another version; destroying a version that still protects data loses that data.
- Alert on `DestroyCryptoKeyVersion` and `DisableCryptoKeyVersion` audit events.

## 4. Separation of duties and access
- Key project: the security team holds `roles/cloudkms.admin` (destroy and restore need it on the key); keep `cryptoKeyEncrypterDecrypter` on prod keys to service agents and workload service accounts, not people.
- `roles/cloudkms.viewer` for auditors.
- **Key Access Justifications** (with Cloud EKM) include the reason for each request in the call to your external key manager.
- Direct API use (`gcloud kms encrypt --plaintext-file= --ciphertext-file=`) is limited to 64 KiB for software keys (8 KiB for HSM keys); larger data needs envelope encryption.

## 5. HSM and EKM
- HSM keys: `--protection-level=hsm`. Import your own material with import jobs (`--skip-initial-version-creation` so the imported key is version 1).
- EKM: `EXTERNAL` keys go over the internet and `EXTERNAL_VPC` keys over a VPC; you can migrate existing key versions between the two. Losing access to the external key can cause permanent data loss.

## Gotchas
- Removing access to a key a resource depends on can make the resource unavailable; alert on `DisableCryptoKeyVersion` as well as destroy events.
- Some services accept a CMEK only at creation; check each service's CMEK page.

## Verify
- [ ] `gcloud kms keys describe` shows `rotationPeriod`, HSM level, and destroy duration; next rotation is in the future.
- [ ] The resource's `describe` shows the key; writes from the data project work.
- [ ] No `user:` principal holds `cryptoKeyEncrypterDecrypter` on prod keys (`gcloud kms keys get-iam-policy`).
- [ ] Audit log alert fires on `DestroyCryptoKeyVersion` in a sandbox; `restore` within the window recovers decryption.

## Checked
2026-10-28. Confirmed on the Cloud KMS overview, key rotation, destroy-restore, HSM, EKM, importing-a-key and audit-logging pages: FIPS 140-2 Level 3 HSMs, EXTERNAL and EXTERNAL_VPC levels and migration between them, 24 hour minimum and 30 day default destroy duration, 64 KiB software and 8 KiB HSM limits, `cloudkms.admin` for destroy/restore, `--skip-initial-version-creation` for imports, Autokey KeyHandle calls, Key Access Justifications. gcloud commands and flags passed check_commands. Removed: service-agent emails and per-service flag table, org policy constraint names, location-matching rules, pricing notes, attestation and external-key-uri details, custom-role and PAM advice, Terraform and quota gotchas.
Method: documentation only; no commands were run.
