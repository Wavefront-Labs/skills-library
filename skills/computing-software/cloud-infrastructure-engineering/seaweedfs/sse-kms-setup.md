---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.sse-kms-setup
name: sse-kms-setup
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [kms, openbao, ssekms-key-id, sse-kms, key-id]
level: advanced
status: docs-checked
description: "Enable SSE-KMS on SeaweedFS S3 with AWS KMS, Google Cloud KMS or OpenBao/Vault, using a kms block in the S3 config, and compare with SSE-S3."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Server-Side-Encryption-SSE-KMS
  - https://github.com/seaweedfs/seaweedfs/wiki/Server-Side-Encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sse kms setup

Choose: SSE-KMS (external KMS, audit trails), SSE-C (your keys, per request, see the SSE-C skill), SSE-S3 (SeaweedFS-managed; `x-amz-server-side-encryption: AES256` or bucket default).

Providers: AWS KMS and Google Cloud KMS (full), OpenBao/Vault (full), Azure Key Vault (experimental, build tag `azurekms`).

Add a `kms` section to the S3 config JSON (it sits beside identities):
```json
"kms":{"default_provider":"openbao","providers":{"openbao":{"type":"openbao","address":"http://localhost:8200","token":"root-token","transit_path":"transit","cache_enabled":true,"cache_ttl":"1h"}}}
```
```bash
weed s3 -config=s3_kms_config.json -port=8333
aws --endpoint-url $S3_ENDPOINT s3 cp test-file.txt s3://mybucket/test-file.txt   --server-side-encryption aws:kms --ssekms-key-id alias/my-key
```
Per-bucket key assignment and Bucket Key optimization are supported.

Gotchas:
- `weed filer.backup` decrypts SSE-KMS objects before uploading, but it does not load the S3 config; give it `[kms]` in `security.toml` or `WEED_KMS_*` variables.
- SSE-S3 key material comes from `s3.sse.kek` or `s3.sse.key` in `security.toml` (see the environment-variable skill).

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages Server-Side Encryption SSE-KMS (providers and support levels, kms block fields, `weed s3 -config`, aws:kms and `--ssekms-key-id` example) and Server-Side Encryption (comparison, per-bucket keys, Bucket Key, filer.backup `[kms]` in security.toml or `WEED_KMS_*`, `s3.sse.kek` and `s3.sse.key`). Removed the Verify line (the head-object output is not on the page).
Method: documentation only; no commands were run.
