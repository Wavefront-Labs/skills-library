---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-import-topics-from-kafka-and-cloud-storage
name: pubsub-import-topics-from-kafka-and-cloud-storage
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pubsub-import-topics, kafka-ingestion, cloud-storage-ingestion, kinesis]
level: practitioner
status: docs-checked
description: "Create Pub/Sub import topics that ingest from Cloud Storage, Amazon MSK, Confluent Cloud, Azure Event Hubs or Kinesis without writing a connector, and monitor ingestion."
sources: ["https://docs.cloud.google.com/pubsub/docs/create-cloud-storage-import-topic", "https://github.com/googleapis/googleapis/blob/master/google/pubsub/v1/pubsub.proto", "https://docs.cloud.google.com/sdk/gcloud/reference/pubsub/topics/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub import topics

An import topic pulls from an external source and publishes into itself; subscriptions consume as usual.

## 1. From Cloud Storage
```bash
gcloud pubsub topics create gcs-ingest \
  --cloud-storage-ingestion-bucket=<BUCKET> \
  --cloud-storage-ingestion-input-format=text --cloud-storage-ingestion-text-delimiter=$'\n' \
  --cloud-storage-ingestion-minimum-object-create-time=2026-10-01T00:00:00Z \
  --cloud-storage-ingestion-match-glob='logs/**.jsonl'
```
- Formats: `text` (one message per delimiter, default newline), `avro` (Avro binary objects), `pubsub_avro` (objects written by a Cloud Storage subscription).
- Grant the Pub/Sub service account the permissions `storage.objects.list`, `storage.objects.get` and `storage.buckets.get` on the bucket (for example via `roles/storage.legacyObjectReader` and `roles/storage.legacyBucketReader`).

## 2. From Kafka (Amazon MSK / Confluent Cloud / Azure Event Hubs)
```bash
gcloud pubsub topics create msk-ingest \
  --aws-msk-ingestion-cluster-arn=<ARN> --aws-msk-ingestion-topic=orders \
  --aws-msk-ingestion-aws-role-arn=<IAM_ROLE_ARN> \
  --aws-msk-ingestion-service-account=pubsub-msk@<P>.iam.gserviceaccount.com
```
- The AWS role is assumed with `AssumeRoleWithWebIdentity` and must be set up with `accounts.google.com:sub` equal to the service account's number; the Pub/Sub service account needs the `iam.serviceAccounts.getOpenIdToken` permission on that service account.
- Confluent: `--confluent-cloud-ingestion-bootstrap-server`, `-cluster-id`, `-topic`, `-identity-pool-id`, `-service-account`; Event Hubs: `--azure-event-hubs-ingestion-resource-group`, `-namespace`, `-event-hub`, `-client-id`, `-tenant-id`, `-subscription-id`, `-service-account`.
- Kinesis: `--kinesis-ingestion-stream-arn`, `--kinesis-ingestion-consumer-arn` (Enhanced Fan-Out consumer), `--kinesis-ingestion-role-arn`, `--kinesis-ingestion-service-account`.

## 3. Monitor
- Topic metrics `topic/ingestion_data_source_state` and `topic/ingestion_failure_count`; platform logs are off unless you set `--ingestion-log-severity` (the API severities are DISABLED, DEBUG, INFO, WARNING, ERROR).
- `gcloud pubsub topics describe` shows `ingestionDataSourceSettings`, including the source `state` (ACTIVE, or an error such as CLOUD_STORAGE_PERMISSION_DENIED, PUBLISH_PERMISSION_DENIED, BUCKET_NOT_FOUND, TOO_MANY_OBJECTS).

## Gotchas
- Only objects created at or after `--cloud-storage-ingestion-minimum-object-create-time` and matching `--cloud-storage-ingestion-match-glob` are ingested; quote the glob in the shell.
- Invalid Avro objects are not ingested; Avro block size is limited to 16 MB.
- A topic update that omits an ingestion setting resets it to its default.

## Verify
- [ ] A test object/record appears on a pull subscription; state is ACTIVE.

## Checked
Checked 2026-10-24 against the googleapis `google/pubsub/v1/pubsub.proto` (IngestionDataSourceSettings, PlatformLogsSettings), the gcloud `pubsub topics create` reference and the Cloud Storage import topic page (docs.cloud.google.com). Confirmed every `--*-ingestion-*` flag name, input formats, required Cloud Storage permissions, the web-identity setup, states and metric names. Removed the unconfirmed message-size, Kafka key, re-ingestion and pause-flag claims. The MSK import documentation page returned 404, so MSK specifics rely on the proto only.
Method: documentation only; no commands were run.
