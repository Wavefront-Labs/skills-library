---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-object-storage-backends
name: grafana-mimir-object-storage-backends
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [object-storage, s3, gcs, azure, swift, minio]
level: practitioner
status: docs-checked
description: "Describes Mimir supported object storage backends, bucket rules, the common storage block and the requirement to keep blocks apart from ruler and Alertmanager storage."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-object-storage-backend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Object storage backends

Mimir persists blocks, ruler rules and Alertmanager state in object storage. Mimir does not create the bucket; create it yourself.

## Supported

Amazon S3 (and compatible such as MinIO), Google Cloud Storage, Azure Blob Storage, and Swift. The implementation must not create directories, because Mimir has no notion of them and leaves empty directories after removing blocks. On Azure, disable hierarchical namespace. Ruler and Alertmanager also support a read-only `local` implementation for provisioning state.

## Common configuration

```yaml
common:
  storage:
    backend: s3
    s3:
      endpoint: s3.us-east-2.amazonaws.com
      region: us-east-2
      access_key_id: "${AWS_ACCESS_KEY_ID}"
      secret_access_key: "${AWS_SECRET_ACCESS_KEY}"
blocks_storage:
  s3:
    bucket_name: mimir-blocks
alertmanager_storage:
  s3:
    bucket_name: mimir-alertmanager
ruler_storage:
  s3:
    bucket_name: mimir-ruler
```

Environment variable expansion must be enabled for `${...}` values. When mixing YAML and flags watch the precedence rules.

## Rules to remember

- Blocks storage cannot share the same bucket and prefix as ruler or Alertmanager storage. Mimir fails to start if it does; use a different bucket or a storage prefix.
- S3 endpoint must not be prefixed with the bucket name.
- Prefer injecting cloud credentials (such as a GCS service account) through environment variables rather than writing them in the file.

## Checked

Confirmed against the page: supported backends, no-directories rule and Azure hierarchical namespace, local implementation for ruler and Alertmanager, the S3 common config example, same bucket and prefix failure, endpoint rule, environment variable expansion and precedence note. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-object-storage-backend page (grafana/mimir main), read in full.
