---
id: computing-software.cloud-infrastructure-engineering.minio.sse-s3
name: sse-s3
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, sse-s3, mc-encrypt-set-sse-s3, deployment-wide-key, minio-kms-kes-key-name, kes, bucket-default-encryption]
level: advanced
status: docs-checked
description: "Enable SSE-S3 in MinIO with a single deployment-wide external key set by MINIO_KMS_KES_KEY_NAME and bucket default encryption through mc encrypt set sse-s3."
sources: ["https://github.com/minio/docs/blob/main/source/administration/server-side-encryption/server-side-encryption-sse-s3.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO SSE-S3 (per-deployment key)

SSE-S3 en/decrypts objects with one External Key (EK) from a KES-backed KMS, named by the `MINIO_KMS_KES_KEY_NAME` environment variable at server startup. MinIO uses that same EK for all SSE-S3 operations. Bucket default:

```
mc encrypt set sse-s3 play/mybucket
```

It is functionally compatible with AWS SSE-S3 and supports the same KMS targets as KES.

## Quickstart (play sandbox, evaluation only)
1. Create the key with the `kes` CLI: `kes key create my-minio-sse-s3-key`, using a KES client identity configured through `KES_CLIENT_KEY` / `KES_CLIENT_CERT`.
2. On each MinIO server host:
```
export MINIO_KMS_KES_ENDPOINT=https://play.min.io:7373
export MINIO_KMS_KES_API_KEY=<API-key-identity-string-from-KES>
export MINIO_KMS_KES_KEY_NAME=my-minio-sse-s3-key
```
Alternatively use `MINIO_KMS_KES_KEY_FILE` and `MINIO_KMS_KES_CERT_FILE` in place of the API key; do not mix them.
3. Restart the deployment (`mc admin service restart ALIAS`) so the configuration applies.
4. Enable bucket default encryption with `mc encrypt set sse-s3 ALIAS/BUCKET`.

For production, use one of the KES-supported KMS integrations. The docs say SSE-KMS cannot be disabled once enabled. When you need per-bucket keys instead of one global key, see `computing-software.cloud-infrastructure-engineering.minio.sse-kms`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: server-side-encryption and the SSE-S3 page: MINIO_KMS_KES_* variables, kes key create, KES_CLIENT_KEY, the KEY_FILE alternative, mc encrypt set. Removed or fixed: the SSE requires-TLS claim and the TLS cross-reference (the pages read do not say it).

Method: documentation only; no commands were run.
