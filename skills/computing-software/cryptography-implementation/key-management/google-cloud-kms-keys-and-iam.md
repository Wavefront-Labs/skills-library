---
id: computing-software.cryptography-implementation.key-management.google-cloud-kms-keys-and-iam
name: google-cloud-kms-keys-and-iam
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, google-cloud-kms, gcp, cloud-kms, gcloud, key-rings, key-versions, cmek, iam, protection-level]
level: practitioner
status: docs-checked
description: "Manage Google Cloud KMS key rings, keys, versions, protection levels, rotation and IAM roles with gcloud, including destroy scheduling and CMEK."
sources: ["https://docs.cloud.google.com/kms/docs/resource-hierarchy", "https://docs.cloud.google.com/kms/docs/create-encryption-keys", "https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Cloud KMS key rings, versions and IAM

## Resource model
Project > location > **key ring** > **key** (purpose, protection level, rotation) > **key versions** (the actual
material). Key rings and keys can't be renamed after creation, and the names of deleted keys can't be reused. A key's purpose and protection level can't be changed after creation.

## Create
```
gcloud kms keyrings create app-ring --location europe-west1
gcloud kms keys create orders --keyring app-ring --location europe-west1 \
  --purpose encryption --protection-level hsm \
  --rotation-period 90d --next-rotation-time 2026-12-01T00:00:00Z
```
Protection levels (API names): `SOFTWARE`, `HSM` (multi-tenant HSM), `HSM_SINGLE_TENANT`, `EXTERNAL`, `EXTERNAL_VPC`.

## Use
```
gcloud kms encrypt --key orders --keyring app-ring --location europe-west1 \
  --plaintext-file secret.bin --ciphertext-file secret.enc --additional-authenticated-data-file aad.bin
gcloud kms decrypt --key orders --keyring app-ring --location europe-west1 \
  --ciphertext-file secret.enc --plaintext-file out.bin --additional-authenticated-data-file aad.bin
```

## IAM
| Role | Grants |
|---|---|
| `roles/cloudkms.cryptoKeyEncrypterDecrypter` | encrypt + decrypt on a key |
| `roles/cloudkms.cryptoKeyEncrypter` / `Decrypter` | one direction only |
| `roles/cloudkms.admin` | manage keys, no crypto operations |
| `roles/cloudkms.signerVerifier` | asymmetric sign/verify |
Grant at the lowest level that works (CryptoKey); avoid the owner role. `roles/cloudkms.admin` grants broad administration without the ability to encrypt or decrypt.
```
gcloud kms keys add-iam-policy-binding orders --keyring app-ring --location europe-west1 \
  --member serviceAccount:app@proj.iam.gserviceaccount.com --role roles/cloudkms.cryptoKeyEncrypterDecrypter
```

## Verify
- [ ] Key-level IAM shows only intended principals.
- [ ] Admin and crypto-use roles are held by different principals.

## Checked
2026-10-31. Confirmed against the Cloud KMS resource hierarchy, create-keys quickstart and roles reference pages:
protection-level names, purpose and protection level immutable, no rename or name reuse, role names and what they grant,
owner-role advice. Removed (not on the fetched pages): FIPS level, 64 KiB limit, destroy-schedule default, CMEK service
agent steps, audit-log defaults. gcloud flags checked with check_commands.
Method: documentation only; no commands were run.
