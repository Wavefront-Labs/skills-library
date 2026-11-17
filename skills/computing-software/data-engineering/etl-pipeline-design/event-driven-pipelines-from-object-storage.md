---
id: computing-software.data-engineering.etl-pipeline-design.event-driven-pipelines-from-object-storage
name: event-driven-pipelines-from-object-storage
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, object-storage-events, event-driven, s3-event-notifications, serverless]
level: advanced
status: docs-checked
description: "Trigger pipelines from object storage events (S3, GCS, Azure Blob): destinations, at-least-once delivery, ordering, execution loops, idempotency and backfill."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html
  - https://cloud.google.com/storage/docs/pubsub-notifications
  - https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-driven pipelines from object storage events

**Goal:** process each file as soon as it lands, without polling schedules, and without losing or double-processing files.

## Wiring
- **AWS**: S3 Event Notifications publish to an SNS topic, an SQS queue, a Lambda function or Amazon EventBridge. You store the configuration in the bucket's notification subresource. SQS FIFO queues are not a supported destination; to reach one, go through EventBridge. A typical shape is S3 -> SQS (buffer) -> worker.
- **GCP**: Pub/Sub notifications for Cloud Storage send messages to a topic you choose (any project you have permission on); subscribers pull from it. Cloud Run functions are the option when you do not want to manage a topic (the bucket must be in the same project as the function).
- **Azure**: Blob storage events are pushed through Event Grid to subscribers such as Azure Functions, Logic Apps or your own HTTP listener. Storage (general purpose v1) does not support Event Grid integration.

## Event types that matter for ingestion
- S3: new object created events are one of the published event families (also removal, restore, replication, lifecycle and others); see the page's "Supported event types" for exact names.
- GCS: `OBJECT_FINALIZE` fires when a new object or new generation is successfully created (including copy, rewrite, restore); a failed upload does not trigger it. Replacing an object produces `OBJECT_FINALIZE` for the new one plus `OBJECT_ARCHIVE` or `OBJECT_DELETE` for the old one.
- Azure: events can be filtered by event type, container name and blob name using subject filters (`subjectBeginsWith`, `subjectEndsWith`) on the subject format `/blobServices/default/containers/<containername>/blobs/<blobname>`. To get `Microsoft.Storage.BlobCreated` only once a block blob is fully committed, filter for the `CopyBlob`, `PutBlob`, `PutBlockList` or `FlushWithClose` REST calls.

## Semantics to design for
- **At-least-once**: S3, Cloud Storage (and Pub/Sub behind it) and Azure Storage events are all documented as at-least-once, so duplicates happen. Make processing idempotent: record processed object keys plus version (ETag, GCS generation) in a control table and skip repeats, or MERGE on business keys.
- **No ordering guarantee**: GCS notifications are not guaranteed to be published in order, and Azure messages can arrive out of order (use the `sequencer` field for the order of events on one blob; use `etag` to tell whether your view is stale). For GCS, use object generation and metageneration as preconditions when you modify an object from a notification.
- **Delay**: there is no SLA on delivery time. GCS may take up to 30 seconds to start sending after you add a configuration; Azure messages can take a few minutes. GCS may delete a notification that consistently cannot be delivered after 7 days.
- **Events can still be missed** (misconfiguration, outages, permissions): run a periodic reconciliation listing the prefix against processed keys.
- **Execution loops (S3)**: a function triggered by uploads that writes back to the same bucket triggers itself. Use two buckets or restrict the trigger to the incoming prefix.
- **Consumers**: check the event type and source (topic) before processing, and ignore fields you do not understand.
- Multi-part producers: wait for a `_SUCCESS` or manifest file and trigger on that, not on each part.

## Scaling and failures
- Queue in front of compute for buffering and retries; dead-letter queue after N attempts with an alert.
- Function runtimes have time and memory limits: hand large files to a batch service.
- Throttle concurrency to protect the warehouse or downstream APIs.

## Backfill
Historic files do not emit events: enqueue them yourself (list + send messages) through the same code path.

## Verify
Drop the same file twice and a burst of 1,000 small files: each processed exactly once in the target; DLQ empty; reconciliation shows no unprocessed keys.

## Checked
Checked 2026-11-08 against the S3 Event Notifications overview, the Cloud Storage Pub/Sub notifications page and the Azure Blob storage events page, each read in full as stripped text. Confirmed: destinations, FIFO note, loop warning, GCS event types and delivery guarantees, Azure filtering, ordering and at-least-once guidance. Removed (not on the pages): the S3 notification JSON and its prefix/suffix filter rules, Eventarc, Event Grid to Storage Queue, and the Snowpipe, Auto Loader and BigQuery notes. S3 ordering is not stated on its page and is not claimed.
Method: documentation only; no commands were run.
