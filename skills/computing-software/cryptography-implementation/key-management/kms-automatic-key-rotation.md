---
id: computing-software.cryptography-implementation.key-management.kms-automatic-key-rotation
name: kms-automatic-key-rotation
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-rotation, kms-automatic-rotation, aws-kms, gcp-cloud-kms, azure-key-vault, key-versions, rotation-period, on-demand-rotation]
level: practitioner
status: docs-checked
description: "What automatic KMS rotation does and does not do in AWS KMS, Google Cloud KMS and Azure Key Vault: old versions stay, ciphertext is not re-encrypted, asymmetric keys excluded."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html", "https://cloud.google.com/kms/docs/key-rotation", "https://learn.microsoft.com/en-us/azure/key-vault/keys/how-to-configure-key-rotation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS automatic key rotation

"Enable automatic rotation" satisfies many compliance checklists, but it does
less than people assume.

## What happens

| | AWS KMS | Google Cloud KMS | Azure Key Vault |
|---|---|---|---|
| Enable | `aws kms enable-key-rotation --key-id K --rotation-period-in-days 365` (valid 90-2560; default 365) | `gcloud kms keys update K --rotation-period=90d --next-rotation-time=...` | rotation policy (`az keyvault key rotation-policy update`) |
| New material | new backing key, **same key ARN/ID** | new primary **key version** | new key version |
| Old material | kept for decrypt (deleted only with the key) | old versions stay enabled until you disable/destroy them | old versions remain |
| On-demand | `aws kms rotate-key-on-demand` | `gcloud kms keys versions create --primary` | `az keyvault key rotate` |
| Symmetric only? | automatic: symmetric encryption keys with AWS-generated material only; on-demand also covers imported material; asymmetric, HMAC and custom key store keys rotate manually | symmetric auto; asymmetric needs manual new versions | rotation policy per key (see the Key Vault rotation page for key types) |

## What it does not do

- **No re-encryption** of existing data. Data encrypted under old material
  stays under it. If the reason for rotation is a suspected compromise of key
  material, automatic rotation does not help: re-encrypt (envelope: rewrap
  DEKs with `ReEncrypt`; data: decrypt/encrypt) and then disable old versions.
- **Data keys (DEKs) do not rotate**. In envelope encryption the KMS key is
  the KEK; rotating it changes how new DEKs are wrapped. Rotate DEKs by policy
  (per object, per day, per volume) in your application.
- **Asymmetric signing keys**: rotation means new keys with new public keys;
  you must publish the new public key and switch signers (JWKS rollover).
- **GCP**: previous versions stay active until destroyed; make sure a version is no longer in use before destroying it, or data is permanently lost.

## Rules

- Rotation period per policy (AWS default one year; Google gives every 90 days as an example).
- Monitor rotation: AWS `GetKeyRotationStatus` and `ListKeyRotations`, CloudTrail and CloudWatch.
- Imported key material (BYOK) in AWS cannot auto-rotate; use on-demand rotation or a new key.

## Verify

- [ ] Rotation enabled on all customer-managed symmetric keys with the policy period.
- [ ] DEK rotation and re-encryption needs handled separately and documented.
- [ ] Old key versions disabled only after usage logs show no decrypts.

## Checked

2026-10-31. Confirmed against AWS rotate-keys and EnableKeyRotation pages (default 365, range 90-2560, symmetric AWS_KMS-origin only for automatic, on-demand incl. imported, manual for asymmetric/HMAC), the Cloud KMS key-rotation page (no asymmetric auto-rotation, versions stay active, 90 days example) and the Key Vault rotation policy page. Removed: AWS Config rule name, GCP SCC claim, Azure key-type claim, usage-tracking claim.
Method: documentation only; no commands were run.
