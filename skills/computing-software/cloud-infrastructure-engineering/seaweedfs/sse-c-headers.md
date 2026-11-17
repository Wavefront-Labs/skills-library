---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.sse-c-headers
name: sse-c-headers
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [customer-provided-keys, aes256, x-amz-server-side-encryption-customer-key, sse-c, customer-key, customer-provided]
level: advanced
status: docs-checked
description: "Use SSE-C with SeaweedFS: send your own AES-256 key and MD5 on every request; keys are never stored, so a lost key means lost data."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Server-Side-Encryption-SSE-C
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sse c headers

SSE-C: the client supplies the key per request; SeaweedFS encrypts and decrypts server-side and never stores the key.

Required headers on every PUT, GET and HEAD:
```
X-Amz-Server-Side-Encryption-Customer-Algorithm: AES256
X-Amz-Server-Side-Encryption-Customer-Key: <base64 256-bit key>
X-Amz-Server-Side-Encryption-Customer-Key-MD5: <md5 of the key>
```
```bash
KEY=$(openssl rand -base64 32)
KEY_MD5=$(echo -n "$KEY" | base64 -d | md5sum | cut -d' ' -f1)
curl -X PUT "$S3_ENDPOINT/bucket/enc.txt"   -H "X-Amz-Server-Side-Encryption-Customer-Algorithm: AES256"   -H "X-Amz-Server-Side-Encryption-Customer-Key: $KEY"   -H "X-Amz-Server-Side-Encryption-Customer-Key-MD5: $KEY_MD5" --data "secret"
```
Download and metadata calls must send the same headers and the same key.

Gotchas:
- Lose the key and the object is unrecoverable.
- The AWS CLI/SDK can set these headers for you (`--sse-c`, `--sse-c-key`).
- Prefer SSE-KMS if you need central key management and audit.

Errors: missing SSE-C headers give 400 `InvalidRequest`; an algorithm other than AES256 gives 400 `InvalidEncryptionAlgorithmError`; a bad key format or MD5 mismatch gives 400 `InvalidArgument`.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages Server-Side Encryption SSE-C (headers, key never stored, openssl and md5sum key generation, `--sse-c` and `--sse-c-key`, error table) and Server-Side Encryption (SSE-KMS gives central key management and audit logs). Replaced the Verify line with the page's error table.
Method: documentation only; no commands were run.
