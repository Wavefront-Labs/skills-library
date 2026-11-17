---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-visibility-timeout-tuning-and-heartbeats
name: sqs-visibility-timeout-tuning-and-heartbeats
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, visibility-heartbeat, visibility-extension, change-message-visibility, duplicate-processing, consumer-design]
level: practitioner
status: docs-checked
description: "Set SQS visibility timeouts that avoid duplicates and slow retries: sizing rules, per-receive overrides, ChangeMessageVisibility heartbeats for long jobs, and fast-fail on errors."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ChangeMessageVisibility.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS visibility timeout tuning and heartbeats

## 1. What visibility timeout does
After `ReceiveMessage`, the message is hidden for the visibility timeout (queue default 30 s,
range 0 s to 12 h / 43,200 s). If the consumer does not delete it (or extend the timeout) in time, it becomes
visible again and can be received by another consumer; that counts as a failed receive and, depending on the
queue's redrive policy, the message may go to the DLQ. Too short: duplicate processing. Too long: a crashed
consumer delays retries.

## 2. Sizing rules
- Queue default: AWS suggests starting from the maximum time your application typically needs to process and
  delete a message (if unsure, start near 2 minutes and extend), with a heartbeat for variable work.
- Lambda consumers: queue visibility timeout at least **6 x function timeout** (plus
  `MaximumBatchingWindowInSeconds`), because Lambda may retry throttled batches internally.
- Batch receives (10 messages processed sequentially): timeout must cover the whole batch.
- Per-receive override: the `VisibilityTimeout` parameter of `ReceiveMessage` (`receive-message
  --visibility-timeout 120`) applies to the returned messages; without it the queue default is used.

## 3. Heartbeat for long or variable jobs
Start with a modest timeout and extend while working:
```python
import threading
def heartbeat(sqs, url, receipt, stop, every=60, extend_to=180):
    while not stop.wait(every):
        sqs.change_message_visibility(QueueUrl=url, ReceiptHandle=receipt,
                                      VisibilityTimeout=extend_to)

stop = threading.Event()
t = threading.Thread(target=heartbeat, args=(sqs, url, msg["ReceiptHandle"], stop), daemon=True)
t.start()
try:
    process(msg)
    sqs.delete_message(QueueUrl=url, ReceiptHandle=msg["ReceiptHandle"])
finally:
    stop.set()
```
`ChangeMessageVisibility` sets a new timeout counted from **now**, not added to the
remaining time. The limit is 12 hours from when the message was first received, and extending does not
reset it; asking for more than the time left returns an error. For jobs longer than that, AWS suggests
Step Functions or splitting the task into smaller steps. The change is not remembered: the next receive of
the message uses the original timeout again. Batch variant: `change-message-visibility-batch`
(up to 10 entries per call).

## 4. Fail fast on errors
When processing fails and a retry should happen soon, set visibility to 0 (or a short
backoff like 10-30 s) instead of waiting out the full timeout:
```python
sqs.change_message_visibility(QueueUrl=url, ReceiptHandle=receipt, VisibilityTimeout=15)
```
Lambda with `ReportBatchItemFailures` returns failed IDs; those messages become visible again after the
queue's visibility timeout, so keep it reasonable.

## 5. Gotchas
- If processing outlasts the visibility timeout, another worker can receive the same message and process a
  duplicate, and your later `DeleteMessage` can fail with an error: keep a safety margin, extend before
  expiry, and make processing idempotent.
- In-flight limit: about 120,000 messages for standard queues (`OverLimit` on short-polling receives) and
  120,000 for FIFO. Very long visibility with high throughput can reach it.
- FIFO: while a message of a group is invisible, no more messages of that group are returned until the
  visibility timeout expires or it is deleted; other groups are unaffected. A long timeout stalls the group
  after a crash.

## Verify
- [ ] `ApproximateReceiveCount` mostly 1 in sampled messages; DLQ receives only true poison messages.
- [ ] Long jobs extend visibility (CloudTrail/metrics show ChangeMessageVisibility calls) and do not reappear mid-processing.
- [ ] Crashed consumer test: message reappears within the expected timeout.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide and API Reference, Lambda Developer Guide.
Confirmed: default 30 s and range 0 to 43,200 s; failed-receive and DLQ behaviour; 12-hour limit from first receive and no reset; error when exceeding the time left; new timeout counted from the call and reverting on next receive; `ReceiveMessage` `VisibilityTimeout` parameter; batch variant with 10 entries; Lambda 6x rule plus batching window; in-flight limits (the old "20,000 FIFO" was wrong, FIFO is 120,000); FIFO group blocking while in flight.
Removed (not in docs): "p99" sizing rule, the claim that `DeleteMessage` succeeds silently with an expired handle (the docs say it can fail), and "Batch with SQS as a trigger".
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ChangeMessageVisibility.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html ; https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html

Method: documentation only; no commands were run.
