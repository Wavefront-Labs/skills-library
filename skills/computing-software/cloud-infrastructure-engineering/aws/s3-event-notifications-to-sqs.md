---
id: computing-software.cloud-infrastructure-engineering.aws.s3-event-notifications-to-sqs
name: s3-event-notifications-to-sqs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-to-sqs, queue-policy-s3, sqs, kms-encrypted-queue, event-driven-ingestion]
level: practitioner
status: docs-checked
description: "Wire S3 event notifications to an SQS queue: queue policy with SourceArn/SourceAccount, KMS-encrypted queues, FIFO limits, consumer patterns and validation errors."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 event notifications to SQS

## 1. Queue policy
```json
{"Version": "2012-10-17",
 "Statement": [{
   "Sid": "AllowS3Send", "Effect": "Allow",
   "Principal": {"Service": "s3.amazonaws.com"},
   "Action": "sqs:SendMessage",
   "Resource": "arn:aws:sqs:eu-west-1:111122223333:ingest",
   "Condition": {"ArnLike": {"aws:SourceArn": "arn:aws:s3:::raw-uploads"},
                 "StringEquals": {"aws:SourceAccount": "111122223333"}}}]}
```
```bash
aws sqs set-queue-attributes --queue-url <url> --attributes file://attrs.json   # {"Policy": "<policy as an escaped JSON string>"}
```
Include `aws:SourceAccount`: bucket ARNs contain no account ID, and the S3 documentation's SQS example pairs `aws:SourceArn` with it.

## 2. Encrypted queues
- If the queue is encrypted with an AWS KMS customer managed key, its key policy must allow the S3 principal (the S3 documentation describes only this case):
```json
{"Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"},
 "Action": ["kms:GenerateDataKey", "kms:Decrypt"], "Resource": "*"}
```

## 3. Notification configuration
```bash
aws s3api put-bucket-notification-configuration --bucket raw-uploads \
  --notification-configuration '{"QueueConfigurations": [{
     "Id": "to-ingest", "QueueArn": "arn:aws:sqs:eu-west-1:111122223333:ingest",
     "Events": ["s3:ObjectCreated:*"],
     "Filter": {"Key": {"FilterRules": [{"Name": "prefix", "Value": "incoming/"},
                                         {"Name": "suffix", "Value": ".csv"}]}}}]}'
```
When you save, S3 verifies that the queue exists and that the bucket owner has permission to publish to it; a failure
means the queue policy (or KMS key policy) does not let S3 send. S3 sends an `s3:TestEvent` message to the queue
on save (it has no `Records` array); consumers must ignore it.

## 4. Constraints
- Queue must be in the **same region** as the bucket.
- **FIFO queues are not supported** as S3 notification destinations; use EventBridge and
  then a FIFO target, or a standard queue.
- Set the queue's `MaximumMessageSize` to at least 64 KB: notification messages can be up to 64 KB and SQS rejects larger ones.
- Filters cannot overlap (prefix, suffix or both) for the same event types; a rule without a filter overlaps
  with every other rule for those events. Fan out via SNS or EventBridge.

## 5. Consumer pattern
- Message body is the S3 event JSON with `Records[]`. Keys are
  URL-encoded (`red flower.jpg` becomes `red+flower.jpg`): decode with `urllib.parse.unquote_plus`.
- Delivery is at least once and not guaranteed to be in order; dedupe on `bucket + key + versionId/sequencer`
  (`sequencer` is present on PUT and DELETE events and orders events for the same key only).
- A Lambda consumer through an SQS event source mapping gives batching and retries; size the queue's visibility
  timeout using the Lambda SQS guidance.
- Large backfills: S3 Batch Operations or an inventory-driven enqueue instead of relying on
  events for existing objects (events only fire for new operations).

## Verify
- [ ] Upload `incoming/test.csv`; a message with that key arrives in the queue.
- [ ] Uploading a `.txt` or outside the prefix produces no message.
- [ ] DLQ configured on the queue; consumer handles `s3:TestEvent` and encoded keys.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: SQS policy shape and conditions, customer-managed-key key-policy statement, FIFO not supported, same-Region requirement, 64 KB `MaximumMessageSize` guidance, filter-overlap rule, TestEvent format, key URL-encoding, `sequencer` semantics, at-least-once delivery. Removed unconfirmed claims about the AWS managed SQS key, cross-account queues, the exact validation error text and the visibility-timeout multiple.

Method: documentation only; no commands were run.
