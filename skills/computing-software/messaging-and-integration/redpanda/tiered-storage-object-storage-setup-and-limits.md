---
id: computing-software.messaging-and-integration.redpanda.tiered-storage-object-storage-setup-and-limits
name: tiered-storage-object-storage-setup-and-limits
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [tiered-storage, cloud-storage, s3, gcs, object-storage, enterprise, iam]
level: advanced
status: docs-checked
description: "Configure Redpanda Tiered Storage object storage on S3 or GCS with an instance role or access keys, know its enterprise license and limitations, and reset properties correctly."
sources:
  - https://docs.redpanda.com/streaming/current/manage/tiered-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tiered Storage offloads log segments to object storage and needs an enterprise license; check with `rpk cluster license info`. Supported stores: Amazon S3, Google Cloud Storage, Azure Blob Storage and ADLS.

**Limitations.** No migrating topics to another provider or bucket/container, and no multi-region buckets or containers. The page advises against re-enabling Tiered Storage after enabling and disabling it, because of inconsistent data and gaps.

**S3 with an IAM role**, set via `rpk cluster config edit`:

```properties
cloud_storage_enabled: true
cloud_storage_credentials_source: aws_instance_metadata
cloud_storage_region: <region>
cloud_storage_bucket: <redpanda-bucket-name>
```

**S3 with access keys.** Grant `GetObject`, `DeleteObject`, `PutObject`, `PutObjectTagging` and `ListBucket`, then set `cloud_storage_access_key` and `cloud_storage_secret_key` in place of the credentials source.

**GCS with an IAM role** uses the same keys plus:

```properties
cloud_storage_api_endpoint: storage.googleapis.com
cloud_storage_credentials_source: gcp_instance_metadata
```
For GCS access keys: choose uniform access control, a Google-managed key, a default project, and a service user with HMAC keys.

**SSE-KMS (S3).** Create a symmetric encrypt-and-decrypt KMS key, give the bucket the Key user permission (the configuring user needs Key admin), set the bucket default encryption to SSE-KMS, and optionally re-encrypt existing objects with `aws s3 cp` using `--sse-kms-key-id` and `--sse aws:kms`. Cloud-provider keys cannot be set per topic.

**Caution.** Never set an object storage property to `""` or `null` to reset it. Use `rpk cluster config force-reset <config-name>` or remove the line.

## Checked

2026-11-04. License check, limitations, property sets, KMS steps and the reset caution were confirmed on the Tiered Storage page. Azure steps were not read.

Method: documentation only; no commands were run.
