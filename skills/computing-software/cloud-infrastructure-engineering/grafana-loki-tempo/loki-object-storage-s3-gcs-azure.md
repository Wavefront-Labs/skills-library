---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-object-storage-s3-gcs-azure
name: loki-object-storage-s3-gcs-azure
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-object-storage, loki, s3, gcs, azure-blob, storage-config, common-config]
level: practitioner
status: docs-checked
description: "Point Loki at S3, GCS or Azure object storage using the common storage block and credentials without static keys."
sources: ["https://grafana.com/docs/loki/latest/configure/storage/", "https://grafana.com/docs/loki/latest/configure/#common"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: durable chunk and index storage with correct permissions.

Loki keeps small indexes plus compressed chunks in object storage; TSDB is the recommended index. The `common` block shares storage settings between modules, and more specific settings elsewhere override it.

S3 (omit the key fields to use the instance or workload role):
```yaml
common:
  path_prefix: /loki
  replication_factor: 3
  storage:
    s3:
      region: eu-west-1
      bucketnames: loki-chunks
      s3forcepathstyle: false
```
S3-compatible (MinIO) with a custom endpoint:
```yaml
common:
  storage:
    s3:
      endpoint: minio.storage.svc:9000
      bucketnames: loki
      access_key_id: ${S3_ACCESS_KEY}
      secret_access_key: ${S3_SECRET_KEY}
      insecure: true
      s3forcepathstyle: true
```
Run Loki with `-config.expand-env=true` so `${VAR}` is substituted. The `s3` block also accepts `session_token` and an `s3` URL form. GCS uses `gcs: {bucket_name: loki}`; if no `service_account` is given most services fall back to Application Default Credentials (Google recommends Workload Identity Federation over key files). Azure uses `azure:` with `account_name` and `container_name`, plus `use_managed_identity` or `user_assigned_id`, or a service principal (`use_service_principal`, `tenant_id`, `client_id`, `client_secret`).

Schema and index: pair the store with a `schema_config` period (`store: tsdb`, `object_store: s3`, `schema: v13`) and `storage_config.tsdb_shipper` directories.

S3 policy actions in the docs: `s3:ListBucket`, `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject` on the bucket and its objects.

Gotchas
- Retention is performed by the compactor (index entries removed, chunks deleted asynchronously); bucket lifecycle or TTL rules may be kept only as an extra safeguard.
- Never commit secrets; use env-var expansion or the platform identity.
- Never edit an existing `schema_config` period; add a new one.

## Verify
Push a log line, wait for the flush, and check that objects appear in the bucket; confirm the identity can list, read, write and delete.

## Checked
2026-11-03. Confirmed against the Loki storage page and the configuration reference (common.storage, s3_storage_config, azure and gcs fields, `-config.expand-env`). Removed: `loki_ingester_chunks_flushed_total`, the `fake/` prefix claim, "missing DeleteObject breaks compaction silently", the separate-buckets advice, and "workload identity" wording for GCS beyond the documented ADC note.
Method: documentation only; no commands were run.
