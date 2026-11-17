---
id: computing-software.cloud-infrastructure-engineering.aws.s3-event-notifications
name: s3-event-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-event, s3-events, event-notifications, s3-eventbridge, lambda-trigger, sqs, sns, object-created, object-removed, prefix-filter, suffix-filter, idempotency, event-driven, s3-batch-operations, url-encoded-key, at-least-once, fan-out, restore-events, notification-permissions, destination-validation, event-types-s3, objectcreated]
level: practitioner
status: docs-checked
description: "Wire S3 object events to Lambda, SQS, SNS or EventBridge: pick the target, write filters, handle at-least-once delivery and URL-encoded keys, avoid recursion, backfill with Batch Operations."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ev-events.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html", "https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# S3 event notifications

**Goal:** every object landing in (or leaving) a bucket triggers exactly the right
downstream work, once in effect, with no lost events during bursts and no recursive
triggers that cost a fortune overnight.

## 1. Two delivery mechanisms
| | Classic notifications (`NotificationConfiguration`) | EventBridge |
|---|---|---|
| Targets | Lambda, SQS (standard queues only), SNS (standard topics only); one destination per rule | Any EventBridge rule target |
| Filtering | Literal prefix/suffix per rule; filters cannot overlap for the same event types | Event patterns on event fields (`prefix`, `suffix`, `wildcard`, `numeric`, `equals-ignore-case` operators) |
| Event types | Created/Removed/Restore/Replication/Lifecycle/IntelligentTiering/Tagging/ACL/Retention | Object Created, Object Deleted, Restore Initiated/Completed/Expired, Storage Class Changed, Access Tier Changed, ACL Updated, Tags Added/Deleted, Retention Updated (all sent once enabled) |
| Delivery | At least once; typically seconds, sometimes a minute or longer; not guaranteed in order | Delivered through EventBridge (see its documentation); EventBridge pricing applies |
Enable EventBridge with
`aws s3api put-bucket-notification-configuration --bucket b --notification-configuration '{"EventBridgeConfiguration":{}}'`
— the same configuration object can also carry classic destinations. Consider EventBridge for anything beyond "one
prefix → one Lambda"; its rules are not subject to the classic filter-overlap restriction.

## 2. Classic configuration
```json
{"LambdaFunctionConfigurations": [{
   "Id": "thumbnails",
   "LambdaFunctionArn": "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:thumb",
   "Events": ["s3:ObjectCreated:*"],
   "Filter": {"Key": {"FilterRules": [{"Name": "prefix", "Value": "uploads/"},
                                       {"Name": "suffix", "Value": ".jpg"}]}}}],
 "QueueConfigurations": [{
   "Id": "ingest", "QueueArn": "arn:aws:sqs:<REGION>:<ACCOUNT_ID>:ingest",
   "Events": ["s3:ObjectCreated:Put", "s3:ObjectCreated:CompleteMultipartUpload"],
   "Filter": {"Key": {"FilterRules": [{"Name": "prefix", "Value": "landing/"}]}}}]}
```
- `put` **replaces the whole configuration**; `get` → merge → `put`, and let one IaC
  stack own it (two CloudFormation stacks writing the same bucket's notifications clobber
  each other — a classic cross-stack bug).
- Target must grant S3: Lambda resource policy (`lambda add-permission --principal s3.amazonaws.com --source-arn arn:aws:s3:::b --source-account <ACCOUNT_ID>`),
  SQS/SNS policy allowing `sqs:SendMessage`/`sns:Publish` from `s3.amazonaws.com` with
  `aws:SourceArn` condition. S3 verifies SNS and SQS destinations at `put` time; a failure means
  the policy is missing.
- Filter values are literal: `*` wildcards are not allowed, a space in a value must be written `+`, and other
  special characters must be percent-encoded. For case variants add a rule for each, or use EventBridge
  (`suffix` with `equals-ignore-case`).
- **Overlap rule**: for the same event types, filters may not overlap in prefix, suffix or prefix+suffix
  (`uploads/` and `uploads/2026/` on `ObjectCreated:*` is rejected; overlapping prefixes are fine if the suffixes
  do not overlap, and overlapping filters are fine for different event types).
- SQS FIFO queues and SNS FIFO topics are not supported as direct targets (EventBridge → FIFO queue is fine).

## 3. The event, and how to process it correctly
Payload is `Records[]`; each record has `eventName`, `s3.bucket.name`, `s3.object.key`,
`size`, `eTag`, `versionId`, `sequencer`.
- **Key is URL-encoded** (`red flower.jpg` arrives as `red+flower.jpg`): decode with
  `urllib.parse.unquote_plus` before `GetObject`.
- **At-least-once**: duplicates happen. Make the handler idempotent (DynamoDB
  conditional put on `bucket/key/versionId/sequencer`, or an output that is overwritten).
  `sequencer` (present on PUT and DELETE events) orders events *for the same key*: left-pad the shorter value
  with zeros, then compare lexicographically; it does not order across keys.
- Deletes: `ObjectRemoved:Delete` for an unversioned delete or a permanent version delete,
  `ObjectRemoved:DeleteMarkerCreated` when a delete marker is created; lifecycle expirations fire
  `LifecycleExpiration:*`, not `ObjectRemoved`.
- `ObjectCreated:Put` does **not** fire for multipart uploads
  (`CompleteMultipartUpload`) or `Copy`; subscribe to `ObjectCreated:*`.
- Restores from Glacier emit `ObjectRestore:Post` (started) and `:Completed` — wait for Completed.

## 4. Choosing the target
- **Lambda direct**: simplest. S3 invokes the function asynchronously; on a function error Lambda by default
  retries two more times, then discards the event, so configure an on-failure destination or a dead-letter queue.
  Throttled events are retried for up to 6 hours by default; set reserved concurrency to protect downstream.
- **SQS → Lambda (event source mapping)**: buffers bursts and batches messages (each message has its own
  `Records[]`); Lambda supports partial batch responses. A sensible shape for anything with a database behind it.
- **SNS**: fan-out to several consumers; add SQS subscriptions per consumer.
- **EventBridge rule**: `{"source":["aws.s3"],"detail-type":["Object Created"],"detail":{"bucket":{"name":["b"]},"object":{"key":[{"wildcard":"uploads/*.parquet"}],"size":[{"numeric":[">",0]}]}}}`;
  target Step Functions for multi-step pipelines.

## 5. Avoid the recursion bill
A function that writes back to the bucket that triggers it loops forever. Write to a
different bucket or a prefix excluded by the filter (`in/` → `out/` with the rule on
`in/`), and set a CloudWatch alarm on invocation count.

## 6. Backfill existing objects
Notifications fire only for new events. For "process everything already here" use
**S3 Batch Operations** with a manifest (from S3 Inventory or a CSV) and a
`LambdaInvoke` operation — it drives your function per object and produces a completion report.

## Gotchas
- Delivery does not check that the consumer can read the object: an SSE-KMS object
  whose key denies the Lambda role still produces an event, and the handler then fails
  with `AccessDenied`. Test the consumer end to end, not only delivery.

## Verify
- [ ] `aws s3 cp test.jpg s3://b/uploads/a b.jpg` triggers one processing run that logs the decoded key `uploads/a b.jpg`.
- [ ] Uploading a 200 MB file (multipart) triggers the rule (proves `ObjectCreated:*`, not `:Put`).
- [ ] Replaying the same event twice produces no duplicate side effect.
- [ ] Lambda DLQ / SQS DLQ exists and an injected failure lands there.
- [ ] Invocation-count alarm exists; writing output back does not re-trigger (check CloudWatch `Invocations` stays flat).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: destinations, FIFO exclusions, standard-only SNS/SQS, same-Region requirement, filter grammar (no wildcards, `+` for spaces, percent-encoding) and the overlap rule, delivery semantics, event names and delete semantics, `sequencer` comparison, key URL-encoding, EventBridge event types and the `detail.bucket.name` / `detail.object.key` / `size` fields, EventBridge `wildcard` and `numeric` operators (event bus rules only), Lambda asynchronous retry behaviour, S3 Batch Operations `LambdaInvoke` operation, the self-trigger loop warning. Removed unconfirmed pricing, replay, Lambda loop-detection and cross-account claims.

Method: documentation only; no commands were run.
