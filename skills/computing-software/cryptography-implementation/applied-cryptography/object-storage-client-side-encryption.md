---
id: computing-software.cryptography-implementation.applied-cryptography.object-storage-client-side-encryption
name: object-storage-client-side-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, client-side-encryption, s3-encryption, sse-kms, sse-s3, sse-c, s3-encryption-client, gcs-cmek, azure-storage-encryption, object-storage]
level: practitioner
status: draft
description: "Choose S3/GCS/Azure server-side versus client-side encryption: SSE-S3, SSE-KMS, bucket keys, SSE-C, S3 Encryption Client v3 and commitment policy."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html", "https://docs.aws.amazon.com/amazon-s3-encryption-client/latest/developerguide/what-is-s3-encryption-client.html", "https://cloud.google.com/storage/docs/encryption"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Object storage: client-side versus server-side encryption

## AWS S3 options
| Option | Who holds keys | Protects against |
|---|---|---|
| SSE-S3 (default for all new objects since 2023) | AWS-managed | Physical media loss |
| SSE-KMS / DSSE-KMS | KMS key you control (policies, CloudTrail) | Access without KMS permission; gives an audit trail per decrypt |
| SSE-C | You send the key with each request | AWS storing your key; you must manage keys and lose data if you lose them |
| Client-side (S3 Encryption Client) | You, before upload | The storage provider and anyone with only S3 permissions |

**Bucket keys** (`BucketKeyEnabled`) cut SSE-KMS request costs by caching a bucket-level data key; CloudTrail then
logs per bucket key rather than per object.

## Client-side with the S3 Encryption Client v3
- Uses AES-GCM with a KMS (or raw AES/RSA) keyring, stores the wrapped data key in object metadata or an instruction
  file.
- Migrate from v1/v2: v1 used AES-CBC/unauthenticated modes; v3 defaults to key-committing algorithm suites and
  refuses legacy formats unless explicitly enabled. Decrypt legacy objects with `enableLegacyUnauthenticatedModes`
  only during migration, then re-encrypt.
- Range GETs on client-side encrypted objects need special support; check before choosing it for large media.

## GCS and Azure
- GCS: Google-managed by default; CMEK (Cloud KMS key) per bucket or object; CSEK (customer-supplied, like SSE-C).
- Azure Storage: Microsoft-managed keys, customer-managed keys in Key Vault, and client-side encryption v2 (v1 used
  AES-CBC without authentication and must be migrated).

## Decision rules
- Regulated data where provider staff/admins are in the threat model: client-side.
- Need provider features (S3 Select, replication with transformation, server-side analytics): SSE-KMS.
- Enforce with bucket policy: deny `PutObject` without `s3:x-amz-server-side-encryption: aws:kms` and the right key.

## Verify
- [ ] `aws s3api head-object` shows the expected `ServerSideEncryption` and key ID.
- [ ] Client-side objects cannot be read with S3 permissions alone.
- [ ] Legacy-format decrypts are logged and trending to zero.
