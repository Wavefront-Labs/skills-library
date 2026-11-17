---
id: computing-software.cloud-infrastructure-engineering.aws.kms-importing-key-material-byok
name: kms-importing-key-material-byok
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, import-key-material, byok, external-origin-key, key-material-expiration, wrapping-key]
level: advanced
status: docs-checked
description: "Bring your own key material into KMS: create an EXTERNAL-origin key, wrap material with the import token, set expiry, reimport, and plan for deletion and rotation limits."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-get-public-key-and-token.html", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-import-key-material.html", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-delete-key-material.html", "https://docs.aws.amazon.com/kms/latest/developerguide/imported-key-material-expiration-alarm.html", "https://docs.aws.amazon.com/kms/latest/developerguide/kms-events.html", "https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing key material into KMS (BYOK)

**Why:** a regulator or contract requires that you generate keys in your own HSM, keep an
escrow copy, or be able to make data unreadable instantly by deleting key material. Cost:
you own durability of the material. If you lose your copy and delete or let it expire,
the data is gone.

## 1. Create a key with no material
```bash
KEY=$(aws kms create-key --origin EXTERNAL --key-spec SYMMETRIC_DEFAULT \
  --key-usage ENCRYPT_DECRYPT --description "BYOK payments" --query KeyMetadata.KeyId --output text)
aws kms create-alias --alias-name alias/payments-byok --target-key-id $KEY
```
State is `PendingImport`. Imported material is supported for symmetric encryption, asymmetric (except ML-DSA and ML-KEM) and HMAC keys, including multi-Region keys; not for keys in custom key stores.

## 2. Get the wrapping public key and import token
```bash
aws kms get-parameters-for-import --key-id $KEY \
  --wrapping-algorithm RSAES_OAEP_SHA_256 --wrapping-key-spec RSA_4096 \
  --query '{K:PublicKey,T:ImportToken}' --output json > params.json
jq -r .K params.json | base64 -d > wrapping-key.bin
jq -r .T params.json | base64 -d > import-token.bin
```
The public key and import token set is valid for **24 hours**; download a new set if it lapses. Wrapping algorithms by key material (docs): 256-bit AES symmetric key material uses `RSAES_OAEP_SHA_256` (or `RSAES_OAEP_SHA_1`); asymmetric RSA private key material uses `RSA_AES_KEY_WRAP_SHA_256`; `RSAES_PKCS1_V1_5` is no longer supported (since 10 October 2023). Wrapping key specs are `RSA_2048`, `RSA_3072`, `RSA_4096`; ECC key material cannot be wrapped directly with a small RSA key, use a larger wrapping key or an `RSA_AES_KEY_WRAP_SHA_*` algorithm.

## 3. Generate and wrap the material
In production generate inside your HSM and wrap there. For a test:
```bash
openssl rand -out material.bin 32
openssl pkeyutl -encrypt -in material.bin -out wrapped.bin -inkey wrapping-key.bin \
  -keyform DER -pubin -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256
```
This matches the `RSAES_OAEP_SHA_256` parameters requested above.

## 4. Import
```bash
aws kms import-key-material --key-id $KEY \
  --encrypted-key-material fileb://wrapped.bin --import-token fileb://import-token.bin \
  --expiration-model KEY_MATERIAL_EXPIRES --valid-to <TIMESTAMP_WITHIN_365_DAYS>
```
Or `--expiration-model KEY_MATERIAL_DOES_NOT_EXPIRE`. An expiry can be at most 365 days after import. At expiry KMS deletes the material and the key becomes `PendingImport`, unusable for cryptographic operations until you reimport a copy of the **same** material. You cannot change or cancel the expiry of the current import; reimport the same material to change it. The first material imported becomes permanently associated with the key.

## 5. Lifecycle operations
- **Delete material now:** `aws kms delete-imported-key-material --key-id $KEY` (key ID or ARN, not an alias). The key becomes `PendingImport` and unusable right away, subject to eventual consistency; there is no 7-30 day waiting period (that applies to scheduled key deletion). Resources encrypted under data keys protected by the key are not affected until the key is used again, for example to decrypt a data key.
- **Rotation:** you cannot enable automatic rotation for a key with imported material, but you can rotate manually. Symmetric encryption keys with imported material support on-demand rotation: import multiple key materials and rotate on demand to change the current one. Asymmetric and HMAC keys with EXTERNAL origin can have only one key material.
- **Monitoring:** KMS sends a `KMS Imported Key Material Expiration` event to EventBridge when material expires (best effort, so it is not an early warning). For early warning, use the CloudWatch metric `SecondsUntilKeyMaterialExpires` (published only for keys with expiring material, one alarm per key; the documented example alarms at less than 30 days).

## Gotchas
- You can reimport the same key material but cannot import different material into the key.
- AWS KMS keeps imported material highly available but does not maintain its durability at the same level as KMS-generated material; keep your own copy.
- Deleting key material halts use of the key, but data already protected by cached or decrypted data keys is unaffected until the key is next needed.
- The 24-hour public key and token window matters for offline HSM ceremonies; plan the ceremony inside it.

## Verify
- [ ] `aws kms describe-key` shows `Origin: EXTERNAL`, `KeyState: Enabled`, and `ValidTo` as planned.
- [ ] Encrypt/decrypt round-trip works, and reimporting the escrowed copy into the same key succeeds (proves the escrow is the right material).
- [ ] Expiration alarm exists and fires in a test with a short-lived key.

## Checked
2026-10-27. Documentation: AWS KMS Developer Guide (importing key material, get public key and import token, import key material, delete imported key material, expiration alarm, EventBridge events, considerations), read this date. Confirmed: 24-hour public key and token validity, wrapping algorithm and key spec support (RSAES_PKCS1_V1_5 unsupported since 10 October 2023), expiry up to 365 days, expired material makes the key PendingImport, delete-imported-key-material takes key ID or ARN and acts immediately, no automatic rotation but on-demand rotation for symmetric keys, SecondsUntilKeyMaterialExpires metric (the draft said SecondsUntilKeyMaterialExpiration) and the expiration EventBridge event. Confirmed from the KMS API model: ImportKeyMaterial parameters and enums, WrappingKeySpec and AlgorithmSpec values. Removed unconfirmed multi-Region replica import instructions and the exception name.
Method: documentation only; no commands were run.
