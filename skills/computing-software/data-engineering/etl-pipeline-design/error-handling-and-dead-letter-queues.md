---
id: computing-software.data-engineering.etl-pipeline-design.error-handling-and-dead-letter-queues
name: error-handling-and-dead-letter-queues
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, error-handling, dead-letter-queue, poison-pill, retry-strategy, exponential-backoff, circuit-breaker, transient-vs-permanent-errors, alert-fatigue, quarantine-table, partial-failure]
level: practitioner
status: docs-checked
description: "ETL error handling: classify errors, bound retries, run dead letter queues someone owns (Amazon SQS redrive as example), alert by severity."
sources:
  - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error handling in ETL: fail the right amount

**Goal:** one bad record should not halt a batch, and a systemic failure should not hide as "a few DLQ records" until someone notices the DLQ has been filling for weeks.

## 1. Classify the error before deciding what to do
- **Transient** (timeout, rate limit, source briefly unavailable): retry with a bounded policy.
- **Permanent / data error** (malformed record, failed validation, business-rule violation): the record will fail the same way every time. Route it to quarantine or a DLQ rather than retry-looping.
- **Systemic** (source down, credentials rotated, upstream schema change breaking every record): one root cause that looks like many data errors. A flood of DLQ entries in a short window is the signal. Stop processing and alert instead of quarantining thousands of individually fine records.

## 2. Retry policy
- Bound both the number of attempts and the total retry time, so a misclassified permanent error cannot hold workers indefinitely.
- Retries need idempotent writes: a retry after a timeout where the first attempt actually succeeded can duplicate a non-idempotent write. See computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads.

## 3. Dead letter queues need an owner
Worked example, Amazon SQS (per its Developer Guide):
- A DLQ is a queue that source queues target for messages not processed successfully; it is useful for debugging because unconsumed messages are isolated. The DLQ must be in the same AWS account and Region as the source queue, and you create the queue first, then configure it as a DLQ.
- A redrive policy sets `maxReceiveCount`: how many times a consumer can receive a message before it moves to the DLQ. A low value such as 1 means one failed receive sends the message to the DLQ; set it high enough to allow sufficient retries.
- A redrive allow policy controls which source queues may use the DLQ: all, specific queues via `byQueue` (up to 10 source queue ARNs), or `denyAll`. The default allows all.
- From the DLQ you can examine logs, analyse message contents, check whether the consumer had enough time, and move messages out with DLQ redrive. The guide points to CloudWatch alarms for messages moved to a DLQ.
- For standard queues the enqueue timestamp is unchanged when a message moves, so a message's retention clock keeps running; the guide's best practice is a DLQ retention period longer than the source queue's. For FIFO queues the timestamp resets.
- Do not use a DLQ with a FIFO queue if you need to keep exact message order.

Whatever the platform, minimum hygiene: each entry carries enough context to diagnose without re-running (error, input record, timestamp, failing stage); an alert on DLQ volume or growth rate with an owner who receives it; and a re-drive path that has been tried once after a fix.

## 4. Alerting that reflects severity
Partial failure (a small share of records quarantined) and total failure (source unreachable) need different routes and urgency. Alert on severity tiers and rate of change, not one boolean "errors occurred."

## Verify
- [ ] Transient versus permanent classification is explicit in code, and permanent errors go to the DLQ without burning retries.
- [ ] A simulated source outage stops the pipeline and alerts, rather than quarantining every record.
- [ ] DLQ volume has an alert and a confirmed owner.
- [ ] A DLQ re-drive was tested once.

## Checked
2026-11-01. Confirmed from the Amazon SQS Developer Guide page on dead-letter queues (`sources`): DLQ purpose, same account and Region rule, redrive policy and `maxReceiveCount`, redrive allow policy options, redrive, retention and timestamp behaviour for standard and FIFO queues, FIFO ordering note. Removed (no page read): the exponential backoff with jitter rationale, the circuit breaker description and the retry-storm claim.
Method: documentation only; no commands were run.
