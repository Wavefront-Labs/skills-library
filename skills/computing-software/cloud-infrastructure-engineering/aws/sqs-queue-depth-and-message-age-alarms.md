---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-queue-depth-and-message-age-alarms
name: sqs-queue-depth-and-message-age-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, approximateageofoldestmessage, queue-depth, cloudwatch-alarms, backlog-monitoring, dlq-alarm, sqs-metrics]
level: practitioner
status: docs-checked
description: "Alarm on SQS backlog the way on-call needs it: ApproximateAgeOfOldestMessage for latency, visible depth for backlog, DLQ depth > 0, and the metric quirks that hide problems."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/monitoring-using-cloudwatch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS queue depth and message-age alarms

**Goal:** know a queue is falling behind before customers do, with three alarms per queue
and no false pages from idle queues.

## The metrics that matter (AWS/SQS, dimension QueueName, 1-minute)
| Metric | Meaning | Statistic |
|---|---|---|
| `ApproximateAgeOfOldestMessage` | seconds the oldest unprocessed message has waited | Maximum |
| `ApproximateNumberOfMessagesVisible` | backlog ready to receive | Maximum / Average |
| `ApproximateNumberOfMessagesNotVisible` | in flight (received, not deleted) | Maximum |
| `ApproximateNumberOfMessagesDelayed` | in delay queue / timers | Maximum |
| `NumberOfMessagesSent` / `NumberOfMessagesDeleted` | throughput in vs out | Sum |
| `NumberOfEmptyReceives` | `ReceiveMessage` calls that returned nothing (polling waste) | Sum |

Age is the SLO metric: depth of 10,000 is fine if consumers drain it in 30 s; depth of 5 is a
problem if the oldest is 2 hours old.

## Three alarms per queue
```bash
# 1. Latency: oldest message older than the processing SLO (e.g. 5 min) for 3 of 3 minutes
aws cloudwatch put-metric-alarm --alarm-name orders-age \
  --namespace AWS/SQS --metric-name ApproximateAgeOfOldestMessage \
  --dimensions Name=QueueName,Value=orders --statistic Maximum \
  --period 60 --evaluation-periods 3 --datapoints-to-alarm 3 \
  --threshold 300 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching --alarm-actions "$TOPIC_ARN"
# 2. DLQ: anything at all in the dead-letter queue
aws cloudwatch put-metric-alarm --alarm-name orders-dlq-not-empty \
  --namespace AWS/SQS --metric-name ApproximateNumberOfMessagesVisible \
  --dimensions Name=QueueName,Value=orders-dlq --statistic Maximum \
  --period 300 --evaluation-periods 1 --threshold 0 \
  --comparison-operator GreaterThanThreshold --treat-missing-data notBreaching \
  --alarm-actions "$TOPIC_ARN"
# 3. Consumers stalled: messages sent but none deleted (metric math)
#    m1 = NumberOfMessagesSent Sum, m2 = NumberOfMessagesDeleted Sum, e1 = IF(m1>0 AND m2==0, 1, 0)
```
Add a depth alarm only when depth has a hard business meaning (e.g. capacity of a downstream batch window).

## Quirks
- **Idle queues stop emitting.** Metrics are pushed at one-minute intervals for queues that are *active*: a
  queue is active for up to six hours if it contains messages or any action accesses it. After more than six
  hours of inactivity SQS stops delivering metrics. Use `treat-missing-data notBreaching` or the alarm sits in
  INSUFFICIENT_DATA. Reactivating a queue can delay metrics by up to 15 minutes.
- **Poison messages leave the age metric.** On standard queues, a message received three or more times
  without being deleted is moved to the back of the queue and excluded from `ApproximateAgeOfOldestMessage`
  until processed, so the metric points at the next message. Configure a redrive policy so poison messages
  surface in a DLQ.
- **DLQ age:** on standard queues expiry in the DLQ is based on the original enqueue time, and
  `ApproximateAgeOfOldestMessage` in the DLQ reflects when the message moved; set DLQ retention longer than
  the source queue's. When a message is moved to a DLQ after `maxReceiveCount`, the DLQ metric reflects the move time.
- Values are approximate. Metrics such as `ApproximateNumberOfMessagesNotVisible` can briefly show non-zero
  values on an empty queue if a storage server is unavailable, so alarm on several consecutive data points.
- FIFO queues do not reorder: a failed message blocks its message group until it is deleted or expires, so
  alarm on age and watch `ApproximateNumberOfGroupsWithInflightMessages` (FIFO only).

## Dashboards
Plot Sent vs Deleted on one widget (Sum, 1 min) and Visible/NotVisible on another; a widening
gap between Sent and Deleted is the earliest sign of consumer trouble.

## Verify
- [ ] Each production queue has age, DLQ-not-empty and consumer-stalled alarms wired to a topic.
- [ ] Alarms tested: stop the consumer, send 1 message, see age alarm fire after the threshold.
- [ ] DLQ retention >= source retention; DLQ alarm has a runbook link (how to inspect and redrive).

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide ("Available CloudWatch metrics for Amazon SQS", "Monitoring Amazon SQS queues using CloudWatch").
Confirmed: namespace `AWS/SQS`, dimension `QueueName`, metric names and meanings in the table, one-minute reporting, six-hour activity rule, 15-minute reactivation delay, DLQ guidance (use `ApproximateNumberOfMessagesVisible`), poison-message behaviour of the age metric on standard queues (three receives), age reset when moved to a DLQ, and the FIFO blocking behaviour. Also confirmed against the CloudWatch references: `put-metric-alarm` options used in the examples (CLI reference) and metric-math `IF` and `AND` syntax (metric math page).
Corrected: the six-hour activity rule now matches the docs exactly; the three-receives poison-message claim is scoped to standard queues; the unsupported FIFO "per-group backlog is invisible" remark was removed.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/monitoring-using-cloudwatch.html ; https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-alarm.html ; https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html

Method: documentation only; no commands were run.
