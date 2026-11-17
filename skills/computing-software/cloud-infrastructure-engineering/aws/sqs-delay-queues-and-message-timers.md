---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-delay-queues-and-message-timers
name: sqs-delay-queues-and-message-timers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, delay-queue, message-timer, delay-seconds, change-message-visibility, backoff, scheduled-messages, retry-with-delay, eventbridge-scheduler, step-functions-wait, messaging]
level: practitioner
status: docs-checked
description: "Use SQS DelaySeconds (queue-level delay queues vs per-message timers, 15-minute cap) for deferred work and retry backoff, and know when to switch to visibility changes or EventBridge Scheduler."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-delay-queues.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-timers.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS delay queues and message timers

**Goal:** "do this in N seconds" without a cron, a sleep in a worker, or a polling table —
and without hitting the 15-minute ceiling by surprise.

## 1. The two mechanisms
| | Delay queue (`DelaySeconds` queue attribute) | Message timer (`DelaySeconds` on `SendMessage`) |
|---|---|---|
| Applies to | every message sent to the queue | that message only; overrides the queue default |
| Range | 0–900 s (15 min) | 0–900 s |
| FIFO | supported | **not supported** (FIFO queues do not support timers on individual messages) |
| Change after send | standard queue: not retroactive (messages already queued keep their delay); FIFO queue: **retroactive** (affects messages already in the queue) | cannot be changed after send; use `ChangeMessageVisibility` once received |

```bash
aws sqs set-queue-attributes --queue-url "$Q" --attributes '{"DelaySeconds":"300"}'
aws sqs send-message --queue-url "$Q" --message-body '{"job":"reminder"}' --delay-seconds 600
```
While delayed, a message is invisible to consumers and is reported by the queue attribute
`ApproximateNumberOfMessagesDelayed`. A message is in flight only after a consumer has received it,
so a delayed message is not in flight.

## 2. Retry with backoff (the common real use)
Instead of re-sending a failed message with a timer (which creates a new message, resets
receive count and breaks DLQ logic), **extend the visibility** of the message you already hold:
```python
attempt = int(msg["Attributes"]["ApproximateReceiveCount"])
delay = min(900, 2 ** attempt * 5)        # 10, 20, 40 ... capped at 15 min
sqs.change_message_visibility(QueueUrl=q, ReceiptHandle=msg["ReceiptHandle"], VisibilityTimeout=delay)
# do NOT delete; it becomes visible again after `delay` and the DLQ maxReceiveCount still applies
```
`ChangeMessageVisibility` accepts 0 to 43200 s (12 hours), counted from when the message was first
received; extending does not reset that limit. The new timeout starts counting at the call, and the call
fails (for example `MessageNotInflight`) if the message is no longer in flight. With a Lambda SQS
event source mapping, enable partial batch responses (`ReportBatchItemFailures` in
`FunctionResponseTypes`, return `batchItemFailures` with `itemIdentifier`) and let the queue's visibility
timeout be the retry delay; the queue's redrive policy (Lambda recommends `maxReceiveCount` of at least 5)
moves the rest to the DLQ.

## 3. When 15 minutes is not enough
- **EventBridge Scheduler** one-time schedules (`at(2026-10-16T09:00:00)`) targeting SQS,
  Lambda or any API: AWS names it the recommended solution for scheduling beyond 15 minutes, with no
  time limit; `ActionAfterCompletion` (`NONE | DELETE`) removes the schedule after it runs. A completed
  one-time schedule still counts against your account quota until deleted. Schedules fire with 60-second precision.
- **Step Functions** `Wait` state when the delayed action is part of a workflow.

## 4. Scheduler one-time example
```bash
aws scheduler create-schedule --name remind-1234 --schedule-expression "at(2026-10-17T08:30:00)" \
  --schedule-expression-timezone "Europe/London" --flexible-time-window Mode=OFF \
  --action-after-completion DELETE \
  --target '{"Arn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:reminders","RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/scheduler-to-sqs","Input":"{\"orderId\":\"1234\"}"}'
```

## Gotchas
- A message timer overrides the queue's `DelaySeconds`; on a FIFO queue only the queue-level delay is available.
- Delay queues and visibility timeouts both hide a message, but a delay hides it when first added to
  the queue, a visibility timeout only after it is received.

## Verify
- [ ] A message sent with `--delay-seconds 60` shows in `ApproximateNumberOfMessagesDelayed` and becomes receivable at ~60 s (`receive-message` with 20 s long poll returns it on the fourth call, not the first).
- [ ] Backoff path: a consumer that calls `ChangeMessageVisibility` on failure sees `ApproximateReceiveCount` 1, 2, 3 at increasing intervals and the message moves to the DLQ once `maxReceiveCount` is exceeded.
- [ ] A Scheduler one-time schedule delivers once and the schedule disappears (`ActionAfterCompletion=DELETE`).

## Checked

Date 2026-10-23. Documentation release: current AWS docs for Amazon SQS, EventBridge Scheduler and Lambda.
Confirmed: delay and timer range 0 to 15 minutes; FIFO does not support per-message timers; per-queue delay is retroactive on FIFO but not on standard queues (this corrected the earlier text); timer overrides queue delay; `ChangeMessageVisibility` limits (12 h from first receive, not reset by extension, `MessageNotInflight`); `ApproximateNumberOfMessagesDelayed` attribute; Scheduler `at()` syntax, `--schedule-expression-timezone`, `ActionAfterCompletion` NONE|DELETE, `FlexibleTimeWindow` required; Lambda partial batch response name and shape. Removed claims not found in the docs: `InvalidParameterValue` error name, Lambda `MaximumRetryAttempts` for SQS (wrong), Step Functions Wait limit, DynamoDB TTL timer, hop-chaining advice, DLQ-to-delay-queue and SNS delay behaviour, age-of-oldest-message alarm claim.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-delay-queues.html ; .../sqs-message-timers.html ; .../APIReference/API_ChangeMessageVisibility.html ; https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html ; https://docs.aws.amazon.com/scheduler/latest/APIReference/API_CreateSchedule.html

Method: documentation only; no commands were run.
