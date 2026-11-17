---
id: computing-software.cloud-infrastructure-engineering.minio.sse-c
name: sse-c
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, sse-c, client-managed-keys, customer-provided-keys, aes256, sse-c-headers, replication-compatibility]
level: advanced
status: docs-checked
description: "Use SSE-C with MinIO and client-supplied 256-bit keys, the required X-Amz headers, replication behaviour since 2024-03-30, and the rule that SSE-C overrides SSE-KMS and SSE-S3."
sources: ["https://github.com/minio/docs/blob/main/source/administration/server-side-encryption/server-side-encryption-sse-c.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO SSE-C (client-managed keys)

With SSE-C MinIO encrypts each object with the key the client provides on that request. MinIO **does not store** SSE-C keys and cannot decrypt without them. The key must be 256-bit, either raw base64 encoded or hex encoded (hex support arrived in MinIO Client RELEASE.2024-06-20T14-50-54Z). A non-production way to generate one: `cat /dev/urandom | head -c 32 | base64 -`; follow organisational standards for real keys.

## Headers
- `X-Amz-Server-Side-Encryption-Customer-Algorithm: AES256`
- `X-Amz-Server-Side-Encryption-Customer-Key`: the key
- `X-Amz-Server-Side-Encryption-Customer-Key-MD5`: the 128-bit MD5 digest of the key
`mc` and S3 SDKs have syntax for setting these; `mc cp` has dedicated arguments.

## Considerations
- **Overrides SSE-S3 and SSE-KMS.** An SSE-C object is not additionally encrypted by those.
- **No bucket default** for SSE-C.
- **Replication.** From RELEASE.2024-03-30T09-41-56Z, SSE-C objects replicate through bucket and site replication; earlier versions did not. SSE-C objects that are also compressed are not compatible with either replication type; use SSE-KMS or SSE-S3 for that.
- **Erasure.** Disabling the key temporarily locks the objects; deleting it makes them permanently unreadable (irreversible without client-side key backups). The scope of a key is the set of writes that used it.

Overview of the three strategies: `computing-software.cloud-infrastructure-engineering.minio.sse-overview`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: SSE-C page (server-side-encryption-sse-c.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
