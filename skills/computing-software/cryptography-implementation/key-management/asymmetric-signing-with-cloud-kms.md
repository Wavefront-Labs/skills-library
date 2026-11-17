---
id: computing-software.cryptography-implementation.key-management.asymmetric-signing-with-cloud-kms
name: asymmetric-signing-with-cloud-kms
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, kms-signing, aws-kms, google-cloud-kms, asymmetric-signing, ecdsa, rsa-pss, code-signing, non-exportable-keys]
level: practitioner
status: docs-checked
description: "Sign with non-exportable AWS KMS and Google Cloud KMS asymmetric keys: RAW vs DIGEST messages, DER signatures, public key export and offline verification."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html", "https://docs.aws.amazon.com/cli/latest/reference/kms/sign.html", "https://cloud.google.com/kms/docs/create-validate-signatures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asymmetric signing with cloud KMS

Keep signing keys non-exportable in KMS and verify offline with the exported public key.

## AWS KMS
```
aws kms create-key --key-spec ECC_NIST_P256 --key-usage SIGN_VERIFY --description "release signing"
aws kms get-public-key --key-id <id> --query PublicKey --output text | base64 -d > pub.der
openssl pkey -pubin -inform DER -in pub.der -out pub.pem

# Large files: hash locally, send the digest
openssl dgst -sha256 -binary release.tar > digest.bin
aws kms sign --key-id <id> --message fileb://digest.bin --message-type DIGEST \
  --signing-algorithm ECDSA_SHA_256 --query Signature --output text | base64 -d > release.sig
openssl dgst -sha256 -verify pub.pem -signature release.sig release.tar
```
- `--message-type RAW` accepts up to 4096 bytes and KMS hashes it; `DIGEST` takes a precomputed hash whose length
  must match the algorithm.
- Key specs include RSA_2048/3072/4096, ECC_NIST_P256/P384/P521, ECC_SECG_P256K1, ECC_NIST_EDWARDS25519 and ML_DSA_44/65/87.
- Do not pass an unhashed message with `DIGEST`: KMS skips hashing and security can be compromised. Passing a digest as `RAW` hashes it twice and breaks verification by systems that assume a single hash.

## Google Cloud KMS
```
gcloud kms keys create signer --keyring ring --location global --purpose asymmetric-signing \
  --default-algorithm ec-sign-p256-sha256 --protection-level hsm
gcloud kms keys versions get-public-key 1 --key signer --keyring ring --location global --output-file pub.pem
gcloud kms asymmetric-sign --version 1 --key signer --keyring ring --location global \
  --digest-algorithm sha256 --input-file release.tar --signature-file release.sig
```

## Operational points
- Each sign is an API call; check the vendor's quotas page before using KMS for high-volume per-request signing.
- IAM: `kms:Sign` only for the signing pipeline role; `kms:GetPublicKey` broadly.
- Rotation: plan a new key and publish its public key with an overlap window.

## Checked

2026-10-31. Confirmed in AWS CLI kms sign reference (messages 0-4096 bytes, RAW vs DIGEST, digest length must match the algorithm, double-hash warning), the AWS KMS API model (KeySpec values) and the AWS KMS key types page (ML-DSA keys). CLI commands passed check_commands. Removed: DER encoding and JOSE conversion, FIPS wording, quota and auto-rotation claims, SigningAlgorithms field (not confirmed in fetched pages).

Method: documentation only; no commands were run.

## Verify
- [ ] Offline verification with OpenSSL succeeds against the exported public key.
- [ ] CloudTrail/Audit logs show Sign calls only from the pipeline identity.
