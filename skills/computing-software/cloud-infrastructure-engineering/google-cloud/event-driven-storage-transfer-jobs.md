---
id: computing-software.cloud-infrastructure-engineering.google-cloud.event-driven-storage-transfer-jobs
name: event-driven-storage-transfer-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, storage-transfer-service, event-driven-transfers, s3-sqs-events, continuous-replication, gcloud-transfer]
level: practitioner
status: docs-checked
description: "Set up event-driven Storage Transfer Service jobs that copy new objects continuously from a GCS bucket (Pub/Sub) or S3 (SQS) to a destination bucket, with IAM."
sources: ["https://cloud.google.com/storage-transfer/docs/event-driven-transfers", "https://cloud.google.com/sdk/gcloud/reference/transfer/jobs/create", "https://cloud.google.com/storage-transfer/docs/iam-cloud"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-driven Storage Transfer jobs

Instead of scheduled scans, the job listens for object-change events and transfers new or changed
objects in near-real time, always into a Cloud Storage bucket. Sources: Cloud Storage (Pub/Sub subscription), Amazon S3 (SQS queue
fed by S3 event notifications) and Azure (storage queue events). Object deletions are not detected, so deleting at the source does not delete the destination object.

## GCS to GCS
```bash
gcloud pubsub topics create src-events
gcloud pubsub subscriptions create src-events-sts --topic=src-events
gcloud storage buckets notifications create gs://src-bucket --topic=src-events --event-types=OBJECT_FINALIZE
gcloud transfer jobs create gs://src-bucket gs://dst-bucket \
  --event-stream-name=projects/<P>/subscriptions/src-events-sts \
  --event-stream-starts=2026-10-18T00:00:00+00:00 --name=src-to-dst-live
```
`--event-stream-name` takes a Pub/Sub subscription for Cloud Storage sources, an SQS queue ARN for S3, and an Azure storage queue identifier for Azure (format in the gcloud reference). The start and expiry flags use the `%Y-%m-%dT%H:%M:%S%z` format; without `--event-stream-starts` the job starts listening once created, and without `--event-stream-expires` it listens indefinitely.

The Storage Transfer service agent (`project-<PROJECT_NUMBER>@storage-transfer-service.iam.gserviceaccount.com`) needs:
- source bucket: `roles/storage.legacyBucketReader` and `roles/storage.objectViewer`;
- destination bucket: `roles/storage.legacyBucketWriter`, plus `roles/storage.objectViewer` if the job overwrites only when different or never;
- access to the Pub/Sub subscription (see the Cloud Storage event-driven setup page).
Legacy roles can only be granted at bucket level. The console grants roles for you, as does `gcloud transfer authorize --add-missing`.

## S3 to GCS
1. SQS queue; S3 event notifications sent to the queue.
2. `gcloud transfer jobs create s3://src gs://dst --source-creds-file=creds.json --event-stream-name=arn:aws:sqs:<REGION>:<ACCOUNT_ID>:<QUEUE>`. The AWS-side permissions are listed in the Storage Transfer "event-driven from AWS S3" page; check them there.

## Notes
- Event-driven transfer is the follow-up to a one-time batch migration for existing objects.
- Monitor with `gcloud transfer operations list --job-names=src-to-dst-live`.

## Verify
- [ ] An upload to the source appears in the destination; operations show succeeded counts.

## Checked

2026-10-28. Confirmed against: the Storage Transfer event-driven transfers overview (sources, always a Cloud Storage destination, deletions not detected, live-migration follow-up use), the `gcloud transfer jobs create` reference (`--event-stream-name` formats per source, start and expiry flags and format, defaults) and the Storage Transfer IAM page (service agent name format, bucket-level roles, `gcloud transfer authorize --add-missing`).

Removed: `--ack-deadline`, the Pub/Sub subscriber role and the AWS federation and SQS permission list (not on the pages read), the dedicated-subscription gotcha and timing claims.

Method: documentation only; no commands were run.
