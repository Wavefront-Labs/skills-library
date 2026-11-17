---
id: computing-software.cloud-infrastructure-engineering.minio.sse-kms
name: sse-kms
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, sse-kms, mc-encrypt-set, minio-kms-kes-endpoint, minio-kms-kes-api-key, minio-kms-kes-key-name, kes-key-create, external-key, per-bucket-keys]
level: advanced
status: docs-checked
description: "Enable per-bucket SSE-KMS in MinIO with kes key create, MINIO_KMS_KES_ variables, a restart and mc encrypt set sse-kms, including key scope and erasure effects."
sources: ["https://github.com/minio/docs/blob/main/source/administration/server-side-encryption/server-side-encryption-sse-kms.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO SSE-KMS (per-bucket keys)

Each bucket or object can use its own External Key (EK). MinIO can decrypt an object only if it can reach both the KMS and that EK. Bucket default:

```
mc encrypt set sse-kms EXTERNALKEY play/mybucket
```

## Quickstart flow (play sandbox, non-production)
1. Create an EK with the `kes` CLI. Set `KES_CLIENT_KEY` and `KES_CLIENT_CERT` to the identity key and cert; the identity needs at least the `/v1/create`, `/v1/generate` and `/v1/list` API endpoints. Then `kes key create my-minio-sse-kms-key` (pick a unique name).
2. On every MinIO server host set:
```
export MINIO_KMS_KES_ENDPOINT=https://play.min.io:7373
export MINIO_KMS_KES_API_KEY=<API key from KES>
export MINIO_KMS_KES_KEY_NAME=<key name>
```
The API key is the preferred auth; alternatively use `MINIO_KMS_KES_KEY_FILE` plus `MINIO_KMS_KES_CERT_FILE`. These are mutually exclusive: set the API key or the key/cert files, never all three. The API key's identity must be able to create, generate and decrypt keys.
3. Restart: `mc admin service restart ALIAS`.
4. Enable the bucket default: `mc encrypt set sse-kms my-minio-sse-kms-key ALIAS/BUCKET` (a bucket prefix also works). Repeat per bucket; use different keys per bucket or prefix to narrow each key's scope.

## Write path
A write needs an EK: the bucket EK, replaced by an explicit EK in the request if given; in buckets without a default, the EK from the request. Production deployments should use a supported KMS instead of the play sandbox.

## Scope of loss
Disabling an EK temporarily makes its objects unreadable; deleting it makes them permanently unreadable (irreversible unless the KMS has backups). With one EK per bucket, one disabled key affects one bucket; with one key for everything, it affects the whole deployment.

## Checked

2026-11-03. Confirmed against the MinIO docs source: the SSE-KMS page: environment variables, kes key create, bucket and object encryption flags. Removed or fixed: nothing.

Method: documentation only; no commands were run.
