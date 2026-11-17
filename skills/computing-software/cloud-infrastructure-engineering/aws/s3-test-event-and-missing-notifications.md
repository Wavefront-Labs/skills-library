---
id: computing-software.cloud-infrastructure-engineering.aws.s3-test-event-and-missing-notifications
name: s3-test-event-and-missing-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, test-event, missing-notifications, s3-event-notifications, troubleshooting]
level: advanced
status: docs-checked
description: "Debug S3 event notifications that never arrive: s3:TestEvent, destination and KMS policies, event types, encoded keys, overwritten configs and delivery semantics."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# s3:TestEvent and debugging missing notifications

## 1. s3:TestEvent
When you save a notification configuration, S3 sends a test message to each destination:
```json
{"Service":"Amazon S3","Event":"s3:TestEvent","Time":"...","Bucket":"uploads-prod","RequestId":"...","HostId":"..."}
```
It has no `Records` array: consumers must skip it instead of crashing. Receiving it proves the destination
policy works at config time.

## 2. Checklist when real events do not arrive
1. **Config overwritten**: `aws s3api get-bucket-notification-configuration --bucket b`. IaC tools or a
   second team calling `put-bucket-notification-configuration` replace the whole config.
2. **Event type**: multipart uploads emit `s3:ObjectCreated:CompleteMultipartUpload`; copies emit `:Copy`;
   lifecycle expirations are `s3:LifecycleExpiration:*`, not `ObjectRemoved:Delete`.
3. **Filters**: values are literal (no `*` wildcards), a space must be written `+` and other special characters
   percent-encoded; keys in events are URL-encoded (space becomes `+`), so decode before use. Filters for the same
   event types cannot overlap.
4. **Destination permissions**: SQS/SNS policy for `s3.amazonaws.com` with matching `aws:SourceArn`;
   Lambda resource policy (`lambda add-permission --principal s3.amazonaws.com --source-arn ...`).
5. **KMS**: for a queue or topic encrypted with a customer managed key, the key policy must allow the S3
   principal `kms:GenerateDataKey` and `kms:Decrypt`.
6. **Destination type and Region**: SQS/SNS/Lambda destinations must be in the bucket's Region; SQS FIFO queues and SNS FIFO topics are not supported.
7. **Consumer side**: message delivered but the Lambda failed/throttled, or the queue's consumer deleted it.

## 3. Delivery semantics
Typically within seconds but sometimes a minute or longer; delivered at least once (rare duplicates) and not
guaranteed to arrive in order. Use `sequencer` (present on PUT and DELETE events) to order events for the same key.

## 4. Prove what S3 did
Enable CloudTrail data events for the bucket to confirm the PUT happened, then check the destination's own
CloudWatch metrics and logs.

## Verify
- [ ] Consumer ignores TestEvent; a test upload triggers exactly the expected destination.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: TestEvent format and purpose (no `Records` array), event-type naming for multipart, copy and lifecycle, filter grammar and overlap rule, URL-encoded keys, KMS key-policy requirement for customer managed keys, Region and FIFO restrictions, delivery semantics, `sequencer`. Removed the unconfirmed AWS managed key statement, the same-key single-notification claim and specific destination metric names.

Method: documentation only; no commands were run.
