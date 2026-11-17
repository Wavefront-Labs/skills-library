---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-notifications-for-cloud-storage
name: pubsub-notifications-for-cloud-storage
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, gcs-pubsub-notifications, object-change-notifications, object-finalize, pubsub, event-driven]
level: practitioner
status: docs-checked
description: "Configure Pub/Sub notifications on Cloud Storage buckets: event types, prefix filters, payload format, the GCS service agent permission, duplicates, and limits per bucket."
sources: ["https://docs.cloud.google.com/storage/docs/pubsub-notifications", "https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/notifications/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub notifications for Cloud Storage

## Create
```bash
gcloud storage buckets notifications create gs://uploads --topic=projects/<P>/topics/uploads-events \
  --event-types=OBJECT_FINALIZE,OBJECT_DELETE --object-prefix=incoming/ \
  --payload-format=json --custom-attributes=env=prod
gcloud storage buckets notifications list gs://uploads
gcloud storage buckets notifications delete projects/_/buckets/uploads/notificationConfigs/<ID>
```
The command checks that the topic grants the Cloud Storage service agent the `pubsub.topics.publish` permission and tries to grant it if not; use `--skip-topic-setup` if you lack topic access or the topic is already set up. Defaults: all event types, `--payload-format=json` (the other value is `none`). If `--topic` is omitted, the topic in your default project named after the bucket is used.

## Events
| Type | When |
|---|---|
| `OBJECT_FINALIZE` | new object or new generation successfully created (including copy, rewrite, restore); failed uploads do not trigger it |
| `OBJECT_METADATA_UPDATE` | metadata changed |
| `OBJECT_DELETE` | object permanently deleted (including by lifecycle rules or replacement in a non-versioned bucket) |
| `OBJECT_ARCHIVE` | live version became noncurrent (only with object versioning enabled) |

Message attributes always include `notificationConfig`, `eventType`, `payloadFormat`, `bucketId`, `objectId`, `objectGeneration` and `eventTime`; `overwroteGeneration` (on FINALIZE replacements) and `overwrittenByGeneration` (on ARCHIVE or DELETE replacements) appear when relevant. The data is the object metadata resource as JSON (`JSON_API_V1`, set with `--payload-format=json`) or empty (`NONE`).

## Consumer guidance
- At-least-once delivery: dedupe with `bucketId/objectId#objectGeneration`.
- Replacing an object produces a FINALIZE for the new generation and a DELETE (non-versioned) or ARCHIVE (versioned) for the old one carrying `overwrittenByGeneration`.
- Notifications are not guaranteed to arrive in order; use generation and metageneration as preconditions when acting on them. There is no delivery SLA, and a new configuration can take up to 30 seconds to start.

## Limits
- A bucket can have up to 100 notification configurations in total, and up to 10 configured to trigger for a specific event; custom attributes are limited to 10 per configuration.
- Objects created by your consumer in the same prefix will trigger again: write outputs to another prefix or bucket.

## Alternatives
Eventarc triggers for Cloud Storage events; Storage Insights for bulk inventory.

## Verify
- [ ] Uploading `incoming/test.txt` produces a message with eventType=OBJECT_FINALIZE on a test subscription.

## Checked
Checked 2026-10-24 against the Cloud Storage Pub/Sub notifications page and the gcloud `storage buckets notifications create` reference (docs.cloud.google.com). Confirmed event types, attributes, payload formats, limits (100 per bucket, 10 per event), at-least-once and ordering statements, and the flags used. Removed the service-agent address and role name, which the pages do not give, and the Eventarc "built on this" claim. The page also lists OBJECT_INITIALIZE for zonal buckets, not covered here. Argument form of `notifications delete` was not documented on the pages read, so confirm it with `gcloud storage buckets notifications delete --help`.
Method: documentation only; no commands were run.
