---
id: computing-software.cloud-infrastructure-engineering.aws.sns-subscription-dead-letter-queues
name: sns-subscription-dead-letter-queues
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, subscription-dlq, dead-letter-queue, redrive-policy, sns-delivery-failures]
level: practitioner
status: docs-checked
description: "Attach dead-letter queues to SNS subscriptions so undeliverable messages are kept: RedrivePolicy, queue and KMS policies, FIFO matching, DLQ metrics and redrive."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-configure-dead-letter-queue.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_StartMessageMoveTask.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS subscription dead-letter queues

**Goal:** a message that SNS cannot deliver to a subscriber (endpoint gone, permissions broken,
retries exhausted) lands in an SQS queue you can inspect and replay instead of being dropped.

DLQs are **per subscription**, not per topic.

## Set up
```bash
aws sqs create-queue --queue-name orders-email-dlq \
  --attributes MessageRetentionPeriod=1209600
aws sns set-subscription-attributes --subscription-arn "$SUB" \
  --attribute-name RedrivePolicy \
  --attribute-value "{\"deadLetterTargetArn\":\"$DLQ_ARN\"}"
```
Queue policy so SNS can write:
```json
{"Effect":"Allow","Principal":{"Service":"sns.amazonaws.com"},"Action":"sqs:SendMessage",
 "Resource":"<dlq-arn>","Condition":{"ArnEquals":{"aws:SourceArn":"<topic-arn>"}}}
```
- DLQ must be in the **same account and region** as the subscription.
- Standard topic subscriptions use a standard DLQ; FIFO topic subscriptions use a FIFO DLQ.
- An encrypted DLQ needs a customer managed KMS key whose key policy grants the SNS service principal access
  (for SQS keys the actions are `kms:Decrypt` and `kms:GenerateDataKey`).
- AWS recommends the maximum 14-day retention for DLQs.

## When messages go to the DLQ
- **Client-side errors** (subscribed endpoint deleted, SNS lacks permission to an SQS/Lambda
  endpoint, KMS denies): no retries, straight to the DLQ.
- **Server-side errors** (endpoint unavailable or throwing an exception): after the delivery policy retries are
  exhausted (HTTP/S configurable; SQS and Lambda endpoints retry up to 100,015 times over 23 days; SMTP, SMS and
  mobile push 50 times over 6 hours).
- Failed deliveries do not change the status of your subscriptions. Without a DLQ SNS discards the message.

## Monitor
- `NumberOfNotificationsRedrivenToDlq` and `NumberOfNotificationsFailedToRedriveToDlq` (AWS/SNS, dimension
  `TopicName`). Alarm when the second is > 0: messages could not be moved to the DLQ.
- SQS alarm on DLQ `ApproximateNumberOfMessagesVisible` (AWS recommends it; `NumberOfMessagesSent` does not
  count messages moved on failure), for example threshold 1.

## Redrive
Fix the endpoint, then drain the DLQ: either set it as an event source for a Lambda function or write a
consumer that polls, processes and deletes the messages. SQS `StartMessageMoveTask` does not support DLQs whose
source is SNS, so do not rely on the SQS redrive button here. Consumers must tolerate duplicates.

## Gotchas
- Without a DLQ, exhausted messages are discarded; enable delivery status logging too.
- The DLQ is attached to the subscription, not the topic, and must be in the same account and Region.
- A missing or wrong queue policy on the DLQ (no `sns.amazonaws.com` `SQS:SendMessage` for the topic ARN)
  stops messages reaching it: watch `NumberOfNotificationsFailedToRedriveToDlq`.

## Verify
- [ ] `get-subscription-attributes` shows RedrivePolicy on every production subscription.
- [ ] Test: break the endpoint (deny SNS in the target queue policy), publish, message appears in the DLQ.
- [ ] Alarm on FailedToRedirectToDlq exists.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (dead-letter queues, configuration, delivery retries, CloudWatch metrics) and SQS StartMessageMoveTask reference.
Confirmed: per-subscription DLQ, same account and Region, FIFO matching, RedrivePolicy `deadLetterTargetArn`, queue policy (`sns.amazonaws.com`, `SQS:SendMessage`, `aws:SourceArn` topic), KMS requirement, client-side vs server-side behaviour, retry windows, 14-day recommendation, DLQ alarm metric advice, draining options.
Corrected: metric names are `NumberOfNotificationsRedrivenToDlq` and `NumberOfNotificationsFailedToRedriveToDlq` (the draft's `NumberOfNotifiedMessages...` names do not exist); SQS message-move redrive is not supported for SNS-fed DLQs.
Removed (not in docs): DLQ message error attributes, cross-account DLQ remark, raw-delivery remark.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-configure-dead-letter-queue.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_StartMessageMoveTask.html

Method: documentation only; no commands were run.
