---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-dlq-redrive-and-maxreceivecount
name: sqs-dlq-redrive-and-maxreceivecount
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, dead-letter-queue, dlq, dlq-redrive, maxreceivecount, redrive-policy, redrive-allow-policy, start-message-move-task, poison-message, visibility-timeout, retention-period, approximate-receive-count, dlq-alarm, messaging]
level: practitioner
status: docs-checked
description: "Size SQS maxReceiveCount against visibility timeout and retries, alarm on DLQ depth, inspect poison messages, and redrive them back with StartMessageMoveTask without replaying garbage."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues-redrive.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_StartMessageMoveTask.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS dead-letter queues: maxReceiveCount tuning and redrive

**Goal:** poison messages leave the main queue after a bounded number of attempts, nobody
loses them, someone is paged when they accumulate, and replaying them later is a button —
not a script that duplicates everything.

## 1. Wire the DLQ
```bash
DLQ_ARN=$(aws sqs get-queue-attributes --queue-url "$DLQ" --attribute-names QueueArn --query Attributes.QueueArn --output text)
aws sqs set-queue-attributes --queue-url "$MAIN" --attributes "{
  \"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"$DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"5\\\"}\",
  \"VisibilityTimeout\":\"90\"}"
# lock the DLQ so only this source can dead-letter into it
aws sqs set-queue-attributes --queue-url "$DLQ" --attributes "{\"RedriveAllowPolicy\":\"{\\\"redrivePermission\\\":\\\"byQueue\\\",\\\"sourceQueueArns\\\":[\\\"$MAIN_ARN\\\"]}\"}"
```
- DLQ must be the **same type** (standard/FIFO) and same account+region as the source.
- Set the DLQ `MessageRetentionPeriod` longer than the source queue's (maximum 1209600 s = 14 days;
  default 4 days). On a **standard** queue expiry is based on the original enqueue timestamp, which is
  unchanged by the move, so a message that sat 5 days in the main queue has only 9 days left in a
  14-day DLQ. On a **FIFO** queue the enqueue timestamp resets when the message moves to the DLQ.
- Valid `maxReceiveCount` is 1 to 1,000 (console); the API default is 10. For standard queues with
  `maxReceiveCount` greater than 3, a message received 3 or more times without deletion is moved to the
  back of the queue.
- `RedriveAllowPolicy` `redrivePermission` is `allowAll` (default), `denyAll` or `byQueue`; `byQueue`
  accepts at most 10 `sourceQueueArns`.
- Do not put a DLQ on a FIFO queue if you need to keep exact message order.

## 2. Choosing maxReceiveCount
`ApproximateReceiveCount` increments on every `ReceiveMessage` that returns the message,
including receives that time out because the consumer crashed or the visibility timeout was
too short. So:
- **Transient failures** (downstream 503, throttling): you want several retries, so keep
  `maxReceiveCount` high enough for them. For a Lambda consumer set the queue visibility timeout to at
  least 6x the function timeout (plus `MaximumBatchingWindowInSeconds` when a batching window is used).
- **Lambda event source mapping**: AWS recommends `maxReceiveCount` of at least 5. If Lambda hits an error
  processing a batch, all messages in that batch return to the queue (including ones that succeeded)
  unless you enable partial batch responses (`ReportBatchItemFailures`, return `batchItemFailures`).
  Without it, one bad record sends the whole batch back on every attempt.
- `maxReceiveCount: 1` is a "no retries" switch — appropriate only when retries are handled
  elsewhere (Step Functions) or the work is strictly non-idempotent.
- SQS moves the message to the DLQ when its receive count exceeds `maxReceiveCount`.

## 3. Alarm
```bash
aws cloudwatch put-metric-alarm --alarm-name orders-dlq-depth --namespace AWS/SQS \
  --metric-name ApproximateNumberOfMessagesVisible --dimensions Name=QueueName,Value=orders-dlq \
  --statistic Maximum --period 60 --evaluation-periods 1 --threshold 0 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching --alarm-actions arn:aws:sns:<REGION>:<ACCOUNT_ID>:oncall
```
AWS recommends `ApproximateNumberOfMessagesVisible` for monitoring a DLQ. Messages moved automatically are
not counted in `NumberOfMessagesSent`. `ApproximateAgeOfOldestMessage` on a standard DLQ reflects time since
the original enqueue, so an alarm on it approaching retention (for example > 10 days) is a useful second signal.

## 4. Inspect without consuming
`aws sqs receive-message --queue-url "$DLQ" --max-number-of-messages 10 --visibility-timeout 0
--message-system-attribute-names All --message-attribute-names All` — `--visibility-timeout 0` peeks without
hiding the message from others. Read `SentTimestamp`, `ApproximateFirstReceiveTimestamp` and
`ApproximateReceiveCount`; correlate with consumer logs by message ID. Fix the consumer
**before** redriving, or the messages come straight back.

## 5. Redrive (the built-in way)
```bash
aws sqs start-message-move-task --source-arn "$DLQ_ARN" --max-number-of-messages-per-second 50   # max 500; omit to let SQS pick the rate
# or to a different queue (quarantine, replay queue):
aws sqs start-message-move-task --source-arn "$DLQ_ARN" --destination-arn "$REPLAY_ARN"
aws sqs list-message-move-tasks --source-arn "$DLQ_ARN"     # Status RUNNING/COMPLETED/FAILED, ApproximateNumberOfMessagesMoved
aws sqs cancel-message-move-task --task-handle "$HANDLE"
```
- Omitting `--destination-arn` redrives each message to its original source queue.
- The source must be a DLQ whose sources are other SQS queues; DLQs fed by Lambda or SNS are not supported.
- Only one active message movement task is supported per queue; set a rate so the consumer is not flooded.
- Task status values come from `list-message-move-tasks`; cancel with the `TaskHandle` returned by start.

## Gotchas
- Lambda's own `--dead-letter-config` and on-failure destinations are for **asynchronous**
  invocations; for SQS-triggered functions only the queue's RedrivePolicy matters.
- `RedriveAllowPolicy` `denyAll` on a DLQ blocks every source from using it.
- Moving a message to a DLQ does not change its encryption: encrypted stays encrypted, and an
  unencrypted message stays unencrypted in an encrypted DLQ. A consumer of the DLQ needs `kms:Decrypt` on
  the source queue's key.

## Verify
- [ ] A consumer that always throws sees the message move to the DLQ once its receive count exceeds `maxReceiveCount` (check `ApproximateReceiveCount`).
- [ ] DLQ alarm fires within 2 minutes of the first dead-lettered message.
- [ ] `start-message-move-task` returns messages to the source and the fixed consumer processes them once.
- [ ] A message sent to the DLQ directly by another queue is rejected (RedriveAllowPolicy `byQueue`).

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide and API Reference, Lambda Developer Guide.
Confirmed: DLQ same account, Region and queue type; RedrivePolicy and RedriveAllowPolicy attribute names, values and the 10-ARN limit; maxReceiveCount default 10 and console range 1 to 1,000; retention semantics for standard vs FIFO (corrected: the old text applied the standard rule to all queues); StartMessageMoveTask limits (max 500 per second, one active task, DLQ-with-SQS-sources only, default destination is original source); Lambda 6x visibility rule, maxReceiveCount of 5, partial batch response; DLQ metric guidance; encryption of moved messages.
Removed claims not found in the docs: receive-time redrive nuance, receive count and retention reset on redrive, FIFO group-id preservation, move-task failure on oversize messages, retention effect of RedrivePolicy change.
Also confirmed against the ReceiveMessage reference: `VisibilityTimeout` per call, `ApproximateReceiveCount`, and that `AttributeNames` is deprecated in favour of `MessageSystemAttributeNames` (the peek command was updated).
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html ; .../sqs-configure-dead-letter-queue.html ; .../APIReference/API_SetQueueAttributes.html ; .../APIReference/API_StartMessageMoveTask.html ; .../sqs-available-cloudwatch-metrics.html ; https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html

Method: documentation only; no commands were run.
